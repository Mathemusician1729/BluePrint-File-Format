import pandas as pd # 
from bigtree import * #
from cryptography.fernet import Fernet #
import hashlib # 

def write_to_bpff(input_filename, output_filename): 
    bpff_toWrite = open(output_filename, "w")

    data = pd.read_csv(input_filename, dtype={
        'Budget Limit': 'Int64',
        'Project ID': 'Int64',
        'CommitID': str,
        'LastCommitID': str,
        'isCurrent': bool
    }) # 

    header_data = data[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    # write header to file
    for column in header_data.columns:
        header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
        bpff_toWrite.write(header_line)

    # tree stuff
    tree_data = data[['VersionAuthor','VersionDate','CommitID','LastCommitID','CommitMsg','isCurrent']] # parse tree attributes from dataframe
    tree_data["LastCommitID"] = tree_data["LastCommitID"].astype(str).replace('nan', None) # since bigtree requires None to distinguish root node parent, replace 'nan' with None

    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='LastCommitID') # create tree from the tree_data dataframe (https://bigtree.readthedocs.io/stable/bigtree/tree/construct/#bigtree.tree.construct.dataframe_to_tree_by_relation)

    version_tree_asNewick = tree_to_newick(version_tree, attr_list=['VersionAuthor','VersionDate','CommitID','LastCommitID','CommitMsg','isCurrent'])
    bpff_toWrite.write("\nCOMMIT_TREE:\n"+version_tree_asNewick)

    # create pointer to current version
    currentVersionID = find_attr(version_tree, "isCurrent", True).node_name

    # find main branch IDs (EXPLAIN THIS BETTER)
    main_branch_IDs = find_name(version_tree, currentVersionID).path_name.split("/") #
    main_branch_IDs.remove('') # remove empty string at beginning from split

    # write 
    bpff_toWrite.write("\n{main_branch_historyByID=(")
    for id_idx in range(len(main_branch_IDs)-1):
        bpff_toWrite.write(main_branch_IDs[id_idx]+">")
    bpff_toWrite.write(currentVersionID+")")
    bpff_toWrite.write(",current_ID="+currentVersionID+"}")

    # close file after writing main data 
    bpff_toWrite.close() 

    # Write footer with checksum
    with open(output_filename, "rb") as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest() # create sha256 checksum of file
    
    # append checksum to end of file
    with open(output_filename, "a") as bpff_appendFooter:
        bpff_appendFooter.write("\n\nchecksum-sha256:\n" + digest)

    bpff_appendFooter.close() # close file final

# Helper function to get .bpff contents as array of strings for modifier functions
def getbpffcontents(bpffFile): 
    bpff_read = open(bpffFile, "r")
    bpff_contents = bpff_read.readlines()
    for i in range(len(bpff_contents)):
        bpff_contents[i] = bpff_contents[i].replace('\n','')
    bpff_read.close()
    return bpff_contents

# Additional functions that address the modifiability of .bpff files
def addVersion(bpffFile, author, date, commitmsg): 
    bpff_contents = getbpffcontents(bpffFile)

    tree = newick_to_tree(bpff_contents[bpff_contents.index('COMMIT_TREE:')+1])
    currentNode = find_attr(tree, "isCurrent", "True")
    currentNodeID = currentNode.node_name 

    newNodeID = str(int(currentNodeID)+1).zfill(3) # new node ID is current ID + 1, padded with leading zeros to ensure 3 digits (https://www.w3schools.com/python/ref_string_zfill.asp)
    newNode = Node(newNodeID, VersionAuthor=author, VersionDate=date, CommitMsg=commitmsg, parent=currentNode) # https://bigtree.readthedocs.io/stable/bigtree/node/node/

    with open(bpffFile, "w") as f:
        print('hello world')
        
    f.close()

def revert(bpffFile, revertVersionID): # TODO work on revert function which will revert to a previous main branch
    bpff_contents = getbpffcontents(bpffFile)

# test
write_to_bpff("House_1stFloor_FloorPlan.csv", "tester.bpff")
#addVersion("tester.bpff", "Matthew", "2024-06-10", "Added new door to floor plan")