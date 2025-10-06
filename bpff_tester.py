# import reader and writer modules to test (https://www.geeksforgeeks.org/python/how-to-import-other-python-files/)
import bpff_reader 
import bpff_writer

# get sample data csv file names
bpff_Sample1 = "House_1stFloor_FloorPlan.csv"
bpff_Sample2 = "House_3rdFloor_Plumbing.csv"

# names for output files (.bpff - will be created if they do not exist)
bpffFile1 = "blueprint_sample1.bpff"
bpffFile2 = "blueprint_sample2.bpff"

try:
    # test writer (creates .bpff files from csv data)
    bpff_writer.write_to_bpff(bpff_Sample1,bpffFile1) # write csv sample 1 to .bpff file
    bpff_writer.write_to_bpff(bpff_Sample2,bpffFile2) # write csv sample 2 to .bpff file

    # test reader (reads and prints .bpff file contents)
    print("Read .bpff File 1:")
    bpff_reader.read_bpff(bpffFile1) # read and print .bpff file 1 contents

    print("\n--------------------\nRead .bpff File 2:")
    bpff_reader.read_bpff(bpffFile2) # read and print .bpff file 2 contents

    # test file modifiability 
    # get file names for testing revert and add
    revertFile1 = "blueprint1_testRevert.bpff"
    revertFile2 = "blueprint2_testRevert.bpff"

    addCommitFile1 = "blueprint1_testAdd.bpff"
    addCommitFile2 = "blueprint2_testAdd.bpff"

    # test addVersion - adds new version commit to the current version control tree, with the option of setting as current/main version
    bpff_writer.addCommit(bpffFile1, "Matthew", "10/20/2025", "Added stairway to floor 3", False, addCommitFile1) # add new commit to .bpff file 1 
    bpff_writer.addCommit(bpffFile2, "John", "10/20/2025", "updated all measurement sizes as per new regulations from manager", True, addCommitFile2) # add new commit to .bpff file 2 and push commit as current version

    # test revert - reverts to a previous version in the main branch
    bpff_writer.revert(bpffFile1, "003", revertFile1) # revert .bpff file 1 to version with ID "003"
    bpff_writer.revert(bpffFile2, "007", revertFile2) # revert .bpff file 2 to version with ID "007"

    # read and print modified files to show changes
    print("\n--------------------\nRead .bpff File 1 (after addCommit):")
    bpff_reader.read_bpff(addCommitFile1)
    print("\n--------------------\nRead .bpff File 2 (after addCommit):")
    bpff_reader.read_bpff(addCommitFile2)

    print("\n--------------------\nRead .bpff File 1 (after reversions):")
    bpff_reader.read_bpff(revertFile1)
    print("\n--------------------\nRead .bpff File 2 (after reversions):")
    bpff_reader.read_bpff(revertFile2)

except FileNotFoundError: # handles any missing file errors
    print("There is no such file, please try again")  