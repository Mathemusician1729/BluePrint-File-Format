# basic write to file:
basica_data = {
    "Name:": "Bob",
    "Git ID": 12345679,
    "Msg": "added new wall",
    "Date": "09/10/2025"
}

# save this data to a file
saveas_filename = "commit1.mpff"

# write to a file
file_to_save = open(saveas_filename, "w") # open "file" to write to 
file_to_save.write(str(basica_data)) # write contents to file into it
file_to_save.close() # close file

#############################################

# Fields example
name = "Bob"
git_ID = 1234569
msg = "added new wall"
date = "09/10/2025"

save_as = name + "_" + str(git_ID) + ".aka"

try: # good to have try statements
    file_to_write = open(save_as, "w")
    file_to_write.write("name: "+name+"\n")
    file_to_write.write("git ID: "+str(git_ID)+"\n")
    file_to_write.write("git Message: "+msg+"\n")

    file_to_write.close()

except FileNotFoundError:
    print("nothing man")