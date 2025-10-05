from bigtree import *

def read_bpff(bpff_file): # function for reading .bpff file and printing results
    """
    input: .bpff filename
    output: print .bpff contents to console 
    """
    bpff_read = open(bpff_file, "r") # open specified .bpff file
    bpff_contents = bpff_read.readlines() # get all lines and store in array
    for i in range(len(bpff_contents)): # since each line ends with '\n' for newline, remove \n for the array contents
         bpff_contents[i] = bpff_contents[i].replace('\n','')

    # parse + print header information
    header_length = bpff_contents.index('') # find index for end of header
    for i in range(0,header_length): # print each line of header
        print(bpff_contents[i])
    print()

    # parse newick representation of tree and print out tree (using bigTree)
    tree_index = bpff_contents.index('COMMIT_TREE:')
    newick_string = bpff_contents[tree_index+1]
    versionTree_Reader = newick_to_tree(newick_string)

    print("Blueprint Version History:")
    versionTree_Reader.show(all_attrs=True)

    # parse metadata 
    tree_metadata = bpff_contents[tree_index+2].split(",") # get line which contains 
    history_fromFile, currentVersion = tree_metadata[0], tree_metadata[1]

    #
    currentVersion = currentVersion.strip("current_ID=}")

    #
    history_fromFile = history_fromFile.strip("{main_branch_historyByID=()")
    history_list = history_fromFile.split(">")

    # print results
    print("\nCurrent Version: Branch",currentVersion)

    history = ''
    for ids_i in range(len(history_list)-1):
        history += history_list[ids_i] + " --> "
    history += history_list[-1]
    print("Main Branch History (by Branch ID):",history)
    
    # close file at end
    bpff_read.close()
    return # TODO return something?

read_bpff("tester.bpff")
read_bpff("tester2.bpff")