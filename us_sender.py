import pyaudio
import math
import time
import struct
from constants import *

total_frames = SAMPLE_RATE * NUMBER_OF_SECONDS
current_frames = 0
prev_index = 0
text = "hello"
print(' '.join(format(ord(x), 'b') for x in text))

pya = pyaudio.PyAudio()
stream = pya.open(
	format=pya.get_format_from_width(WIDTH),
	rate=SAMPLE_RATE,
	channels=CHANNELS,
	output=True)

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

def get_symbol(frequency, num_samples=SAMPLES_PER_SYMBOL, rate=SAMPLE_RATE, amplitude=MAX_AMPLITUDE):
	global prev_index
	symbol = []
	final_index = num_samples + prev_index
	for index in xrange(prev_index, final_index):
		symbol.append(get_frame(frequency, index, rate, amplitude))
	prev_index = (final_index % SAMPLE_RATE)
	return symbol

def play(buffer):
	stream.write(buffer)

def callback(in_data, frame_count, time_info, status):
	print(in_data)
	return (in_data, pyaudio.paContinue)

stream.start_stream()

# while stream.is_active():
# time.sleep(2)

# for x in xrange(SYMBOL_RATE * NUMBER_OF_SECONDS):
for x in xrange(SYMBOL_RATE):
	for x in xrange(3):
		data = get_symbol(ONE_FREQUENCY)
		# print(data)
		stream.write(''.join(data))
		# stream.write(''.join([struct.pack('h', ord(d)) for d in data]))
		# print(get_frame(ONE_FREQUENCY, x))
		# stream.write(get_frame(ONE_FREQUENCY, x))

# stream.write("https://google.com")

stream.stop_stream()
stream.close()
pya.terminate()


