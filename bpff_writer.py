import pandas as pd # import pandas to easily process csv sample data 
from bigtree import * # import bigtree for working with tree structures
import hashlib # import hashlib for creating sha256 checksum of file footer 

# writer function -- creates and writes to .bpff file from csv sample data
def write_to_bpff(input_filename, output_filename):
    bpff_toWrite = open(output_filename, "w") # open .bpff file in write mode (creates file if it does not exist)

    # create dataframe from csv file, data types specified for certain columns to ensure correct parsing (from https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html, https://www.statology.org/pandas-read-csv-dtype/)
    data = pd.read_csv(input_filename, dtype={ 
        'Budget Limit': 'Int64', # budget limit is stored as an integer
        'Project ID': 'Int64', # project ID is stored as an integer
        'CommitID': str, # commit IDs are strings (to allow for leading 0s)
        'LastCommitID': str, # last commit IDs are strings (to allow for leading 0s)
        'isCurrent': bool # isCurrent is either True or False
    }) 

    # get header data from dataframe (from columns in header)
    header_data = data[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    # write header data to file
    for column in header_data.columns:
        header_line = column + ": " +  str(header_data.loc[0,column]) + "\n" # get value from first row for each column (this is where header metadata is stored in csv)
        bpff_toWrite.write(header_line)

    # get version history data from csv 
    tree_data = data[['VersionAuthor','VersionDate','CommitID','LastCommitID','CommitMsg','isCurrent']] # parse tree attributes from dataframe
    tree_data["LastCommitID"] = tree_data["LastCommitID"].astype(str).replace('nan', None) # since bigtree requires None to distinguish root node parent, replace 'nan' with None

    # write version history data into tree using bigTree's dataframe to tree, where each node stores author, date, commit ID, last commit ID, commit message, and whether it is the current version
    # specifies the columns to be commmit IDs to use for child and parent relationships (parent by what was the last commitID, and child being the current commitID)
    # (https://bigtree.readthedocs.io/stable/bigtree/tree/construct/#bigtree.tree.construct.dataframe_to_tree_by_relation)
    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='CommitID', parent_col='LastCommitID') # create tree from the tree_data dataframe (https://bigtree.readthedocs.io/stable/bigtree/tree/construct/#bigtree.tree.construct.dataframe_to_tree_by_relation)

    # convert tree to newick representation, which provides for easier storage in file
    # (https://bigtree.readthedocs.io/stable/bigtree/tree/export/#bigtree.tree.export.tree_to_newick)
    version_tree_asNewick = tree_to_newick(version_tree, attr_list=['VersionAuthor','VersionDate','CommitID','LastCommitID','CommitMsg','isCurrent'])
    bpff_toWrite.write("\nCOMMIT_TREE:\n"+version_tree_asNewick) # write newick string representation of the tree to file

    # create pointer variable to the ID of the current version by finding the node which has isCurrent = True (https://bigtree.readthedocs.io/stable/bigtree/tree/search/#bigtree.tree.search.find_attr)
    currentVersionID = find_attr(version_tree, "isCurrent", True).node_name

    # modification: file will also store a "history list" of all IDs that are part of the "main" branch (the path from root to current version node)
    # (https://bigtree.readthedocs.io/stable/bigtree/tree/search/#bigtree.tree.search.find_name)
    main_branch_IDs = find_name(version_tree, currentVersionID).path_name.split("/") # find the ID sequence which is path from root to current version node (main branch history)
    main_branch_IDs.remove('') # remove empty string at beginning from split

    # write pointer and main branch history to file
    bpff_toWrite.write("\n{main_branch_historyByID=(")

    # write each ID in main branch history list to file, separated by '>' (except for last ID)
    for id_idx in range(len(main_branch_IDs)-1): 
        bpff_toWrite.write(main_branch_IDs[id_idx]+">")
    bpff_toWrite.write(currentVersionID+")") 

    # write pointer to current version ID
    bpff_toWrite.write(",current_ID="+currentVersionID+"}") 

    # close file after writing the main data, has to be done before writing footer to ensure checksum isn't applied to empty file
    bpff_toWrite.close() 

    # Write footer with checksum
    with open(output_filename, "rb") as f: # open in binary reading mode to create checksum
        digest = hashlib.file_digest(f, 'sha256').hexdigest() # create checksum for file with hashlib (https://docs.python.org/3/library/hashlib.html)
    
    # append checksum to end of file
    with open(output_filename, "a") as bpff_appendFooter:
        bpff_appendFooter.write("\n\nchecksum-val:\n" + digest)

    # close file after appending footer
    bpff_appendFooter.close() 

