import os
import hashlib
import string
from collections import Counter


def find_identical_files(some_list):
    hash_list = list()
    for i in range(len(some_list)):
        hash_list.append(some_list[i][0])

    d = Counter(hash_list)

    identical_files_list = list([item for item in d if d[item] > 1])

    final_list = list()
    for i in range(len(identical_files_list)):
        for j in range(len(some_list)):
            if identical_files_list[i] == some_list[j][0]:
                final_list.append(some_list[j])

    print("\nIDENTICAL FILES ARE:\n")
    for i in range(len(final_list)):
        print(final_list[i])


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


def hash_all_files(root_path):
    x = list()
    for subdir, dirs, files in os.walk(root_path):
        for file in files:
            x.append([hash_file(os.path.join(subdir, file)), os.path.join(subdir, file)])

    print("\nHASH VALUES ARE:\n")
    for i in range(len(x)):      # We print every hashed value and their path to check.
        print(x[i])

    return x


def take_snapshot(root_path):
    print("\nSNAPSHOT OPERATION STARTED...")
    list_to_text = list(hash_all_files(root_path))

    with open("Snapshots/snp_1.txt", 'w') as f:
        f.write('\n'.join(str(e) for e in list_to_text))

    print("\nSNAPSHOT SAVED.\n")


# This is where we execute and demonstrate our IDS' functionalities.
def main():
    rootdir = 'DEMO_DIRECTORY'  # Define the root path's name where IDS will work on.
    list_of_current_hash_values = hash_all_files(rootdir)  # Get hash values of every existing file in the given path/directory.

    find_identical_files(list_of_current_hash_values)   # Find every identical file from their hash values and return them

    take_snapshot(rootdir)      # Takes snapshot of the DEMO_DIRECTORY's current version. (Saves hash values and file path's as .txt file)


if __name__ == "__main__":
    main()