Welcome to my CSE 439 Computer Security project!

This project's main goal was to implement a host-level Intrusion Detection System (IDS). Basically, it has 3 main features:
1. Recognizing identical files: The application will pick a folder (DEMO_DIRECTORY in my case) and scan through all files under the folder. The application will then recognize identical files by checking each files' hash values. If any identical files exist, the list of that will be returned as output.

2. Checkpointing files: The application will take a snapshot of the files in a folder (DEMO_DIRECTORY in my case) and create a checkpoint that will be used for comparison to the current state of the folder/directory. Basically, this checkpoint is used to identify the modified files. The security of the checkpoint file is provided by encrypting a copy of the file with AES algorithm. When needed to check if snapshot file is modified, we decrypt the encrypted copy and compare it to the main snpashot file. If both files are equal, then we are ensured of that this file was not modified by an out-source.

3. Identifying modified files: As mentioned above, the application reads the checkpoint file which is created earlier, and detect the modified files since the creation of the checkpoint. The output of this task will is returned as a list of the modified files.

IMPORTANT NOTE:
In order for AES encryption to work, I have used an external Python library 'pyCryptodome'. So make sure to install pyCryptodome with Python's package installer pip:

"pip install pycryptodome" 

After installation of pyCryptodome, you can run the program with:

"python3 main.py"

For the usage part, the greeting menu will be mostly self-explanatory. "Replace .txt" and "Replace snapshot" options are to simulate how program reacts if an outsider modifies those files.