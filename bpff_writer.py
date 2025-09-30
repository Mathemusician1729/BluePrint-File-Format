import bigtree as bt
import csv

try:
    # create new .bpff file, which we want to write to
    bpffFile1 = "blueprint_sample1.bpff"
    bpff_toWrite = open(bpffFile1, "w")

    Sample1_asArray = [] # create array to store contents of file

    # open sample data (csv) and append contents into array
    with open("Sample_1.csv", "r") as Sample1: 
        line = csv.reader(Sample1, delimiter=',')
        for col in line:
            Sample1_asArray.append(col)

    # Writing header contents to bpff file, given by the first 2 rows and the first 5 columns (up until "Est. Date of Completion") in the csv
    for i in range(Sample1_asArray[0].index("Est. Date of Completion")+1):
        header_line = Sample1_asArray[0][i] + ": " + Sample1_asArray[1][i] + "\n"
        bpff_toWrite.write(header_line)

    # tree stuff
    current_version = "001" # pointer to current version ID, starts at first commit possible
    

except FileNotFoundError: # handles if there is no file found for sample data
    print("There is no such file, please try again")