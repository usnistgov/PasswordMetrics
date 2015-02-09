#!/usr/bin/python
##############################################################
## This program takes a string as input (a password) and    ##
##  permutes the password.				    				##
##############################################################
# How to use: ./programName.py [password_string]            ##
# Example: ./transform.py ABCabc123!!!                      ##
# Note: Ensure the #!/location/to/python is correct		    ## 
# Note: Make sure to chmod a+x [filename] on your system 	## 
# Note: Some characters such as the ' and ; interact with   ##
# the shell and don't permute properly.	 Passing it in as   ##
# a file containing the password makes it perform better    ##
##############################################################

import sys
import timeit
import re

# take in an argument from the command line 
password = sys.argv[1]

# Create arrays to hold characters
lowerArray = []
upperArray = []
digitArray = []
symbolArray = []

# This is the heart of the script
##  Runs through each character of a string and
##  places it into an array  
def charSwap(text):
	upper = lower = digit = space = 0
	for c in text:
		if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        upper += 1
                        upperArray.append(c)
		elif c in "abcdefghijklmnopqrstuvwxyz":
			lower += 1
			lowerArray.append(c)
		elif c in "0123456789":
			digit += 1
			digitArray.append(c)
		else : 
			symbolArray.append(c)
	return (upper, lower, digit, space)

# Call the primary function
charSwap(str(password))

# .join merges characters from an array into a string 
tempUpperPass = ''.join(upperArray)
tempLowerPass = ''.join(lowerArray)
tempDigitPass = ''.join(digitArray)
tempSymbolPass = ''.join(symbolArray)

# Concatenate all the strings
newPass = tempUpperPass + tempLowerPass + tempDigitPass + tempSymbolPass

# print result
print newPass

