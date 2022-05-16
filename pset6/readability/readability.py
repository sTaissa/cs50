from cs50 import get_string
import re

# reading the text
t = get_string("Text: ")

# couting sentences
t1 = re.findall('[.?!]', t)
sentences = len(t1)

# counting words
t1 = re.findall("[^\W\d_]+(?:['][^\W\d_]+)*", t)  # finding all alphabetic words
words = len(t1)

# counting letters
t1 = re.findall('\w', str(t1))  # finding all alphabetic letters
letters = len(t1)

# apply teh Coleman-Liau index
l = letters/words*100
s = sentences/words*100
grade = 0.0588 * l - 0.296 * s - 15.8

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade ", round(grade))