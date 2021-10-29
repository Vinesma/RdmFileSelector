import argparse, logging, os

class Options:
    """ Initialize argument based options and logging.
    """
    def __init__(self):
        # Defaults
        self.path_user = os.path.expanduser('~')
        self.dir_input = os.path.abspath('.')
        self.dir_destination = os.path.join(self.path_user, 'Podcasts', 'Phone')
        self.dir_cache = os.path.join(self.path_user, '.cache', 'rdmfileselector')
        self.file_cache = "cache.json"
        self.quantity = 5
        self.max_files = 100

        # Initializer
        parser = argparse.ArgumentParser(description="Picks files randomly.")
        # Argument definition
        # optional
        parser.add_argument("-q", "--quantity", type=int, help="how many files to pick from the input directory.")
        parser.add_argument("-i", "--input", help="where to select the files from.")
        parser.add_argument("-v", "--verbose", help="make the application more verbose.", action="store_true")
        parser.add_argument("-c", "--cache", help="use a different directory for the cache file.")
        parser.add_argument("-o", "--condition", type=int, help="only proceed if there are less files in the dir than the chosen parameter.")
        # positional
        parser.add_argument("destination", help="where to put the randomly picked files.")
        args = parser.parse_args()

        # Loads arguments
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: [%(funcName)s] %(message)s")
        else:
            logging.basicConfig(level=logging.INFO, format="%(levelname)s:  [%(funcName)s] %(message)s")

        if args.quantity is not None:
            self.quantity = args.quantity

        if args.input.startswith('~', 0, 1):
            self.dir_input = os.path.expanduser(args.input)
        elif args.input is not None:
            self.dir_input = os.path.abspath(args.input)

        if args.destination.startswith('~', 0, 1):
            self.dir_destination = os.path.expanduser(args.destination)
        elif args.destination is not None:
            self.dir_destination = os.path.abspath(args.destination)

        if args.cache is not None:
            self.dir_cache = os.path.expanduser(args.cache)
        
        if args.condition is not None:
            self.max_files = args.condition

        logging.debug(f"Quantity: {self.quantity}")
        logging.debug(f"Input: {self.dir_input}")
        logging.debug(f"Destination: {self.dir_destination}")