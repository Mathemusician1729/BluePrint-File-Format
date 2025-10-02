import bigtree as bt
import pandas as pd
from bigtree import dataframe_to_tree_by_relation
from cryptography.fernet import Fernet

def write_to_bpff(input_filename, output_filename): 
    bpff_toWrite = open(output_filename, "w")

    data = pd.read_csv(input_filename, dtype={
        'Budget Limit': 'Int64',
        'Project ID': 'Int64',
        'CommitID': str,
        'Last CommitID': str
        # TODO add datetime for date columns
    })
    header_data = data[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    # write header to file
    for column in header_data.columns:
        header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
        bpff_toWrite.write(header_line)

    # tree stuff
    main_branch_IDs = [] # create array to store version IDs of "finalized" nodes
    tree_data = data[['Version Author','Version Date','CommitID','Last CommitID','CommitMsg']]
    tree_data["Last CommitID"] = tree_data["Last CommitID"].astype(str).replace('nan', None) # this confounds me

    print(tree_data,"\n")
    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='Last CommitID')
    version_tree.show(attr_list=['Version Author', 'Version Date'])

    # TODO check if isMain is True, then add that commitID to main_branch_IDs list
    # TODO create pointer which is initialized to be the most recent entry in the list

    # TODO add supplier data to csv
    # TODO parse supplier data in pandas and use in doubly linked list
    # TODO encrypt into file using fernet
        
    # TODO create some demo pdfs for the tester

def add_commit(bpffFile, author, date, last_commitID, commitmsg):
    print("hello world")

write_to_bpff("Sample_1.csv", "tester.bpff")