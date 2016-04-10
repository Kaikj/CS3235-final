import pyaudio
import math
import time
from constants import *

class UsSender:
	def __init__(self):
		self.prev_index = 0
		self.pya = pyaudio.PyAudio()
		self.stream = self.pya.open(
			format=self.pya.get_format_from_width(WIDTH),
			rate=SAMPLE_RATE,
			channels=CHANNELS,
			output=True)

	def teardown(self):
		self.stream.close()
		self.pya.terminate()

	def pya_format(self, arr):
		return ''.join(arr)

	def send(self, bits):
		self.stream.start_stream()

		# Repeat the sending so that the receiver has more chance
		# of receiving the sound that is sent
		for i in xrange(3):

			# Pad the start of the payload with 0s so that the
			# receiver knows when the payload starts
			for i in xrange(SIZE_OF_START * BITS_PER_ASCII):
				self.stream.write(self.pya_format(self.get_symbol(ZERO_FREQUENCY)))

			for bit in bits:
				if bit == '1':
					self.stream.write(self.pya_format(self.get_symbol(ONE_FREQUENCY)))
				elif bit == '0':
					self.stream.write(self.pya_format(self.get_symbol(ZERO_FREQUENCY)))


		self.stream.stop_stream()

	def get_symbol(self, frequency, num_samples=SAMPLES_PER_SYMBOL, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
		symbol = []
		final_index = num_samples + self.prev_index
		for index in xrange(self.prev_index, final_index):
			symbol.append(self.get_frame(frequency, index, rate, amplitude))
		prev_index = (final_index % SAMPLE_RATE)
		return symbol

	def get_frame(self, frequency, index, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
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


sender = UsSender()
sender.send(''.join(format(ord(x), 'b') for x in "Hello"))
sender.teardown()