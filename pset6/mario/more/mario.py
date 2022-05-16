from cs50 import get_int

# input validation
while True:
    n = get_int("Height: ")
    if n <= 8 and n > 0: #between 1 and 8
        break

for row in range(n):
    for space in range(n-row, 1, -1): # make the first spaces
        print(" ", end="")
    for hash1 in range(row+1): # make the first pyramid
        print("#", end="")
    print("  ", end="") #make the gap between the pyramids
    for hash2 in range(row+1): #finishing the pirymid
        print("#", end="")
    print()