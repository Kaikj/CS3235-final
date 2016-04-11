import pyaudio
import math
import time
from simple_fec import encode
from constants import *

class UsSender:
	"""
	This class handles the ultrasonic transmission of data. Using a network
	analogy, it can be thought of as the physical layer. It's only responsibility
	includes sending the bits given to it as the relevant sound waves. Since
	frequency modulation is being used, the frequency of the sound produced is
	then dependent on the bit that is passed in
	"""
	def __init__(self):
		self.prev_index = 0
		self.pya = pyaudio.PyAudio()
		self.stream = self.pya.open(
			format=self.pya.get_format_from_width(WIDTH),
			rate=SAMPLE_RATE,
			channels=CHANNELS,
			output=True)

	def teardown(self):
		"""
		Stops processes and threads to allow application
		to shutdown gracefully
		"""
		self.stream.close()
		self.pya.terminate()

	def pya_format(self, arr):
		"""
		Converts the array that defines the amplitude of the sound
		at a particular point into string, which pya prefers
		"""
		return ''.join(arr)

	def send(self, bits):
		"""
		Converts the bits given into the relevant frequencies and send
		them out as sound waves
		"""
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
		"""
		Processes the frequency passed into the function and gives an array of
		changing amplitudes with time to describe the wave to be produced
		"""
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

if  __name__ == "__main__":
	sender = UsSender()
	message = ''.join(format(ord(x), 'b') for x in "Hello")
	message = encode(message)
	sender.send(message)
	sender.teardown()
