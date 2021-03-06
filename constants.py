import notes

SAMPLE_RATE = 44100
CHANNELS = 1
NUMBER_OF_SECONDS = 5
ONE_FREQUENCY = 19000
ZERO_FREQUENCY = 18000
BYTE_SIZE = 8
WIDTH = 1
WIDTH_BITS = WIDTH * BYTE_SIZE

SAMPLES_PER_SYMBOL = 409
SYMBOL_RATE = SAMPLE_RATE / SAMPLES_PER_SYMBOL

BITS_PER_ASCII = 7
SIZE_OF_START = 8

# The threshold to for determining if it is a
# legit sound or is it just background sound
THRESHOLD = 5000

# When calculating the wave, it is done about the x-axis,
# so there is a need to correct for this transformation
TRANSFORMATION = 2 ** (WIDTH_BITS - 1)
MAX_AMPLITUDE = TRANSFORMATION - 1
