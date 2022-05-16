from sys import argv, exit
import csv

#get the input
if len(argv) != 3:
    print('Usage: python dna.py data.csv sequence.txt')
    exit(1)

# open and read the csv file
with open(argv[1], "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    database = []
    for column in reader:
        database.append(column)

# open and read the text file
with open(argv[2], "r") as f:
    file = f.read()

# inititlizing lists to get the bigest repeat
count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
bigest = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for column in range(1, len(database[0])):  # go across the STRs from database
    nsize = 0
    for size in range(0, len(file)):  #go across the dna sequence
        if nsize == size:  # setting the size value of the strings that have already been calculated in the while
            if database[0][column] == file[size:size+len(database[0][column])]:  #verifying if the database matches with dna sequence
                count[column] = 0
                while database[0][column] == file[nsize:nsize+len(database[0][column])]:  #increasing the repeat sequence
                    count[column] += 1
                    if count[column] > bigest[column]:
                        bigest[column] = count[column]
                    nsize += len(database[0][column])  #increasing to the next STR in the sequence
            nsize += 1

# verifying if the STR values matches at someone in database
for column in database:
    i = 1
    match = True
    while match == True and i < len(column):
        if column[i] != str(bigest[i]):
            match = False
        i += 1

    if match == True:
        print(column[0])
        #exit(0)
if match == False:
    print("No match")

print(f"bigest : {bigest[1]},  {bigest[2]},  {bigest[3]}, {bigest[4]}, {bigest[5]}, {bigest[6]}, {bigest[7]}, {bigest[8]}")