import os, shutil, random, json, sys, argparse

user_path = os.path.expanduser('~')
input_directory = os.path.abspath('.')

# Default values
destination_dir = os.path.join(user_path, 'Podcasts', 'Phone')
quantity = 5
allowed_formats = ('.mp3', '.mp4')
savefile = 'cache.json'
isVerbose = False

def status_message(message, status=None, prefix="", suffix="", isDebug=False):
    """ Displays an optional status message to the user.
    """
    if (isVerbose and isDebug) or not isDebug:
        if status is not None:
            print(f"{prefix}[{status}] {message}{suffix}")
        else:
            print(f"{prefix}{message}{suffix}")

def load_args():
    """ Parse and load arguments
    """
    global input_directory
    global destination_dir
    global quantity
    global isVerbose

    # Initializer
    parser = argparse.ArgumentParser(description="Picks files randomly.")
    # Argument definition
    # optional
    parser.add_argument("-q", "--quantity", type=int, help="How many files to pick from the input directory.")
    parser.add_argument("-i", "--input", help="Place to select the files from.")
    parser.add_argument("-v", "--verbose", help="Control amount of output.", action="store_true")
    # positional
    parser.add_argument("destination", help="Place to put the randomly picked files.")
    args = parser.parse_args()

    # Loads arguments
    if args.quantity is not None:
        quantity = args.quantity

    if args.input == '.':
        input_directory = os.path.abspath('.')
    elif args.input is not None:
        input_directory = args.input

    if args.destination == '.':
        destination_dir = os.path.abspath('.')
    elif args.destination is not None:
        destination_dir = args.destination

    if args.verbose:
        isVerbose = True

    status_message(f"Verbosity: {isVerbose}\nQuantity: {quantity}\nInput: {input_directory}\nDestination: {destination_dir}", isDebug=True)

def save_data(directories):
    """ Save directory data.
    """
    with open(savefile, 'w') as file:
        file.write(json.dumps(directories))

    status_message("Save successful!", status="save")

def load_data():
    """ Load saved data.
    """
    if os.path.isfile(savefile):
        status_message("Savedata found!", status="load")
        with open(savefile, 'r') as file:
            directories = json.load(file)

        return directories

    status_message("No savedata found...", status="load")
    return []

def copy_files(files):
    """ Copy a list of files.
    """
    for file in files:
        print(f'Copying {file} to {destination_dir}')
        filepath = os.path.join(input_directory, file)
        shutil.copy(filepath, destination_dir)
    print('\nDone!')

def pick_files(files, last_picks, quantity):
    """ Randomly pick a number of files from the directory.
    """
    picked_files = []
    count = 0

    while count < quantity:
        random_int = random.randint(0, len(files) - 1)
        file = files[random_int]
        picked_before = False

        if file.endswith(allowed_formats):
            if len(last_picks) > 0:
                for item in last_picks:
                    if item == file:
                        picked_before = True
                        break

            if len(picked_files) > 0:
                for item in picked_files:
                    if item == file:
                        picked_before = True
                        break

            if not picked_before:
                print(f'{file} was picked!')
                picked_files.append(file)
                count += 1

    return picked_files

def find_dir(directory_name, directories):
    """ Find a directory by name inside a list of directories and return a tuple with index and True/False
    """
    for i, item in enumerate(directories):
        if item['directory_name'] == directory_name:
            status_message(f"Directory: {directory_name} found at index {i}", status="find dir", isDebug=True)
            return (True, i)

    return (False, -1)

def dir_is_updated(previous_directory):
    """ Check if the directory is unchanged.
    """
    previous_file_number = previous_directory['file_quantity']
    current_file_number = len(os.listdir(input_directory))
    if previous_file_number == current_file_number:
        status_message("Directory is up to date!", status="dir is updated?", isDebug=True)
        return True

    status_message("Directory is not up to date.", status="dir is updated?", isDebug=True)
    return False

def update_dir(directory, directories):
    """ Update a directory's entry in the directories.
    """
    isFound, index = find_dir(directory['directory_name'], directories)
    files = os.listdir(input_directory)
    if isFound:
        if len(files) > directory['file_quantity']:
            for item in files:
                fileIsUpToDate = False
                for directory_file in directory['files']:
                    status_message(f"Comparing: {item} with: {directory_file['filename']}", status="update_dir", isDebug=True)
                    if item == directory_file['filename']:
                        fileIsUpToDate = True
                        break
                if not fileIsUpToDate:
                    status_message(f"New file found: {item}, Adding it with default score.", status="update dir", isDebug=True)
                    directory['files'].append({ "filename": item, "score": 10 })
        else:
            deletedFiles = []
            for directory_file in directory['files']:
                fileHasBeenDeleted = True
                for item in files:
                    status_message(f"Comparing: {directory_file['filename']} with: {item}", status="update_dir", isDebug=True)
                    if directory_file['filename'] == item:
                        fileHasBeenDeleted = False
                        break
                if fileHasBeenDeleted:
                    deletedFiles.append(directory_file)

            for removed_file in deletedFiles:
                status_message(f"File not found: {removed_file['filename']}, Removing entry.", status="update dir", isDebug=True)
                directory['files'].remove(removed_file)

        directory['file_quantity'] = len(directory['files'])
        directories[index] = directory
        status_message(f"Updated directory {directory['directory_name']} in cache.", status="update dir", isDebug=True)

    return directories

def add_dir(directory, directories):
    """ Add a directory to the directories.
    """
    status_message(f"Adding directory: {directory['directory_name']}", status="add directory", isDebug=True)
    directories.append(directory)

    return directories

def scan_dir():
    """ Scan a directory if it hasn't been scanned before.
    """
    files = os.listdir(input_directory)
    aggregated = []
    status_message("Scanning destination directory...", status="scan")
    status_message(f"Found {len(files)} files.", status="scan")

    for item in files:
        aggregated.append({ "filename": item, "score": 10 })
        status_message(f"File: {item}, score: 10", status="scan", isDebug=True)

    directory = {
        "directory_name": input_directory,
        "file_quantity": len(aggregated),
        "files": aggregated
    }

    return directory

def main():
    load_args()
    directories = load_data()
    isFound, index = find_dir(input_directory, directories)
    if isFound:
        directory = directories[index]
        if not dir_is_updated(directory):
            status_message(f"Directory: {directory['directory_name']} has been changed. Updating now...", status="update dir", isDebug=True)
            directories = update_dir(directory, directories)
    else:
        status_message(f"Directory: {input_directory} has not been found. Adding it...", status="not found")
        directory = scan_dir()
        directories = add_dir(directory, directories)

    save_data(directories)

  # if len(files) - 2 >= quantity:
  #     last_picks = load_data()
  #     valid_files = (len(files) - 2) - len(last_picks)
  #     if valid_files >= quantity:
  #         picked_files = pick_files(files, last_picks, quantity)
  #         copy_files(picked_files)

  #         save_data(picked_files)
  #     else:
  #         print(f"Not enough files to pick in the directory, try asking for {valid_files} file(s).")
  # else:
  #     print("Not enough files to pick in the directory...")

main()
