#!/usr/bin/python
##################################################################
##  permuteAndScorePassword.py					##
##  This program takes a string as input (a password) and       ##
##  permutes the password. It then calculates the difference    ##
##  of the original entropy and entropy loss due to the 	##
##  usability transform. 				 	##
##################################################################
# How to use:							##
# Run the program from the command line and the program will    ##
# then prompt the user for a password.		                ##
# Example:							## 
# ./permuteAndScorePassword.py			                ##
# Please type a password > T3sTP@$$w0rd	                        ##
# Note: Make sure to chmod a+x [filename] on your system        ## 
# Note: There's an alternative version of this program that	## 
# uses a list of passwords as its input, allowing for batch	##
# processing of large lists of passwords.			##
##################################################################

# No external libraries are required
import sys
from datetime import date
from operator import mul 
from fractions import Fraction
import string 
import math
import time

# take in an argument from the command line 
password = raw_input( 'Please type a password: ' )

# Create arrays to hold characters
lowerArray = []
upperArray = []
digitArray = []
symbolArray = []

# This is the heart of the script
##  Runs through each character of a string and
##  places it into an array
def charSwap(text):
        upper = lower = digit = symbols = 0
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
        return (upper, lower, digit, symbols)

# Call the primary function
charSwap(str(password))

# .join merges characters from an array into a string
tempUpperPass = ''.join(upperArray)
tempLowerPass = ''.join(lowerArray)
tempDigitPass = ''.join(digitArray)
tempSymbolPass = ''.join(symbolArray)

# Concatenate all the strings
permutedPassword = tempUpperPass + tempLowerPass + tempDigitPass + tempSymbolPass

# Calculates n Choose k (n elements in k combinations) 
def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

# Calculate simple password entropy
def calcOrigEnt(input):
	localLengthVar = len(input)
	
	## This line defines the character pool size.
	## Change 94 to a different number 
	## for alternative char pool sizes.
	mid = 94**localLengthVar
	output = math.log(mid, 2)
	return output

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
def calcFinalEnt(originalEntropy, entropyLoss):
        finalResult = originalEntropy - entropyLoss
        return finalResult

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

# Define temporary variables used in calculation
tempDiff = 0 
tempLoss = 0 

# Remove any pesky \r and \n, aka white spaces
## (Likley redundant at this point, just being safe)
password = password.rstrip()

# Performing entropy loss calculations
length = len(password)
tempLower = str(numberOfLowers(password))
tempUpper = str(numberOfUppers(password))
tempDigits = str(numberOfDigits(password))
originalEntropy = calcOrigEnt(password)
tempLoss = calcLoss(length, tempUpper, tempLower, tempDigits)
newPasswordStrength = calcFinalEnt(originalEntropy, tempLoss)
tempDiff = tempLoss/originalEntropy
percentLoss = tempDiff*100

# Print the results
print "Original password: " + str(password)  
print "Permuted password: " + str(permutedPassword)
print "Original entropy : " + str(originalEntropy)
print "Entropy loss     : " + str(tempLoss)
print "Permuted entropy : " + str(newPasswordStrength)
print "Percentage loss  : " + str(percentLoss) + str(' %')

print "DISCLAIMER: These measurements are only valid for randomly-generated passwords."
print "They do not apply to passwords created by humans."
