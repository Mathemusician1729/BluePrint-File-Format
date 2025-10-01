import bigtree as bt # Import the bigtree library
from bigtree import dict_to_tree, Node
import csv

# Create a dictionary representing the tree structure
data_dict = {
    "gitID1": {"message":"blank", "CurrentVer": False},
    "gitID1/gitID2": {"message":"git commit 1", "CurrentVer": False},
    "gitID1/gitID3": {"message":"git commit 2", "CurrentVer": False},
    "gitID1/gitID2/gitID4": {"message":"git commit 3", "CurrentVer": False},
    "gitID1/gitID2/gitID5": {"message":"git commit 4", "CurrentVer": True}
}

lolz = dict_to_tree(data_dict) # Convert the dictionary to a tree structure
# lolz.show(attr_list=["message", "CurrentVer"]) # Display the tree with the 'message' attribute

root = Node("001", msg="poopypants", date="09/10/2025")
child_2a = Node("002", msg="poopypants 2", date="09/11/2025", parent=root)
child_2b = Node("003", msg="poopypants 4", date="09/12/2025", parent=root)
child_3a = Node("004", msg="poopypants 5", date="09/13/2025", parent=child_2b)
child_3b = Node("004", msg="poopypants 5", date="09/13/2025", parent=child_2a)

root.show(attr_list=["msg", "date"])