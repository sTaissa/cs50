from cs50 import get_string
import re

n = get_string("Number: ") # get the number as a string
size = len(n)

sum1 = 0

if size != 13 and size != 15 and size != 16: # verify if it is a card size
    print("INVALID")

# Luhn's algorithm
for i in range(size-2, -1, -2):
    cc = int(n[i]) * 2

    # if the product has two digits, divide them to sum
    if cc > 9:
        while cc > 0:
            digit = cc % 10
            sum1 += digit
            cc //= 10
    else:
        sum1 += cc

for i in range(size-1, -1, -2):
    sum1 += int(n[i])

if sum1 % 10 == 0:
    # check which card is
    if re.search('^3[47][0-9]{13}$', n):
        print("AMEX")
    elif re.search('^5[1-5][0-9]{14}$', n):
        print("MASTERCARD")
    elif re.search('^4[0-9]{12}([0-9]{3})?$', n):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")