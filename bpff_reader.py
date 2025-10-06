from bigtree import *

def read_bpff(bpff_file): # function for reading .bpff file and printing results
    bpff_read = open(bpff_file, "r") # open specified .bpff file
    bpff_contents = bpff_read.readlines() # get all lines and store in array (https://www.geeksforgeeks.org/python/python-program-to-replace-specific-line-in-file/)
    for i in range(len(bpff_contents)): # since each line ends with '\n' for newline, remove \n for the array contents
         bpff_contents[i] = bpff_contents[i].replace('\n','')

    # parse + print header information
    print("HEADER DATA:")
    header_length = bpff_contents.index('') # find index for end of header
    for i in range(0,header_length): # print each line of header
        print(bpff_contents[i])
    print()

    # parse newick representation of tree and print out visual representation of tree (using bigTree)
    tree_index = bpff_contents.index('COMMIT_TREE:')
    newick_string = bpff_contents[tree_index+1] # get newick string from contents (which occurs after when "COMMIT_TREE:" happens)
    versionTree_Reader = newick_to_tree(newick_string) # convert newick string to tree (https://bigtree.readthedocs.io/0.16.4/bigtree/tree/construct/#bigtree.tree.construct.newick_to_tree)

    print("BLUEPRINT VERSION HISTORY:")
    versionTree_Reader.show(all_attrs=True) # show visual rep of tree with data (author, date, message, and if it is current (if it applies))

    # parse and print pointer/history data for tree
    tree_metadata = bpff_contents[tree_index+2].split(",") # get line which contains the data for history/current version ID (2 lines after COMMIT_TREE:)
    history_fromFile, currentVersion = tree_metadata[0].strip("{main_branch_historyByID=()"), tree_metadata[1].strip("current_ID=}") # get history list and ID, removing extra text from files
    history_list = history_fromFile.split(">") # convert history into list again where each element is main branch IDs

    print("Current Version: Branch",currentVersion)
    history = '' # initialize history list string to show version history
    for ids_i in range(len(history_list)-1): # for each ID in the history list, add ID followed by "-->" (except for last) to history string
        history += history_list[ids_i] + " --> "
    history += history_list[-1]
    print("Main Branch History (by Branch ID):",history) # print history 

    # parse and print footer
    print("\nFOOTER DATA:")
    footer_index = bpff_contents.index('checksum-val:') # get index for beginning of footer 
    print("File Checksum Value (SHA-256): "+bpff_contents[footer_index+1]) # print checksum (line after where 'checksum-val:' happens)
    
    # close file at end
    bpff_read.close()