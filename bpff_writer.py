import pandas as pd
from bigtree import *
from cryptography.fernet import Fernet

def write_to_bpff(input_filename, output_filename): 
    bpff_toWrite = open(output_filename, "w")

    data = pd.read_csv(input_filename, dtype={
        'Budget Limit': 'Int64',
        'Project ID': 'Int64',
        'CommitID': str,
        'Last CommitID': str,
        'isMain': bool
    }) # 

    header_data = data[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    # write header to file
    for column in header_data.columns:
        header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
        bpff_toWrite.write(header_line)

    # tree stuff
    main_branch_IDs = [] # create array to store version IDs of "finalized" nodes
    tree_data = data[['Version Author','Version Date','CommitID','Last CommitID','CommitMsg','isMain']] # parse tree attributes from dataframe
    tree_data["Last CommitID"] = tree_data["Last CommitID"].astype(str).replace('nan', None) # this confounds me

    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='Last CommitID')

    version_tree_asNewick = tree_to_newick(version_tree, attr_list=['Version Author','Version Date','CommitID','Last CommitID','CommitMsg','isMain'])
    bpff_toWrite.write("\nCOMMIT_TREE:\n"+version_tree_asNewick)

    # check if isMain is True, then add that commitID to main_branch_IDs list
    for i, row in tree_data.iterrows(): # TODO Might change to tree traversal if needed
        if row['isMain']:
            main_branch_IDs.append(row['CommitID'])
        
    # create pointer which is the most recent entry in the list
    currentVersionID = main_branch_IDs[-1]
    
    # write 
    bpff_toWrite.write("\n{main_branch_history=(")
    for id_idx in range(len(main_branch_IDs)-1):
        bpff_toWrite.write(main_branch_IDs[id_idx]+">")
    bpff_toWrite.write(currentVersionID+")")
    bpff_toWrite.write(",current_ID="+currentVersionID+"}")
    
    # TODO parse supplier data in pandas and use in doubly linked list
    supplier_data = data[['Supplier Name','Material','Date Ordered','Contractor Name']].drop([4,5,6,7]) # get supplier info from dataframe (also drop the NaN columns)

    # Create Doubly Linked List class in Python
    class Node:
        def __init__(self, nextNode, prevNode, data):
            self.nextNode = None
            self.prevNode = None
            self.data = data
    
    def insertNode():
        print("hellow World")

    # Fernet Encryption to File:
    suppliers_key = Fernet.generate_key()

    # write to .bpff file
    bpff_toWrite.write("\nSUPPLIERS:")

    # TODO encrypt into file using fernet
        
    # TODO create some demo pdfs for the tester
    # TODO determine how to make pointers to pdfs

    # TODO implement checksum for footer

    # Footer stuffs:

    # close file after writing
    bpff_toWrite.close() 

def add_version(bpffFile, author, date, last_commitID, commitmsg): # TODO work on add version which will add a new update to the git log
    version_node = Node()

def revert(bpffFile, revertVersionID): # TODO work on revert function which will revert to a previous main branch
    print("hello world") 

write_to_bpff("House_1stFloor_FloorPlan.csv", "tester.bpff")