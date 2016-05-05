#!/usr/bin/python
##################################################################
#  permutePasswordBatch.py  					##
#  This program takes a file containing passwords as an input.  ## 
#  Each password must be on a new line. Each password is        ##
#  then permuted and written to a new file with the filename    ##
#  permutedResults-year.month.day-hour.minute.second.txt        ##
##################################################################
# How to use:							##
# Run the program from the command line and the program will    ##
# read in a password file. Refer to line 49 to change the       ## 
# input file name.   			                        ##
# Example:							## 
# ./permutePasswordBatch.py	                                ##
# Note: Make sure to chmod a+x [filename] on your system        ## 
# Note: There's an alternative version of this program that	## 
# permutes only a single password at a time. 			##
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
tempResultsFile = 'permutedResults-'  + str(now) + '.txt'
resultsFile = open(tempResultsFile, "w")
resultsFile.close()
resultsFile = open(tempResultsFile, "a")

print "Beginning batch processing" 

# Open password file
## This program requires a file named inputFile.txt
## RENAME inputFile.txt TO USE ANOTHER FILE
inputFile = open('inputFile.txt', 'r')

# This function begins the permutation
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

# Permute each line in the inputFile
for line in inputFile:
        # Defining and reinitializing arrays
	lowerArray = []
        upperArray = []
        digitArray = []
        symbolArray = []

        # Call the primary function
        charSwap(str(line))

        # .join merges characters from an array into a string
        tempUpperPass = ''.join(upperArray)
        tempLowerPass = ''.join(lowerArray)
        tempDigitPass = ''.join(digitArray)
        tempSymbolPass = ''.join(symbolArray)

        # Concatenate all the strings
        newPass = tempUpperPass + tempLowerPass + tempDigitPass + tempSymbolPass

        resultsFile.write(str(newPass))

print "Processing complete"
print "DISCLAIMER: These measurements are only valid for randomly-generated passwords."
print "They do not apply to passwords created by humans."
print "Please look for a file called " + str(tempResultsFile) + " on your system."

# Closing the file prevents odd behavior 
inputFile.close()
resultsFile.close()
