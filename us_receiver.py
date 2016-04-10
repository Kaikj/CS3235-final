import pyaudio
import math
import time
import Queue
import threading
from constants import *

# total_frames = SAMPLE_RATE * NUMBER_OF_SECONDS
# current_frames = 0

# frame_queue = Queue.Queue()
# window_queue = Queue.Queue()
# bit_queue = Queue.Queue()

# def goertzel_filter(samples, target):
# 	"""
# 	Applies the Goertzel filter to the set of samples
# 	to see if the target frequency can be found

# 	:param samples: A list of samples collected from the
# 		external environment
# 	:param target: The target frequency to detect in the
# 		samples
# 	"""
# 	k = 0.5 + ((SAMPLES_PER_SYMBOL * target)/SAMPLE_RATE)
# 	w = (2 * math.pi * k) / SAMPLES_PER_SYMBOL
# 	cos_w = math.cos(w)
# 	sin_w = math.sin(w)
# 	coefficient = 2 * cos_w

# 	s_prev = 0.0
# 	s_prev2 = 0.0

# 	for index, sample in enumerate(samples):
# 		hamm_window = ord(sample) * (0.54 - 0.46 * math.cos(2 * math.pi * (index / SAMPLES_PER_SYMBOL)))
# 		s_next = hamm_window + (coefficient * s_prev) - s_prev2
# 		s_prev2 = s_prev
# 		s_prev = s_next

# 	return (s_prev2 * s_prev2) + (s_prev * s_prev) - (coefficient * s_prev * s_prev2)

# def process_frame_queue():
# 	no_frame_count = 0
# 	# Terminates after 3 attempts of waiting for new frames
# 	while True:
# 		while not frame_queue.empty():
# 			# Resets the counter
# 			no_frame_count = 0

# 			window = []

# 			# Filling up the window till we get 1 symbol length
# 			while len(window) < SAMPLES_PER_SYMBOL:
# 				window.append(frame_queue.get())

# 			window_queue.put(window)

# 		no_frame_count += 1
# 		time.sleep(1)

# def process_window_queue():
# 	no_window_count = 0

# 	# Terminates after 3 attempts of waiting for new window
# 	while True:
# 		while not window_queue.empty():
# 			# Resetting the counter
# 			no_window_count = 0

# 			window = window_queue.get()

# 			one_count = 0
# 			zero_count = 0
# 			# Calculate the power of the frequency obtained from the filter
# 			on_freq_pow = goertzel_filter(window, ONE_FREQUENCY)
# 			off_freq_pow = goertzel_filter(window, ZERO_FREQUENCY)


# 			if (on_freq_pow > 5000) or (off_freq_pow > 5000):
# 				# print 1, "is: %d" % on_freq_pow
# 				# print 0, "is: %d" % off_freq_pow
# 				# print

# 				# print("On power = %f" % on_freq_pow)
# 				# print("Off power = %f" % off_freq_pow)
# 				if on_freq_pow > off_freq_pow:
# 					bit_queue.put(1)
# 				else:
# 					bit_queue.put(0)

# 		no_window_count += 1
# 		time.sleep(1)

# def from_binary(bits):
# 	return chr(int(''.join(str(x) for x in bits), 2))

# def process_bit_queue():
# 	while True:
# 		bits = []

# 		while len(bits) < BITS_PER_ASCII:
# 			bit = bit_queue.get()
# 			print bit
# 			bits.append(bit)

# 		print from_binary(bits)


# def get_frame(frequency, index, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
# 	"""
# 	Calculates the frame value at the given frequency and index

# 	:param frequency: The given frequency at which the frame is
# 		to be calculated
# 	:param index: The index of the frame that is to be calculated
# 	:param rate: The sampling rate
# 	"""
# 	time = index / float(rate)

# 	# y(t) = A * sin(2 * (pi) * f * t)
# 	y = amplitude * math.sin(2 * math.pi * frequency * time)
# 	return chr(int(y + TRANSFORMATION))

# thread_targets = [process_frame_queue, process_window_queue, process_bit_queue]

# def callback(in_data, frame_count, time_info, status):
# 	for frame in in_data:
# 		if not frame_queue.full():
# 			frame_queue.put_nowait(frame)
# 	return (None, pyaudio.paContinue)

