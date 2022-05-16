from sys import argv, exit
import cs50

# make link to sqlite
students = cs50.SQL("sqlite:///students.db")

# get the input
if len(argv) != 2:
    print('Usage: python roster.py house')
    exit(1)

# get the data asked for
db = students.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])

# check if the middle name is null and print
for row in db:
    if row['middle'] != None:
        print(f"{row['first']} {row['middle']} {row['last']}, born {str(row['birth'])}")
    else:
        print(f"{row['first']} {row['last']}, born {str(row['birth'])}")