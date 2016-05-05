#!/usr/bin/python
##################################################################
#  scorePasswordBatch.py                                        ##
#  This program takes a file containing permuted passwords      ##
#  as an input. Each password must be on a new line. Each       ##
#  password is then permuted and written to a new file with the ##
#  filename scoredResults-year.month.day-hour.minute.second.txt ##
##################################################################
# How to use:                                                   ##
# Run the program from the command line and the program will    ##
# read in a password file. Refer to line 54 to change the       ##
# input file name.                                              ##
# Example:                                                      ##
# ./scorePasswordBatch.py                                       ##
# Note: Make sure to chmod a+x [filename] on your system        ##
# Note: There's an alternative version of this program that     ##
# permutes and only a single password at a time.                ##
##################################################################

# No external libraries are required
import sys
import timeit
import re
import sys
from datetime import date
from operator import mul
from fractions import Fraction
import string
import math
import time

# Time an date stamp to append to the end of the file
## This avoids results filename collision
timestr = time.strftime("%Y%m%d-%H%M%S")

# Write results to an external file
## The file is opened and closed to clear it
now = timestr
tempResultsFile = 'scoredResults-'  + str(now) + '.txt'
resultsFile = open(tempResultsFile, "w")
resultsFile.close()
resultsFile = open(tempResultsFile, "a")

print "Beginning batch processing"

def stringAndStrip(input): 
	input = str(input)
	input =  input.rstrip()
	return input

# Open password file
## This program requires a file named inputFile.txt
## RENAME inputFile.txt TO USE ANOTHER FILE
inputFile = open('inputFile.txt', 'r')

# Calculates n Choose k (n elements in k combinations) 
def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

# Calculate simple password entropy
def calcOrigEnt(input):
	localLengthVar = len(input)
	
	# This is an important line!
	## Change 94 to calculate entropy 
	## for alternative char pool sizes
	mid = 94**localLengthVar
	output = math.log(mid, 2)
	return output

# Calculate the number of lowercase letters in a password
def numberOfLowers(string):
    return sum(1 for c in string if c.islower())

# Calculate the number of uppercase letters in a password
def numberOfUppers(value):
	localLength =len(filter(lambda x: x in string.uppercase, value))
	return localLength

# Calculate the number of digits in a password
def numberOfDigits(value):
	localLength = len([c for c in value if c.isdigit()])
	return localLength

# Calculate the entropy loss due to the usability password transform
def calcLoss(length, upper, lower, digits):
	# Storing and casting local vars
	length = length
	upper = int(upper)
	lower = int(lower)
	digits = int(digits)
	# n Choose k of uppercase chars
	nCkUpper = nCk(length, upper) 
	tempvar1 = length - upper
	# n Choose k of lowercase chars
	nCkLower = nCk(tempvar1, lower)
	tempvar2 = length - upper - lower
	nCkDigits = nCk(tempvar2, digits) 
	intermediateResult = nCkUpper * nCkLower * nCkDigits
	finalResult = math.log(intermediateResult, 2)
	#finalResult = np.log2(intermediateResult)
	return finalResult 

# Subtract the entropy loss from the original entropy
def calcFinalEntropy(originalEntropy, entropyLoss):
	finalResult = originalEntropy - entropyLoss
	return finalResult

# Write header to logfile and screen
print "% 12s % 12s % 12s % 12s % 12s %12s" %("Password", "Length", "Original Entropy", "Entropy Loss", "Final Entropy", "Percentage Loss")
print("\n")
resultsFile.write("% 12s % 12s % 12s % 12s % 12s %12s" %("Password", "Length", "Original Entropy", "Entropy Loss", "Final Entropy", "Percentage Loss"))
resultsFile.write("\n")

# This for loop performs the calculations on every single password
for line in inputFile: 
	
	# Remove whitespaces
	password = stringAndStrip(line)
	length = len(password)
	tempLower = numberOfLowers(password)
	tempUpper = numberOfUppers(password)
	tempDigits = numberOfDigits(password)
	tempSymb = length - tempUpper - tempLower - tempDigits
	originalEntropy = calcOrigEnt(line)
	entropyLoss = calcLoss(length, tempUpper, tempLower, tempDigits)
	newPasswordStrength = calcFinalEntropy(originalEntropy, entropyLoss)
	percentLoss = entropyLoss/originalEntropy*100

#	print(str(password) + "\t" + str(length) + "\t" + str(originalEntropy) + "\t" + str(entropyLoss) + "\t" + str(newPasswordStrength) + "\t" + str(percentLoss))	
	print "% 12s % 12d % 12f % 12f % 12f %12f" %(password, length, originalEntropy, entropyLoss, newPasswordStrength, percentLoss)

	# Log the results to a file with the following format
	# Password, password length, original entropy, entropy loss, permuted entropy, percent loss
#	resultsFile.write(str(password) + "\t" + str(length) + "\t" + str(originalEntropy) + "\t" + str(entropyLoss) + "\t" + str(newPasswordStrength) + "\t" + str(percentLoss))
	resultsFile.write("% 12s % 12d % 12f % 12f % 12f %12f" %(password, length, originalEntropy, entropyLoss, newPasswordStrength, percentLoss))
	resultsFile.write("\n")

print "Processing complete"
print "DISCLAIMER: These measurements are only valid for randomly-generated passwords."
print "They do not apply to passwords created by humans."
print "Please look for a file called " + str(tempResultsFile) + " on your system."

# Closing the file prevents odd behavior
inputFile.close()
resultsFile.close()
