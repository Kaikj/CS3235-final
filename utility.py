def to_binary(str):
		return ''.join(format(ord(x), 'b') for x in str)

def from_binary(bits):
	return chr(int(bits, 2))