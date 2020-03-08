# import the necessary packages
import numpy as np
import cv2


def dhash(image, hashSize=8):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    resized = cv2.resize(gray, (hashSize + 1, hashSize))

    diff = resized[:, 1:] > resized[:, :-1]

    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def convert_hash(h):

	return int(np.array(h, dtype="float64"))

def hamming(a, b):

	return bin(int(a) ^ int(b)).count("1")