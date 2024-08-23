import os
import sys
import ctypes
import requests
import subprocess
import time

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False

def run_as_admin(script_path):
    """Request UAC elevation."""
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])  # Pass additional args if necessary
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {params}', None, 1)
    sys.exit(0)  # Exit the current process

def delete_old_file(file_path):
    """Delete the old Python script if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
        os.system('cls')

def download_new(url, file_path):
    """Download the new Python script from the URL."""
    try:
        print("Downloading...")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        print("Download successful")
        print("Installing...")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Installation successful")
    except requests.RequestException:
        print("Error downloading the file.")
        print("Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues")
        input("Press Enter to exit...")
        sys.exit(1)

def run_new(batch_file_location):
    """Run the newly downloaded Python script and the batch file."""
    try:
        os.chdir(batch_file_location)
        os.startfile("Runner.bat")  # Run the batch file
    except Exception as e:
        print("Error running the batch file.")
        print("Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues")
        input("Press Enter to exit...")
        sys.exit(1)

def main():
    time.sleep(2)
    # Define paths
    file_path = r"C:\Program Files (x86)\FileOrganizeSuite\FileOrganizeSuite.py"
    url = "https://raw.githubusercontent.com/makisHr03/FileOrganizeSuite/main/FileOrganizeSuite/src/FileOrganizeSuite.py"
    batch_file_location = r"C:\Program Files (x86)\FileOrganizeSuite"

    # If not running as admin, request elevation
    if not is_admin():
        print("Administrative access is required to upgrade this app.")
        ask_admin = input("Would you like to run with administrative privileges (y/n)? ").strip().lower()
        if ask_admin in ["y", "yes"]:
            print("Requesting administrative privileges...")
            run_as_admin(sys.argv[0])
        else:
            print("Administrative privileges are required to upgrade this app.")
            input("Press Enter to exit...")
            sys.exit(1)

    # Proceed with the rest of the script after gaining admin privileges
    delete_old_file(file_path)
    download_new(url, file_path)
    run_new(batch_file_location)

    # Prompt user to press Enter to exit
    print("The program was upgraded successfully!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
