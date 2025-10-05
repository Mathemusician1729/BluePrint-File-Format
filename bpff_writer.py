import pandas as pd # 
from bigtree import * # import bigtree for working with tree structures
import hashlib # import hashlib for creating sha256 checksum of file footer 

def write_to_bpff(input_filename, output_filename): 
    bpff_toWrite = open(output_filename, "w")

    # 
    data = pd.read_csv(input_filename, dtype={ 
        'Budget Limit': 'Int64',
        'Project ID': 'Int64',
        'CommitID': str,
        'LastCommitID': str,
        'isCurrent': bool
    }) 

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
    bpff_read = open(bpffFile, "r") # open specified .bpff file in read mode
    bpff_contents = [] # initialize empty array to store lines
    for line in bpff_read:
        if line.startswith("checksum-sha256:"): 
            break
        bpff_contents.append(line)

    for i in range(len(bpff_contents)):
        bpff_contents[i] = bpff_contents[i].replace('\n','')

    bpff_read.close()
    return bpff_contents

# Additional functions that address the modifiability of .bpff files
# AddVersion: adds new version to the version tree
def addVersion(bpffFile, author, date, commitmsg, current): 
    bpff_contents = getbpffcontents(bpffFile) #  get current .bpff contents 
    tree = newick_to_tree(bpff_contents[bpff_contents.index('COMMIT_TREE:')+1])
    currentNode = find_attr(tree, "isCurrent", "True") # find current node in tree (https://bigtree.readthedocs.io/stable/bigtree/tree/search/#bigtree.tree.search.find_attr)

    Nodes = list(tree.descendants) # get list of all nodes in tree (https://bigtree.readthedocs.io/stable/bigtree/node/basenode/#bigtree.node.basenode.BaseNode.descendants) 
    latestID = max([int(node.node_name) for node in Nodes]) # find latest ID by converting all node names to integers and finding max (which will be the most recent)

    newNodeID = str(int(latestID)+1).zfill(3) # new node ID is current ID + 1, using zfill to ensure leading 0s (https://www.w3schools.com/python/ref_string_zfill.asp)
    newNode = Node(newNodeID, VersionAuthor=author, VersionDate=date, CommitMsg=commitmsg, isCurrent=current, parent=currentNode) # create new node with added information https://bigtree.readthedocs.io/stable/bigtree/node/node/

    if current == True: # we set the pointer for current version to the new node, so we need to set the old current node to False
        currentNode.isCurrent = False 

    with open(bpffFile, "w") as f: # write new tree back to file
        # write header data back to file
        for line in bpff_contents[:bpff_contents.index('COMMIT_TREE:')+1]:
            f.write(line + "\n")

        # update newick string in file contents
        treeBacktoNewick = tree_to_newick(tree, attr_list=['VersionAuthor','VersionDate','CommitID','LastCommitID','CommitMsg','isCurrent'])
        bpff_contents[bpff_contents.index('COMMIT_TREE:')+1] = treeBacktoNewick
        f.write(treeBacktoNewick + "\n")

        # update main branch history + current ID in file contents
        # extract current history list from file contents
        versionData = bpff_contents[bpff_contents.index('COMMIT_TREE:')+2].split(",") 
        history_list = versionData[0].strip("{main_branch_historyByID=()").split(">")

        history_list.append(newNodeID) # add new node ID to end of history list
        history_list = ">".join(history_list) # convert back to string with '>' separating IDs (from previous format) ht

        f.write("{main_branch_historyByID=(" + history_list + ")," + "current_ID=" + newNodeID + "}\n") # write updated verison history and current ID back to file
    f.close() # close file after writing

    # rewrite checksum footer
    with open(bpffFile, "rb") as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest() # create sha256 checksum of file
    
    # append checksum to end of file
    with open(bpffFile, "a") as bpff_appendFooter:
        bpff_appendFooter.write("\nchecksum-sha256:\n" + digest)
    bpff_appendFooter.close() # close file final

# Revert: reverts to a previous version in the main branch
def revert(bpffFile, revertVersionID): # TODO work on revert function which will revert to a previous main branch
    bpff_contents = getbpffcontents(bpffFile)
    tree = newick_to_tree(bpff_contents[bpff_contents.index('COMMIT_TREE:')+1])

# test
write_to_bpff("House_3rdFloor_Plumbing.csv", "tester2.bpff")
addVersion("poop2.bpff", "Matthew", "10/31/2025", "Added new door to floor plan", True)