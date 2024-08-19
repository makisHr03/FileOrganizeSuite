import os
import shutil
import subprocess
import sys
from tqdm import tqdm
import urllib.request

# Global variables
log_full = []
log_error = []
duplicate_files = []
duplicates_detected = False
script_url = "https://raw.githubusercontent.com/makisHr03/FileOrganizeSuite/main/FileOrganizeSuite.py"

def show_logo():
    print("""
////////////////////////////////////////////////////////////////////////////////
// _____ _ _       ___                        _         ____        _ _       //
//|  ___(_) | ___ / _ \ _ __ __ _  __ _ _ __ (_)_______/ ___| _   _(_) |_ ___ //
//| |_  | | |/ _ \ | | | '__/ _` |/ _` | '_ \| |_  / _ \___ \| | | | | __/ _ \//
//|  _| | | |  __/ |_| | | | (_| | (_| | | | | |/ /  __/___) | |_| | | ||  __///
//|_|   |_|_|\___|\___/|_|  \__, |\__,_|_| |_|_/___\___|____/ \__,_|_|\__\___|//
//                          |___/                                             //
////////////////////////////////////////////////////////////////////////////////
                                                                         v1.1.0
    """)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def install_tqdm():
    try:
        from tqdm import tqdm
        return tqdm
    except ImportError:
        clear_screen()
        print("You need to install the tqdm module to use this program.")
        if input("Install tqdm now? (y/n): ").strip().lower() in ["y", "yes"]:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
                from tqdm import tqdm
                return tqdm
            except subprocess.CalledProcessError:
                clear_screen()
                print("Could not install tqdm. Please install it manually with 'pip install tqdm'.")
                sys.exit(1)
        else:
            print("Exiting because tqdm is required.")
            sys.exit(1)

# Check for tqdm
tqdm = install_tqdm()

def log_message(level, message):
    if level == "INFO":
        log_full.append(f"{level} - {message}")
    elif level == "ERROR":
        log_full.append(f"{level} - {message}")
        log_error.append(f"{level} - {message}")

def calculate_size(files):
    return sum(os.path.getsize(file) for file in files)

def get_free_space(folder):
    if os.name == "nt":
        _, _, free = shutil.disk_usage(folder)
    else:
        st = os.statvfs(folder)
        free = st.f_bavail * st.f_frsize
    return free

def copy_files(source_dir, dest_dir, extensions, category):
    global duplicate_files
    dest_folder = os.path.join(dest_dir, category)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    files_to_copy = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                files_to_copy.append(os.path.join(root, file))

    total_size = calculate_size(files_to_copy)
    free_space = get_free_space(dest_dir)
    if total_size > free_space:
        log_message("ERROR", "Not enough space in destination.")
        print("Not enough space in destination.")
        return

    with tqdm(total=len(files_to_copy), desc=f"Copying {category}", unit="file", dynamic_ncols=True) as pbar:
        for file_path in files_to_copy:
            file = os.path.basename(file_path)
            dest_path = os.path.join(dest_folder, file)

            if os.path.exists(dest_path):
                duplicate_files.append(file_path)
                log_message("INFO", f"Duplicate found: {file_path}")
                continue

            try:
                shutil.copy(file_path, dest_path)
                log_message("INFO", f"Copied {file_path} to {dest_path}")
            except Exception as e:
                log_message("ERROR", f"Error copying {file_path}: {e}")

            pbar.update(1)

    print(f"Finished copying {category} files.")

def select_file_types():
    file_types = {
        "Photos": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Audio": [".mp3", ".wav", ".flac"],
    }

    selected_categories = []
    clear_screen()
    show_logo()

    while True:
        print("Select the types of files you want to copy:")
        print("1. Photos")
        print("2. Videos")
        print("3. Documents")
        print("4. Audio")
        print("5. Custom select extensions")
        print("6. Select all types of files")
        print("----------------------------")
        print("7. Upgrade script")
        print("8. Exit")

        try:
            choice = int(input("Please select an option (e.g., 1): ").strip())

            if choice == 8:
                handle_exit()
                return None

            if choice == 7:
                upgrade_script()
                return None

            if choice == 5:
                selected_exts = []
                for cat, exts in file_types.items():
                    print(f"\nSelect {cat} extensions (e.g., jpg,png):")
                    print(f"Available: {', '.join(exts)}")
                    user_exts = input("Enter your choices: ").strip().split(",")
                    selected_exts.extend([f".{ext.strip()}" for ext in user_exts if f".{ext.strip()}" in exts])
                selected_categories.append(("Custom", selected_exts))

            elif choice == 6:
                selected_categories = [("All", [ext for exts in file_types.values() for ext in exts])]
            
            elif choice in [1, 2, 3, 4]:
                category = list(file_types.keys())[choice - 1]
                selected_categories.append((category, file_types[category]))

            else:
                print("Invalid choice. Please enter a number from the list.")

            if selected_categories or choice == 6:
                break

        except ValueError:
            print("Invalid input. Please enter a number.")

    if not selected_categories:
        selected_categories = [("All", [ext for exts in file_types.values() for ext in exts])]

    return selected_categories

