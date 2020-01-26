#!/usr/bin/env python 
#RMS 2020 

from Hopfield import HopfieldWord

def main():

	inputword = str(input("Provide target word: "))
	print("\nTARGET: %s provided\n" %inputword)

	model = HopfieldWord(inputword)

	inputstart = str(input("Provide target word: "))
	print("\nSTARTING: %s provided\n" %inputstart)

	output, Evec, Ediffvec = model.predict(inputstart)

	print("\nOUTPUT: %s\n" %output)

if __name__ == "__main__":

	main()

