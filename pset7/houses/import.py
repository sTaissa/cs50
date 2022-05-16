from sys import argv, exit
import csv
import cs50

# make link with the sqlite
students = cs50.SQL("sqlite:///students.db")

# get the input
if len(argv) != 2:
    print('Usage: python import.py characters.csv')
    exit(1)

# open and read the CSV file
with open(argv[1], "r") as chara:
    reader = csv.DictReader(chara, delimiter=",")

    for row in reader:
        name = row['name'].split()
        first, middle, last = name[0], name[1] if len(name) == 3 else None, name[-1]
        house = row['house']
        birth = row['birth']

        students.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)", first, middle, last, house, int(birth))
