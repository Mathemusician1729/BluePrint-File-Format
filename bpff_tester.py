import bpff_reader 
import bpff_writer

# get sample data csv files (names)
bpff_Sample1 = "Sample_1.csv"
bpff_Sample2 = "Sample_2.csv"

# names for output files
bpffFile1 = "blueprint_sample1.bpff"
bpffFile2 = "blueprint_sample2.bpff"

try:
    bpff_writer.write_to_bpff(bpff_Sample1, bpffFile1)
    #bpff_writer.write_to_bpff(bpff_Sample2,bpffFile2)

    # test reader
    bpff_reader.read_bpff(bpffFile1)
    bpff_reader.read_bpff(bpffFile2)

    # test add
    #bpff_writer.add_commit(bpffFile1, "Matthew", )

except FileNotFoundError: # handles any missing file errors
    print("There is no such file, please try again")  