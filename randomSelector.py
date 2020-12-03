import os, shutil, random, json, sys, argparse

user_path = os.path.expanduser('~')
working_dir = os.path.abspath('.')

# Default values
destination_dir = os.path.join(user_path, 'Podcasts', 'Phone')
quantity = 5
allowed_formats = ('.mp3', '.mp4')
savefile = 'cache.json'
isVerbose = False

def status_message(message, status=None, prefix="", suffix="", isDebug=False):
    if (isVerbose and isDebug) or not isDebug:
        if status is not None:
            print(f"{prefix}[{status}] {message}{suffix}")
        else:
            print(f"{prefix}{message}{suffix}")

def load_args():
    global working_dir
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
        working_dir = os.path.abspath('.')
    elif args.input is not None:
        working_dir = args.input

    if args.destination == '.':
        destination_dir = os.path.abspath('.')
    elif args.destination is not None:
        destination_dir = args.destination

    if args.verbose:
        isVerbose = True

    status_message(f"Verbosity: {isVerbose}\nQuantity: {quantity}\nInput: {working_dir}\nDestination: {destination_dir}", isDebug=True)

def pick_files(filelist, last_picks, quantity):
    picked_files = []
    count = 0

    while count < quantity:
        random_int = random.randint(0, len(filelist) - 1)
        file = filelist[random_int]
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

def copy_files(filelist):
    for file in filelist:
        print(f'Copying {file} to {destination_dir}')
        filepath = os.path.join(working_dir, file)
        shutil.copy(filepath, destination_dir)
    print('\nDone!')

def save_data(picked_files):
    with open(savefile, 'w') as file:
        file.write(json.dumps(picked_files))

    print('Save successful!')

def load_data():
    if os.path.isfile(savefile):
        print(f"Savedata found!")
        with open(savefile, 'r') as file:
            last_picked_files = json.load(file)

        return last_picked_files

    print("No savedata found...")
    return []

def scan_dir(filelist):
    """ Scan a directory if it hasn't been scanned before.
    """
    listing = []
    status_message("Scanning destination directory...", status="scan")
    status_message(f"Found {len(filelist)} files.", status="scan")

    for item in filelist:
        listing.append({ "filename": item, "score": 10 })
        status_message(f"File: {item}, score: 10", status="scan", isDebug=True)

    directory = {
        "directory_name": working_dir,
        "filelist": listing
    }

    return directory

def main():
   load_args()
   filelist = os.listdir(working_dir)
   scan_dir(filelist)

   # if len(filelist) - 2 >= quantity:
   #     last_picks = load_data()
   #     valid_files = (len(filelist) - 2) - len(last_picks)
   #     if valid_files >= quantity:
   #         picked_files = pick_files(filelist, last_picks, quantity)
   #         copy_files(picked_files)

   #         save_data(picked_files)
   #     else:
   #         print(f"Not enough files to pick in the directory, try asking for {valid_files} file(s).")
   # else:
   #     print("Not enough files to pick in the directory...")

main()
