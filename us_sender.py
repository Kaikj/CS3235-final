import pyaudio
import math
import time
from constants import *

class UsSender:
	def __init__(self):
		prev_index = 0

	def setup(self):
		pya = pyaudio.PyAudio()
		stream = pya.open(
			format=pya.get_format_from_width(WIDTH),
			rate=SAMPLE_RATE,
			channels=CHANNELS,
			output=True)

	def teardown(self):
		stream.close()
		pya.terminate

	def pya_format(self, arr):
		return ''.join(arr)

	def send(self, bits):
		stream.start_stream()

		# Repeat the sending so that the receiver has more chance
		# of receiving the sound that is sent
		for i in xrange(3):

			# Pad the start of the payload with 0s so that the
			# receiver knows when the payload starts
			for i in xrange(SIZE_OF_START * BITS_PER_ASCII):
				stream.write(self.pya_format(get_symbol(ZERO_FREQUENCY)))

			for bit in bits:
				if bit == '1':
					stream.write(self.pya_format(get_symbol(ONE_FREQUENCY)))
				elif bit == '0':
					stream.write(self.pya_format(get_symbol(ZERO_FREQUENCY)))


		stream.stop_stream()

	def get_symbol(frequency, num_samples=SAMPLES_PER_SYMBOL, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
		symbol = []
		final_index = num_samples + prev_index
		for index in xrange(prev_index, final_index):
			symbol.append(get_frame(frequency, index, rate, amplitude))
		prev_index = (final_index % SAMPLE_RATE)
		return symbol

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


sender = UsSender()
sender.setup()
sender.teardown()