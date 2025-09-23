file_toLoad = "Tutorial Help/commit1.mpff" # make sure to specify full file path if using folder (not huge worry outside of tutorial stuff)
array = []

try:
    file = open(file_toLoad, "r") # open to "read"/r (not write/modify/w)
    for line in file: # loop through each line in the file
        array.append(line) # append data into array
    
    file.close()
    print("File Loaded:", file_toLoad)
    print(array)

except FileNotFoundError:
    print("No File Found")
    