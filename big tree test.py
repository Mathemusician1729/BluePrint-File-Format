import bigtree as bt # Import the bigtree library
from bigtree import dict_to_tree # Import the dict_to_tree function

# Create a dictionary representing the tree structure
data_dict = {
    "gitID1": {"message":"blank"},
    "gitID1/gitID2": {"message":"git commit 1"},
    "gitID1/gitID3": {"message":"git commit 2"},
    "gitID1/gitID2/gitID4": {"message":"git commit 3"},
    "gitID1/gitID2/gitID5": {"message":"git commit 4"}
}

root = dict_to_tree(data_dict) # Convert the dictionary to a tree structure
root.show(attr_list=["message"]) # Display the tree with the 'message' attribute