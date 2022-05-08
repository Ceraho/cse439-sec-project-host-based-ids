import os
import hashlib
import pickle
from collections import Counter


def edit_sub_text():
    print("press 1 to edit sub_1_text_2.txt, press 2 to revert it to original text.")
    action = int(input("action: "))
    if action == 1:
        new_text = input("New text: ")
        with open("DEMO_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt", 'w') as f:
            f.write(new_text)
    elif action == 2:
        with open("DEMO_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt", 'w') as f:
            f.write("This is a dummy text file to test Host Based IDS Project.")


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
    for i in range(len(x)):  # We print every hashed value and their path to check.
        print(x[i])

    return x


def find_identical_files(root_path):
    some_list = hash_all_files(root_path)
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


def take_snapshot(root_path):
    print("\nSNAPSHOT OPERATION STARTED...")
    list_to_text = list(hash_all_files(root_path))

    open_file = open("Snapshots/snapshot.txt", 'wb')
    pickle.dump(list_to_text, open_file)
    open_file.close()

    print("\nSNAPSHOT SAVED.\n")


def compare_to_latest_snapshot(root_path):
    print("\nCOMPARISON OPERATION HAS BEEN STARTED...\n")

    try:
        open_file = open("Snapshots/snapshot.txt", 'rb')
    except:
        print("No snapshot file exists yet!")
        return 0

    last_checkpoint_list = pickle.load(open_file)
    open_file.close()

    current_hash_list = hash_all_files(root_path)

    last_checkpoint_list.sort()
    current_hash_list.sort()

    if last_checkpoint_list == current_hash_list:
        print("\nIT ALL SEEMS FINE, NO MODIFICATIONS SINCE THE CHECKPOINT.")
    else:
        print("\nMODIFIED FILES DETECTED:")


# This is where we execute and demonstrate our IDS' functionalities.
def main():
    rootdir = 'DEMO_DIRECTORY'  # Define the root path's name where IDS will work on.

    # Find every identical file from their hash values and return them
    # find_identical_files(rootdir)

    # Takes snapshot of the DEMO_DIRECTORY's current version. (Saves hash values and file path's as .txt file)
    # take_snapshot(rootdir)

    # Start comparison with the latest snapshot and check if any file got modified
    # compare_to_latest_snapshot(rootdir)

    while True:
        print("\nWELCOME TO LOCAL IDS SYSTEM. PLEASE CHOOSE AN ACTION TO PROCEED:")
        print("1. Check for identical files in current state of the directory.")
        print("2. Take a snapshot of the current state of this directory.")
        print("3. Compare the current state with the last snapshot.")
        print("4. (FOR DEMO PURPOSES) Edit sub_1_text_2.txt to test compare function.")
        print("0. Exit")
        action = int(input("action: "))
        if action == 1:
            find_identical_files(rootdir)
        elif action == 2:
            take_snapshot(rootdir)
        elif action == 3:
            compare_to_latest_snapshot(rootdir)
        elif action == 4:
            edit_sub_text()
        elif action == 0:
            break


if __name__ == "__main__":
    main()
