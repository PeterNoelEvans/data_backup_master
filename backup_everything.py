'''This is the master code for all backups.
It cannot be used as is.
Source and Destination need to be confirmed.'''
import os
import shutil
import signal
import sys
import time
import ctypes
import subprocess

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Copying interrupted.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def find_drive_by_label(drive_label):
    try:
        result = subprocess.check_output('wmic logicaldisk get name, volumename', shell=True)
        lines = result.decode().split('\n')
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1].lower() == drive_label.lower():
                return parts[0] + '\\'  # Return the drive letter with backslash
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute command: {e}")
    return None

def confirm_drive(label, drive_letter):
    response = input(f"The drive for '{label}' is set to {drive_letter}. Is this correct? (yes/no): ")
    return response.lower() == 'yes'

def copy_files(src, dest):
    total_files = 0
    copied_files = 0
    total_bytes = 0
    start_time = time.time()

    # Calculate the size of files to be copied and adjust total_files count
    for root, _, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(root, src)
            dest_file_dir = os.path.join(dest, relative_path)
            dest_file = os.path.join(dest_file_dir, file)
            
            if not os.path.exists(dest_file):  # Only count files that need to be copied
                total_files += 1
                total_bytes += os.path.getsize(src_file)

    if not os.path.exists(dest):
        os.makedirs(dest)

    for root, _, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(root, src)
            dest_file_dir = os.path.join(dest, relative_path)
            dest_file = os.path.join(dest_file_dir, file)

            if not os.path.exists(dest_file):
                if not os.path.exists(dest_file_dir):
                    os.makedirs(dest_file_dir)
                
                file_size = os.path.getsize(src_file)
                file_start_time = time.time()
                shutil.copy2(src_file, dest_file)
                file_end_time = time.time()
                copied_files += 1

                # Calculate the speed of the copy
                time_elapsed = file_end_time - file_start_time
                speed = (file_size / time_elapsed) / 1048576 if time_elapsed > 0 else 0
                print(f"Copied: {src_file} to {dest_file} [{copied_files}/{total_files} files] at {speed:.2f} MB/s")
            else:
                print(f"Skipped: {src_file} (already exists)")

    total_elapsed_time = time.time() - start_time
    avg_speed = (total_bytes / total_elapsed_time) / 1048576 if total_elapsed_time > 0 else 0
    print(f"All files copied. Total time: {total_elapsed_time:.2f}s, Average speed: {avg_speed:.2f} MB/s")

source_drive_label = 'SourceDriveLabel'  
destination_drive_label = 'MyBackupDrive'

source_drive = find_drive_by_label(source_drive_label)
destination_drive = find_drive_by_label(destination_drive_label)

if source_drive and destination_drive:
    if confirm_drive('source', source_drive) and confirm_drive('destination', destination_drive):
        src = os.path.join(source_drive, "data_source")  # Adjust path if different
        dest = os.path.join(destination_drive, "destination_backup")  # Destination path
        copy_files(src, dest)
        if input("Backup completed. Do you want to shut down the computer? (yes/no): ").lower() == 'yes':
            print("Shutting down the computer...")
            time.sleep(60)
            ctypes.windll.user32.ExitWindowsEx(0x00000008, 0x00000000)
        else:
            print("Shut down aborted. Exiting script.")
    else:
        print("Drive confirmation failed. Please verify the drives and try again.")
else:
    print("One or both drives not found. Please check the drive labels and connections.")
