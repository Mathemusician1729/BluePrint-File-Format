import bigtree as bt
import pandas as pd
from bigtree import * #
import csv

try:
    # create new .bpff file, which we want to write to
    bpffFile1 = "blueprint_sample1.bpff"
    bpff_toWrite = open(bpffFile1, "w")

    sampleData = pd.read_csv("Sample_1.csv")
    header_data = sampleData[['File Author','Build Location', "Budget Limit", "Project ID", "Date of Approval", "Est. Date of Completion"]]

    for column in header_data.columns:
       header_line = column + ": " +  str(header_data.loc[0,column]) + "\n"
       bpff_toWrite.write(header_line)

    # tree stuff
    main_branch_IDs = [] # create array to store version IDs of "finalized" nodes
    tree_data = sampleData[['Version Author','Version Date','CommitID','CommitMsg','Last CommitID']]

    version_tree = dataframe_to_tree_by_relation(tree_data, child_col='Last CommitID',parent_col='CommitID')
    version_tree.show()

    # for j in range(1,len(Sample1_asArray)):
    #     for name, date, id, msg in Sample1_asArray[j]:
             

    #     if Sample1_asArray[j][Sample1_asArray[0].index("isMain")] == "True":
    #             main_branch_IDs.append(Sample1_asArray[j][Sample1_asArray[0].index("CommitID")])
    
    
            
            
except FileNotFoundError: # handles if there is no file found for sample data
    print("There is no such file, please try again")