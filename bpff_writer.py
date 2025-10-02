import bigtree as bt
import pandas as pd
from bigtree import * #
from cryptography.fernet import Fernet

try:
    # create new .bpff file, which we want to write to
    bpffFile1 = "blueprint_sample1.bpff"
    bpff_toWrite = open(bpffFile1, "w")

    sampleData = pd.read_csv("Sample_1.csv")
    header_data = sampleData[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    for column in header_data.columns:
       header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
       bpff_toWrite.write(header_line)

    # tree stuff
    main_branch_IDs = [] # create array to store version IDs of "finalized" nodes
    tree_data = sampleData[['Version Author','Version Date','CommitID','CommitMsg','Last CommitID']]

    print(tree_data)
    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='Last CommitID')
    version_tree.show()

    # TODO fix the fucking tree root node issue
    # TODO check if isMain is True, then add that commitID to main_branch_IDs list
    # TODO create pointer which is initialized to be the most recent entry in the list

    # TODO add supplier data to csv
    # TODO parse supplier data in pandas and use in doubly linked list
    # TODO encrypt into file using fernet
            
except FileNotFoundError: # handles if there is no file found for sample data
    print("There is no such file, please try again")    