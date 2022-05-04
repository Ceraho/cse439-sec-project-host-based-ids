import os
import string
import random

rootdir = 'DEMO_DIRECTORY'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # print(os.path.join(subdir, file))
        with open(os.path.join(subdir, file), 'w') as f:
            # f.write("This is a dummy text file to test Host Based IDS Project.")
            if os.path.join(subdir, file) == 'DEMO_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt' or os.path.join(subdir, file) == 'DEMO_DIRECTORY/text_4.txt':
                f.write("This is a dummy text file to test Host Based IDS Project.")
            else:
                f.write(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128)))