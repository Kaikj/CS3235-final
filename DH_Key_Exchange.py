import math
import us_sender 
import us_receiver

sharedG = int(raw_input('Shared G value: '))
sharedP = int(raw_input('Shared P value: '))
secretA = int(raw_input('Secret A value: '))
secretB = int(raw_input('Secret B value: '))

def computeSentValue(secret, g = sharedG, p = sharedP):
	sharedValue = (g ** secret) % p
	return sharedValue

def computSharedSecret(secret, sharedValue, p = sharedP): 
	sharedKey = (sharedValue ** secret) % p
	return sharedKey

sentValueFromA = computeSentValue(secretA)
sentValueFromB = computeSentValue(secretB)
sharedKeyForA = computSharedSecret(secretA, sentValueFromB)
sharedKeyForB = computSharedSecret(secretB, sentValueFromA)

print(sharedKeyForA)
print(sharedKeyForB)