def handle_exit():
    clear_screen()
    show_logo()
    print("Thank you for using FileOrganizeSuite!")
    input("Press Enter to exit...")
    sys.exit()

def view_logs(log_type):
    if log_type == "full":
        logs = log_full
    elif log_type == "error":
        logs = log_error
    else:
        print("Invalid log type")
        return

    if logs:
        for log in logs:
            print(log)
    else:
        print(f"{log_type.capitalize()} log is empty.")

def handle_duplicates():
    global duplicate_files, duplicates_detected

    if not duplicate_files:
        print("No duplicate files detected.")
        duplicates_detected = False
        return

    duplicates_detected = True
    print("\nDuplicate files detected:")
    for i, file_path in enumerate(duplicate_files, 1):
        print(f"{i}. {file_path}")

    while True:
        print("\nOptions for duplicates:")
        print("1. Ignore all")
        print("2. Overwrite all")
        print("3. Cancel")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("Ignoring duplicates.")
            duplicate_files.clear()
            duplicates_detected = False
            break
        elif choice == "2":
            print("Overwriting duplicates.")
            with tqdm(total=len(duplicate_files), desc="Overwriting duplicates", unit="file", dynamic_ncols=True) as pbar:
                for file_path in duplicate_files:
                    file = os.path.basename(file_path)
                    dest_path = os.path.join(destination_dir, file)

                    if os.path.exists(dest_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = os.path.join(destination_dir, f"{base}_{counter}{ext}")
                            counter += 1

                    try:
                        shutil.copy(file_path, dest_path)
                        log_message("INFO", f"Overwritten {file_path} to {dest_path}")
                    except Exception as e:
                        log_message("ERROR", f"Error overwriting {file_path}: {e}")

                    pbar.update(1)

            duplicate_files.clear()
            duplicates_detected = False
            break
        elif choice == "3":
            print("Cancelled.")
            break
        else:
            print("Invalid choice, try again.")

def upgrade_script():
    """  
    print("The upgrade feature is coming in the future.")
    input("Press Enter to continue...")
    select_file_types()
    """

    global script_url
    try:
        response = urllib.request.urlopen(script_url)
        updated_script = response.read()

        with open(sys.argv[0], 'wb') as file:
            file.write(updated_script)

        print("Download complete.")
        input("Press Enter to restart...")
        subprocess.call([sys.executable] + sys.argv)
        sys.exit()

    except Exception as e:
        log_message("ERROR", f"Failed to upgrade script: {e}")
        print("Failed to upgrade script. Please check the log for details.")

def main():
    global destination_dir, duplicates_detected

    while True:
        selected_categories = select_file_types()

        if selected_categories is None:
            return

        source_dir = input("Enter source directory: ").strip().strip('"')
        destination_dir = input("Enter destination directory: ").strip().strip('"')

        save_separately = input("Save each category in a separate folder? (y/n): ").strip().lower()

        clear_screen()
        show_logo()

        if save_separately in ["y", "yes"]:
            for category, exts in selected_categories:
                copy_files(source_dir, destination_dir, exts, category)
        else:
            all_exts = [ext for _, exts in selected_categories for ext in exts]
            copy_files(source_dir, destination_dir, all_exts, "All")

        if duplicates_detected:
            handle_duplicates()

        while True:
            print("\nOptions:")
            print("1. View full log")
            print("2. View error log")
            print("3. Handle duplicates")
            print("4. Copy another folder")
            print("5. Exit")

            option = input("Choose an option: ").strip()

            if option == "1":
                view_logs("full")
            elif option == "2":
                view_logs("error")
            elif option == "3":
                handle_duplicates()
            elif option == "4":
                clear_screen()
                break
            elif option == "5":
                if duplicate_files:
                    print("You have duplicate files!")
                    exit_duplicate = input("Would you like to handle them (y/n): ").strip().lower()
                    if exit_duplicate == 'y':
                        handle_duplicates()
                handle_exit()
            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
