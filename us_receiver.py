import pyaudio
import math
import time
import Queue
import threading
from constants import *

total_frames = SAMPLE_RATE * NUMBER_OF_SECONDS
current_frames = 0

frame_queue = Queue.Queue()
window_queue = Queue.Queue()

def goertzel_filter(samples, target):
	"""
	Applies the Goertzel filter to the set of samples
	to see if the target frequency can be found

	:param samples: A list of samples collected from the
		external environment
	:param target: The target frequency to detect in the
		samples
	"""
	w = (2 * math.pi * target) / SAMPLES_PER_SYMBOL
	cos_w = math.cos(w)
	sin_w = math.sin(w)
	coefficient = 2 * cos_w

	s_prev = 0.0
	s_prev2 = 0.0

	for index, sample in enumerate(samples):
		hamm_window = ord(sample) * (0.54 - 0.46 * math.cos(2 * math.pi * (index / SAMPLES_PER_SYMBOL)))
		s_next = hamm_window + (coefficient * s_prev) - s_prev2
		s_prev2 = s_prev
		s_prev = s_next

	return (s_prev2 * s_prev2) + (s_prev * s_prev) - (coefficient * s_prev * s_prev2)

def process_frame_queue():
	no_frame_count = 0
	# Terminates after 3 attempts of waiting for new frames
	while no_frame_count < 3:
		while not frame_queue.empty():
			# Resets the counter
			no_frame_count = 0

			window = []

			# Filling up the window till we get 1 symbol length
			while len(window) < SAMPLES_PER_SYMBOL:
				window.append(frame_queue.get())

			window_queue.put(window)

		no_frame_count += 1
		time.sleep(1)

def process_window_queue():
	no_window_count = 0

	# Terminates after 3 attempts of waiting for new window
	while no_window_count < 3:
		while not window_queue.empty():
			# Resetting the counter
			no_window_count = 0

			window = window_queue.get()

			one_count = 0
			zero_count = 0
			for x in xrange(3):

				# Calculate the power of the frequency obtained from the filter
				on_freq_pow = goertzel_filter(window, ONE_FREQUENCY)
				off_freq_pow = goertzel_filter(window, ZERO_FREQUENCY)

				if (on_freq_pow > 1) or (off_freq_pow > 1):
					# print("On power = %f" % on_freq_pow)
					# print("Off power = %f" % off_freq_pow)
					if on_freq_pow > off_freq_pow:
						# print(1)
						one_count +=1
					else:
						# print(0)
						zero_count += 1

			if (one_count > 0) or (zero_count > 0):
				if one_count > zero_count:
					print(1)
				else:
					print(0)

		no_window_count += 1
		time.sleep(1)


def get_frame(frequency, index, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
	"""
	Calculates the frame value at the given frequency and index

	:param frequency: The given frequency at which the frame is
		to be calculated
	:param index: The index of the frame that is to be calculated
	:param rate: The sampling rate
	"""
	time = index / float(rate)

	# y(t) = A * sin(2 * (pi) * f * t)
	y = amplitude * math.sin(2 * math.pi * frequency * time)
	return chr(int(y + TRANSFORMATION))

thread_targets = [process_frame_queue, process_window_queue]

def callback(in_data, frame_count, time_info, status):
	for frame in in_data:
		if not frame_queue.full():
			frame_queue.put_nowait(frame)
	return (None, pyaudio.paContinue)

pya = pyaudio.PyAudio()
stream = pya.open(
	format=pya.get_format_from_width(WIDTH),
	rate=SAMPLE_RATE,
	channels=CHANNELS,
	input=True,
	stream_callback=callback)

try:
	stream.start_stream()

	for target in thread_targets:
		thread = threading.Thread(target=target)
		thread.daemon = True
		thread.start()

	while stream.is_active():
		time.sleep(1)
except KeyboardInterrupt:
	stream.stop_stream()
	stream.close()
	pya.terminate()

	for thread in thread_targets:
		thread.join()


