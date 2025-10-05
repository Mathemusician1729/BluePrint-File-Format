import bigtree as bt # Import the bigtree library
from bigtree import *
import pandas as pd

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

relation_data = pd.DataFrame([["a", None, 90],
                              ["b", "a", 65],
                              ["c", "a", 60],
                              ["d", "b", 40]],
                              columns=["child", "parent", "age"]
                              )

print(relation_data)
version_tree = dataframe_to_tree_by_relation(relation_data, child_col="child", parent_col="parent")
version_tree.show(attr_list=['age'])

d = [node.node_name for node in bt.preorder_iter(version_tree)]
print(d)