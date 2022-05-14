import os
import hashlib
import pickle
import AES
import filecmp
from collections import Counter


def edit_some_file(filename):
    print(f"press 1 to edit {filename} file (edited file will be modified in an unintended way,"
          " causing conflicts to test IDS functionalities)")
    if "sub_1_text_2.txt" in filename:
        print("press 2 to revert sub_1_text_2.txt back to original")
    print("press 0 to go back.")

    action = int(input("action: "))

    if action == 1:
        new_text = input("New text: ")
        with open(filename, 'w') as f:
            f.write(new_text)
    elif action == 2 and "sub_1_text_2.txt" in filename:
        with open("DEMO_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt", 'w') as f:
            f.write("This is a dummy text file to test Host Based IDS Project.")
    else:
        pass


def hash_file(filename):
    # make a hash object
    h = hashlib.sha256()
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

    try:
        open_file = open("Snapshots/snapshot.txt", 'wb+')
        pickle.dump(list_to_text, open_file)
        open_file.close()
    except FileNotFoundError:
        print("Could not find Snapshots directory, creating one now.")
        os.mkdir("Snapshots")
        open_file = open("Snapshots/snapshot.txt", 'wb+')
        pickle.dump(list_to_text, open_file)
        open_file.close()

    password = input("Password: ")

    AES.encrypt(AES.getKey(password), "Snapshots/snapshot.txt")

    print("\nSNAPSHOT SAVED AND ENCRYPTED.\n")


def compare_to_latest_snapshot(root_path):
    print("\nCOMPARISON OPERATION HAS BEEN STARTED...\n")

    password = input("Password: ")

    try:
        AES.decrypt(AES.getKey(password), "Snapshots/(enc)snapshot.txt")
    except FileNotFoundError:
        print("Can't find encrypted snapshot file, exiting comparison process.")
        return

    check_if_modified = filecmp.cmp("Snapshots/snapshot.txt", "Snapshots/(dec)snapshot.txt", shallow=False)
    os.remove("Snapshots/(dec)snapshot.txt")

    if not check_if_modified:
        print("WARNING: THE SNAPSHOT FILE HAS BEEN MODIFIED BY AN OUT-SOURCE, PLEASE CONTROL THE \"snapshot.txt\"!")
        return

    try:
        open_file = open("Snapshots/snapshot.txt", 'rb')
        last_checkpoint_list = pickle.load(open_file)
        open_file.close()
    except:
        print("No snapshot file exists yet!")
        return

    current_hash_list = hash_all_files(root_path)

    last_checkpoint_list.sort()
    current_hash_list.sort()

    if last_checkpoint_list == current_hash_list:
        print("\nIt all seems fine, no modifications since the checkpoint.")
    else:
        print("\nWARNING: MODIFIED FILES DETECTED IN THE DIRECTORY!:")

        for cur_element in current_hash_list:
            if cur_element not in last_checkpoint_list:
                print(cur_element[1])


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
        print("4. (FOR DEMO PURPOSES) Edit sub_1_text_2.txt to test compare to last checkpoint function.")
        print("5. (FOR DEMO PURPOSES) Edit snapshot.txt to test if modifying original snapshot file case is covered.")
        print("0. Exit")
        action = int(input("action: "))
        if action == 1:
            # Find every identical file from their hash values and return them.
            find_identical_files(rootdir)
        elif action == 2:
            # Takes snapshot of the DEMO_DIRECTORY's current version.
            # ... (Saves hash values and file path's as .txt file)
            take_snapshot(rootdir)
        elif action == 3:
            # Start comparison with the latest snapshot and check if any file got modified.
            compare_to_latest_snapshot(rootdir)
        elif action == 4:
            # We use edit_some_file() func. to modify sub_1_text_2.txt after we run take_snapshot()
            # ... and right before compare_to_latest_snapshot() in order to test and see if comparing
            # ... to the latest snapshot works.
            edit_some_file("DEMO_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt")
        elif action == 5:
            # We use edit_some_file() func. to modify snapshot.txt after we run take_snapshot()
            # ... and right before compare_to_latest_snapshot() in order to test and see if we can
            # ... detect modified snapshot file.
            edit_some_file("Snapshots/snapshot.txt")
        elif action == 0:
            # Quit the program safely.
            break
        else:
            print("Invalid action, please try again.")


if __name__ == "__main__":
    main()