# pya = pyaudio.PyAudio()
# stream = pya.open(
# 	format=pya.get_format_from_width(WIDTH),
# 	rate=SAMPLE_RATE,
# 	channels=CHANNELS,
# 	input=True,
# 	stream_callback=callback)

# try:
# 	stream.start_stream()

# 	for target in thread_targets:
# 		thread = threading.Thread(target=target)
# 		thread.daemon = True
# 		thread.start()

# 	while stream.is_active():
# 		time.sleep(1)
# except KeyboardInterrupt:
# 	stream.stop_stream()
# 	stream.close()
# 	pya.terminate()

# 	for thread in thread_targets:
# 		thread.join()

class UsReceiver:
	def __init__(self):
		self.thread_targets = [self.process_frame_queue, self.process_window_queue]
		self.threads = []

		self.frame_queue = Queue.Queue()
		self.window_queue = Queue.Queue()
		self.bit_queue = Queue.Queue()

		self.pya = pyaudio.PyAudio()
		self.stream = self.pya.open(
			format=self.pya.get_format_from_width(WIDTH),
			rate=SAMPLE_RATE,
			channels=CHANNELS,
			input=True,
			stream_callback=self.callback)

		# For setting of exit flag
		self.event = threading.Event()

		# Start to process the information in parallel
		for target in self.thread_targets:
			thread = threading.Thread(target=target)
			thread.daemon = False
			thread.start()
			self.threads.append(thread)

	def teardown(self):
		self.stream.stop_stream()
		self.event.set()
		for thread in self.threads:
			thread.join()
		self.stream.close()
		self.pya.terminate()

	def callback(self, in_data, frame_count, time_info, status):
		for frame in in_data:
			if not self.frame_queue.full():
				self.frame_queue.put_nowait(frame)
		return (None, pyaudio.paContinue)

	def get_bits(self, num_bits = 1024):
		"""
		Obtains the number of bits specified and returns it to
		the caller. This method operates on a best effort assumption.
		It will attempt to return as many bits as it can. In the
		event that there is insufficient bits to fill up the buffer,
		all that can be obtained is returned.
		"""
		bits = []
		attempt = 0

		while len(bits) < num_bits:
			if self.bit_queue.empty():
				attempt += 1
				time.sleep(1)
			else:
				attempt = 0
				bits.append(self.bit_queue.get())

			if attempt > 3:
				break
		return bits


	def goertzel_filter(self, samples, target):
		"""
		Applies the Goertzel filter to the set of samples
		to see if the target frequency can be found

		:param samples: A list of samples collected from the
			external environment
		:param target: The target frequency to detect in the
			samples
		"""
		k = 0.5 + ((SAMPLES_PER_SYMBOL * target)/SAMPLE_RATE)
		w = (2 * math.pi * k) / SAMPLES_PER_SYMBOL
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

	def process_frame_queue(self):
		while not self.event.is_set():
			while not self.frame_queue.empty():
				window = []

				# Filling up the window till we get 1 symbol length
				while len(window) < SAMPLES_PER_SYMBOL:
					window.append(self.frame_queue.get())

				self.window_queue.put(window)

			# Sleep for a while to wait for more input
			time.sleep(1)

	def process_window_queue(self):
		while not self.event.is_set():
			while not self.window_queue.empty():
				window = self.window_queue.get()

				# Calculate the power of the frequency obtained from the filter
				on_freq_pow = self.goertzel_filter(window, ONE_FREQUENCY)
				off_freq_pow = self.goertzel_filter(window, ZERO_FREQUENCY)

				# Only process if it is above the threshold. Otherwise it is
				# just background sound
				if (on_freq_pow > THRESHOLD) or (off_freq_pow > THRESHOLD):
					if on_freq_pow > off_freq_pow:
						self.bit_queue.put(1)
					else:
						self.bit_queue.put(0)

			# Sleep until the input arrives
			time.sleep(1)


receiver = UsReceiver()
try:
	while True:
		bits = receiver.get_bits()
		print bits
except KeyboardInterrupt:
	print "Shutting down..."
	receiver.teardown()


