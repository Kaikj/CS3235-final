import pyaudio
import math
import time
import Queue
import threading
from simple_fec import decode
from constants import *

class UsReceiver:
	"""
	This class handles the ultrasonic transmission of data. Using a network
	analogy, it can be thought of as the physical layer. It's only responsibility
	includes receiving the relevant sound waves and converting them into bits
	as necessary. Since frequency modulation is being used, a filter is needed
	to sieve the pre-defined frequencies out.
	"""
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
			thread.daemon = True
			thread.start()
			self.threads.append(thread)

	def teardown(self):
		"""
		Stops processes and threads to allow application
		to shutdown gracefully
		"""
		self.stream.stop_stream()
		self.stream.close()
		self.pya.terminate()

		self.event.set()
		for thread in self.threads:
			thread.join()

	def callback(self, in_data, frame_count, time_info, status):
		"""
		This callback method queues the data obtained from the audio
		module for further processing
		"""
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
		"""
		Processes the queue of frames. Basically just tries to get enough
		frames to form a window before passing it along for further processing.
		"""
		while not self.event.is_set():
			window = []

			# Filling up the window till we get 1 symbol length or give
			# up since there isn't going to be any more
			attempt = 0
			while len(window) < SAMPLES_PER_SYMBOL:
				if self.frame_queue.empty():
					attempt += 1
					time.sleep(1)
				else:
					attempt = 0
					window.append(self.frame_queue.get())

				if attempt > 3:
					break

			# Make do with what we have
			self.window_queue.put(window)

	def process_window_queue(self):
		"""
		Processes the queue of windows. Basically applies the filter to the
		window to see if it is background noise, a 1 bit or a 0 bit.
		"""
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

        def run(self):
            try:
                while True:
                    bits = self.get_bits()
                    bits = decode(bits)
                    output = ''
                    while len(bits) > 0:
                        current = bits[0:4]
                        current = int(current, 2)
                        output = output + str(current)
                        bits = bits[4:]
                    return output
            except KeyboardInterrupt:
                print "Shutting down..."
                self.teardown()


