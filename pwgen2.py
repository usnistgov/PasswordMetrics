import random
import math
import string

charPool  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '<', '>', '?', '/', '{', '[', '}', ']', '|', '$', ':', ';', ',', '.'] 


def makeRandomPassword(length):
	S = ""
	for i in range(length):
		S += random.choice(charPool)
	return S

# If any function returns False, reject the password.  This allows you to apply a list of requirements
# to a password, and reject it if it fails any of them.  We just keep generating random passwords till
# something passes, or some password generating attempt takes too long--then we give up.  
#
# I'm using one of the funny things Python lets you do--you can pass functions around just like they're any
# other kind of variables.  So I can just hand this function a list of functions to execute as needed.  
#
def rejectionSamplePassword(length, list_of_functions):
	# Do this as a for loop to recover from endless loops from unattainable conditions.
	for i in range(100000):
		P = makeRandomPassword(length)
		okay_flag = True
		for f in list_of_functions:
			okay_flag = okay_flag and f(P)
		if okay_flag: return P
	
	raise ValueError, "Got stuck in an infinite loop--you probably have some impossible conditions."

# Put this function in to get no rejections.  
def alwaysPass(P):
	return True

# Require one of each type.
def oneOfEach(P):

	upper_flag = False
	lower_flag = False
	digit_flag = False
	symbol_flag = False

	for ch in P:
		if ch in string.uppercase: 
			upper_flag = True
		elif ch in string.lowercase: 
			lower_flag = True
		elif ch in string.digits:
			digit_flag = True
		else:
			symbol_flag = True

	return upper_flag and lower_flag and digit_flag and symbol_flag


def dontStartWithUppercase(P):

	if P[0] in string.uppercase:
		return False
	else: 
		return True

def dontEndWithPunctuation(P):

	if P[-1] == "." or P[-1] == "?" or P[-1] == "!": 
		return False
	else:
		return True

def generateRuledPassword(length):
	flist = [oneOfEach, dontStartWithUppercase, dontEndWithPunctuation]
	return rejectionSamplePassword(length, flist)
	
# COUNT CHARACTER TYPES
def countCategories(P):

	upper = 0
	lower = 0
	digit = 0
	symbol = 0

	for ch in P:
		if ch in string.uppercase: 
			upper += 1
		elif ch in string.lowercase: 
			lower += 1
		elif ch in string.digits:
			digit += 1
		else:
			symbol += 1

	return upper, lower, digit, symbol

def fact(n):
	P = 1
	for i in range(2,n+1):
		P *= i
	return P

def choose(n,k):
	return fact(n)/ (fact(n-k)*fact(k) )

# Compute how many passwords will map into the same ending password as this one, using Kristen's mapping-down function.
# Note: the count includes this password!
def fanOut(P):
	u,l,d,s = countCategories(P)
	n = len(P)
	
	return choose(n,u) * choose(n-u,l) * choose(n-u-l,d)

# Show fan-out = number of passwords that will map to the same user-friendly password)
def experimentOne(from_length, to_length, trials):
	print "Fan-out By Password Length: How many passwords map to the same user-friendly password?"
	print "% 12s: % 12s % 12s % 12s % 12s" %("length", "P10", "Median", "P90", "Average")
	for L in range(from_length,to_length+1):
		xl = [generateRuledPassword(L) for i in range(trials)]
		results = [fanOut(P) for P in xl]
		results.sort()
		average = sum(results)*1.0/len(results)
		pct_10 = results[int(trials*0.1)]
		median = results[int(trials*0.5)]
		pct_90 = results[int(trials*0.9)]
		print "% 12d: % 12d % 12d % 12d % 12.1f"%(L,pct_10,median,pct_90, average)

# Show entropy loss in bits
def experimentTwo(from_length, to_length, trials):
	print "Entropy Loss By Password Length: How much entropy is lost by mapping to user-friendly password?"
	print "% 12s: % 8s % 8s % 8s % 8s %s" %("length", "P10", "Median", "P90", "Average", "Additional letters")
	for L in range(from_length,to_length+1):
		xl = [generateRuledPassword(L) for i in range(trials)]
		results = [fanOut(P) for P in xl]
		results.sort()
		average = sum(results)*1.0/len(results)
		pct_10 = results[int(trials*0.1)]
		median = results[int(trials*0.5)]
		pct_90 = results[int(trials*0.9)]

		# Based on average fan out, about how many extra lowercase letters are needed to make up for the
		# loss in entropy?
		letters = math.ceil(math.log(average,26))
		print "% 12d: % 8.1f % 8.1f % 8.1f % 8.1f % 8d"%\
			(L,math.log(pct_10,2), math.log(median,2), math.log(pct_90,2), math.log(average,2), letters)