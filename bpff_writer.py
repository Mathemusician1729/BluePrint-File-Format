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
        'isCurrent': bool
    }) # 

    header_data = data[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    # write header to file
    for column in header_data.columns:
        header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
        bpff_toWrite.write(header_line)

    # tree stuff
    tree_data = data[['Version Author','Version Date','CommitID','Last CommitID','CommitMsg','isCurrent']] # parse tree attributes from dataframe
    tree_data["Last CommitID"] = tree_data["Last CommitID"].astype(str).replace('nan', None) # since bigtree requires None to distinguish root node parent, replace 'nan' with None

    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='Last CommitID')

    version_tree_asNewick = tree_to_newick(version_tree, attr_list=['Version Author','Version Date','CommitID','Last CommitID','CommitMsg','isCurrent'])
    bpff_toWrite.write("\nCOMMIT_TREE:\n"+version_tree_asNewick)

    # create pointer to current version
    currentVersionID = tree_data[tree_data["isCurrent"] == True]["CommitID"].values[0]

    # find main branch IDs (EXPLAIN THIS BETTER)
    main_branch_IDs = find_name(version_tree, currentVersionID).path_name.split("/") #
    main_branch_IDs.remove('') # remove empty string at beginning from split

    # write 
    bpff_toWrite.write("\n{main_branch_historyByID=(")
    for id_idx in range(len(main_branch_IDs)-1):
        bpff_toWrite.write(main_branch_IDs[id_idx]+">")
    bpff_toWrite.write(currentVersionID+")")
    bpff_toWrite.write(",current_ID="+currentVersionID+"}")
    
    # TODO parse supplier data in pandas and use in doubly linked list
    supplier_data = data[['Supplier Name','Material','Date Ordered','Contractor Name']].dropna(inplace=True) # get supplier info from dataframe (also drop the NaN columns)

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

# test
write_to_bpff("House_1stFloor_FloorPlan.csv", "tester.bpff")
write_to_bpff("House_3rdFloor_Plumbing.csv", "tester2.bpff")