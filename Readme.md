### Finding the Correct Drive Names

1. **Identify the Drive Labels:**
   - **Windows:** Open 'This PC' or 'Computer' from the Start menu or File Explorer. You'll see the drive names along with their assigned letters. The name displayed here is what Windows considers the volume label.
   - **Command Line:** You can also use the command line to list all drives with their labels for confirmation:
     ```bash
     wmic logicaldisk get name, volumename
     ```
     This will output the drive letters along with their volume names, helping you identify the correct labels to use in your script.

2. **Confirming Drive Labels:**
   - Make sure that the labels are unique to avoid any confusion, especially if you have multiple drives connected to your system.
   - If you’re unsure or if the labels could change (if someone renames them), you might want to consider setting more permanent and distinctive labels through the properties dialog of each drive in Windows Explorer.

### Updating Your Script

Once you have confirmed the labels, you can set these in your script:

- **Source Drive Label:** This is where your files that need backing up are currently stored. You'll want to ensure that the drive containing this folder has a stable label.
  
- **Destination Drive Label:** This is the label of the drive to which you are backing up your data. In your script. The placeholder might be 'MyBackupDrive'. You will need to make sure this is updated.


### Key Points:
- **Drive Detection**: The script uses the `find_drive_by_label` function to determine the correct drive based on its label. This function uses `wmic` to fetch volume names and compares them to your specified label.
- **Execution Flow**: The script only proceeds with copying if the drive is found. If not, it outputs an error message.
- **System Shutdown**: Ensure that the conditions for shutting down the system are appropriate and that this action won't disrupt other processes or lead to data loss.



### Running Your Script
- **Modify Drive Labels**: Replace `'SourceDriveLabel'` and `'MyBackupDrive'` with the actual labels of your source and destination drives.
- **Check Paths**: Ensure that the paths for `data_source` and `destination_backup` are correct according to your directory structure.
- **Schedule or Run Manually**: Depending on how you plan to use the script, either run it manually when the drives are connected, or schedule it while ensuring it checks if the drives are present before executing.


To create a batch file that will run your Python script `backup_everything.py` from the desktop in a command prompt window with administrator privileges on Windows 11, follow these steps:

### Step 1: Create the Batch File
1. **Open Notepad** or any text editor.
2. **Enter the following lines** into the text editor:

```batch
@echo off
cd %USERPROFILE%\Desktop
python backup_everything.py
pause
```

This batch file changes the directory to your desktop (where your `backup_everything.py` is located) and runs the script. The `pause` command keeps the window open after the script finishes so you can see any messages or errors.

### Step 2: Save the Batch File
- **Save the file** with a `.bat` extension, for example, `run_backup.bat`, on your desktop or any other convenient location.

### Step 3: Run the Batch File as Administrator
To ensure the batch file runs as an administrator, you can use one of the following methods:

#### Method 1: Manual Right-click
- **Right-click** the `run_backup.bat` file.
- Choose **Run as administrator** from the context menu.

#### Method 2: Create a Shortcut with Admin Rights
- **Right-click** on the `run_backup.bat` file and select **Create shortcut**.
- **Right-click** the shortcut and go to **Properties**.
- In the **Shortcut** tab, click **Advanced**.
- Check the box **Run as administrator**.
- Click **OK** and then **Apply** on the Properties window.

Now, whenever you double-click the shortcut, it will prompt for administrator privileges and run the batch file in an elevated command prompt.

### Note
Make sure Python is added to your system’s PATH environment variable. If it's not, you’ll need to specify the full path to the Python executable in your batch file, like this:

```batch
@echo off
cd %USERPROFILE%\Desktop
C:\Path\To\Python\python.exe backup.py
pause
```

Replace `C:\Path\To\Python\python.exe` with the actual path to your Python installation. This setup will ensure that your Python script runs with the necessary privileges and in the correct directory.