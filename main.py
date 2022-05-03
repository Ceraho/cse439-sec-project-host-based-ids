import os
import hashlib


def hash_file(filename):
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()


rootdir = 'IDS_DIRECTORY'
list_of_hash_values = list()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        list_of_hash_values.append(hash_file(os.path.join(subdir, file)))

print(list_of_hash_values)