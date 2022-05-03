import os
import string
import random

rootdir = 'IDS_DIRECTORY'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # print(os.path.join(subdir, file))
        with open(os.path.join(subdir, file), 'w') as f:
            # f.write("This is a dummy text file to test Host Based IDS Project.")
            if os.path.join(subdir, file) == 'IDS_DIRECTORY/SUB_DIRECTORY_1/sub_1_text_2.txt' or os.path.join(subdir, file) == 'IDS_DIRECTORY/text_4.txt':
                f.write("This is a dummy text file to test Host Based IDS Project.")
            else:
                f.write(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128)))

# echo "# CSE439_Sec_Project-Host_Based_IDS" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/Ceraho/CSE439_Sec_Project-Host_Based_IDS.git
# git push -u origin main
