import sys

# if (len(sys.argv)) != 3:
#     print("Usage: python3 compute_inverse.py <a> <m>")
#     sys.exit(1)

a = int(input())
m = int(input())

print("SPIM Version 8.0 of January 8, 2010")
print("Copyright 1990-2010, James R. Larus.")
print("All Rights Reserved.")
print("See the file README for a full copyright notice.")
print("Loaded: /usr/lib/spim/exceptions.s")
print(pow(a,-1,m))