# Helper function to get .bpff contents as array of strings for modifier functions
def getbpffcontents(bpffFile): 
    bpff_read = open(bpffFile, "r") # open specified .bpff file in read mode
    bpff_contents = [] # initialize empty array to store lines
    for line in bpff_read: # read each line in file and append to contents up until checksum footer (since checksum will change if file is modified)
        if line.startswith("checksum-val:"): 
            break
        bpff_contents.append(line) 

    for i in range(len(bpff_contents)): # since each line ends with '\n' for newline from file, remove \n for the array contents
        bpff_contents[i] = bpff_contents[i].replace('\n','')

    bpff_read.close() # close file after reading
    return bpff_contents # return array of strings representing file contents

# Additional functions that address the modifiability of .bpff files
# AddVersion: adds new version to the version tree, with option of setting that version as current/main version
def addCommit(bpffFile, author, date, commitmsg, current, outputFile): 
    bpff_contents = getbpffcontents(bpffFile) #  get current .bpff contents 
    tree = newick_to_tree(bpff_contents[bpff_contents.index('COMMIT_TREE:')+1]) # get newick string (https://www.w3schools.com/python/ref_list_index.asp) from bpff_contents and convert to tree (easier with bigtree operations) (https://bigtree.readthedocs.io/0.16.4/bigtree/tree/construct/#bigtree.tree.construct.newick_to_tree)
    currentNode = find_attr(tree, "isCurrent", "True") # find current node in tree (https://bigtree.readthedocs.io/stable/bigtree/tree/search/#bigtree.tree.search.find_attr)

    Nodes = list(tree.descendants) # get list of all nodes in tree (https://bigtree.readthedocs.io/stable/bigtree/node/basenode/#bigtree.node.basenode.BaseNode.descendants) 
    latestID = max([int(node.node_name) for node in Nodes]) # find latest ID by converting all node names to integers and finding max (which will be the most recent)

    newNodeID = str(int(latestID)+1).zfill(3) # new node ID is current ID + 1, using zfill to ensure leading 0s (https://www.w3schools.com/python/ref_string_zfill.asp)
    newNode = Node(newNodeID, VersionAuthor=author, VersionDate=date, CommitMsg=commitmsg, isCurrent=current, parent=currentNode) # create new node with added information https://bigtree.readthedocs.io/stable/bigtree/node/node/

    if current == True: # we set the pointer for current version to the new node, so we need to set the old current node to False
        currentNode.isCurrent = False 

    # write updated tree and history back to file    
    f = open(outputFile, "w")

    # write header data (all lines before COMMIT_TREE:) back to file
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
    f.close() # close file after writing before adding footer

    # rewrite checksum footer
    with open(outputFile, "rb") as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest() # create sha256 checksum for updated file
    
    # append checksum to end of file
    with open(outputFile, "a") as bpff_appendFooter:
        bpff_appendFooter.write("\nchecksum-val:\n" + digest)
    bpff_appendFooter.close() # close file after appending footer

# Revert: reverts to a previous version in the main branch
def revert(bpffFile, revertVersionID, outputFile): 
    bpff_contents = getbpffcontents(bpffFile) # get .bpff contents
    tree = newick_to_tree(bpff_contents[bpff_contents.index('COMMIT_TREE:')+1]) # get newick string from contents and convert to tree
    revertNode = find_name(tree, revertVersionID) # find node to revert to by its ID (https://bigtree.readthedocs.io/stable/bigtree/tree/search/#bigtree.tree.search.find_name)
    currentNode = find_attr(tree, "isCurrent", "True") # find node which is currently marked as current version

    revertNode.set_attrs({"isCurrent": True}) # set desired revert version to be current
    currentNode.isCurrent = False # set old current version to false

    # write updated tree and history back to file
    f = open(outputFile, "w")
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

    # find index of revert node in history list and slice history list to that index (inclusive)
    revertIndex = history_list.index(revertVersionID)
    history_list = history_list[:revertIndex+1] 

    history_list = ">".join(history_list) # convert back to string with '>' separating IDs (from previous format)

    f.write("{main_branch_historyByID=(" + history_list + ")," + "current_ID=" + revertVersionID + "}\n") # write updated verison history and current ID back to file
    f.close() # close file after writing before footer

    # rewrite checksum footer
    with open(outputFile, "rb") as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest() # create sha256 checksum of file
    
    # append checksum to end of file
    with open(outputFile, "a") as bpff_appendFooter:
        bpff_appendFooter.write("\nchecksum-val:\n" + digest)
    bpff_appendFooter.close() # close file final
