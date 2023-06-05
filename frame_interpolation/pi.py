# The probability that two integers are coprime is 6 / pi^2
# 	x = 6/pi^2
#	pi = sqrt(6/x)
# --- 
#	we generate a series of random integers
#   test for coprimality
#   and collect the results to calculate the probability x


import random
import math

def gcd(a,b): 
    if(b==0): 
        return a 
    else: 
        return gcd(b,a%b) 

# The maximum value for our integer pairs
max_val = 1000000
# The number of pairs to test for coprimality
pairs = 10000

cofactors_tally = 0.0
coprimes_tally = 0.0
  
# Generate random pairs of integers, test them for coprimality
for i in range(pairs):
	a = random.randint(1, max_val)
	b = random.randint(1, max_val)
	if gcd(a, b) == 1: coprimes_tally += 1
	else: cofactors_tally += 1

print ("Coprimes:   ", coprimes_tally)
print ("Cofactors:  ", cofactors_tally)
print ("--")

# The probability based on our tests. 
P = coprimes_tally / pairs
print ("Probability:", P)

# estimate pi 
pi = math.sqrt(6.0/P)

print (pi)