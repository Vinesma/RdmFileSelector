""" Deal with directories in the context of this application.
"""

import logging
from os import listdir
from random import sample
from json import JSONEncoder
from rdmfileselector.classes.file import File


class Directory(JSONEncoder):
    """Represents one directory"""

    def __init__(self, path, files=None):
        if files is None:
            file_list = []
        else:
            file_list = [
                File(
                    path_directory=path,
                    name=_file["name"],
                    score=_file.get("score", None),
                )
                for _file in files
            ]

        self.files = file_list
        self.path = path

    def __len__(self):
        return len(self.files)

    def __dict__(self):
        return {"path": self.path, "files": [_file.__dict__() for _file in self.files]}

    def default(self, o):
        return object.__dict__

    def increase_all_file_scores(self):
        """Increase score for all files in this directory."""

        for _file in self.files:
            _file.score_increase()

    def has_changed(self):
        """Determine if a directory has changed since the last time."""

        files_now = len(listdir(self.path))
        files_before = len(self.files)

        if files_now == files_before:
            logging.debug("Directory is up to date!")
            return False

        logging.debug("Directory is NOT up to date!")
        return True

    def update(self):
        """Update this directory with new files."""
        file_names = listdir(self.path)
        cache_file_names = [_file.name for _file in self.files]

        if len(file_names) > len(self.files):
            logging.info("More files were added since last time.")
            # Find which files are new by filtering out filenames that already exist
            new_files = [
                File(self.path, _file)
                for _file in list(
                    filter(
                        lambda file_name: file_name not in cache_file_names, file_names
                    )
                )
            ]
            self.files = [*self.files, *new_files]
        else:
            logging.info("Some files were removed since last time.")
            # Find which files were removed by singling out names that don't exist anymore
            removed_files = list(
                filter(lambda file_name: file_name not in file_names, cache_file_names)
            )
            self.files = list(
                filter(lambda _file: _file.name not in removed_files, self.files)
            )

        logging.debug("Updated directory: '%s'", self.path)

    def pick_random(self, quantity, dir_to):
        """Select files at random and copy them somewhere else."""

        shuffled_files = sample(self.files, len(self.files))
        prefer_score = File.MAX_SCORE
        count = 0
        done = False

        if quantity > len(shuffled_files):
            logging.info(
                f"Directory only has {len(shuffled_files)}, less than asked ({quantity}). Less files will be picked."
            )

        while not done:
            logging.debug(f"Preferred score is now {prefer_score}")
            for _file in shuffled_files:
                if _file.score == prefer_score:
                    logging.debug(f"Picked '{_file.name}' with score: {_file.score}")
                    _file.copy(dir_to)
                    count += 1

                if count == quantity:
                    logging.info("Hit quantity limit.")
                    done = True
                    break

            if prefer_score == 0 and not done:
                logging.debug("Unable to hit quantity limit.")
                done = True
            elif prefer_score != 0 and not done:
                prefer_score -= 1
            else:
                done = True

    @staticmethod
    def find(directory_path, directories):
        """Return the index of a directory in a list of directories by the path.
        If none is found, returns -1.
        """

        for index, directory in enumerate(directories):
            if directory.path == directory_path:
                logging.debug(f"Directory '{directory_path}' found at index {index}")
                return index

        return -1

    @staticmethod
    def scan(directory_path):
        """Scan a directory.
        Returns a directory instance.
        """

        logging.info(f"Directory '{directory_path}' has not yet been scanned.")
        logging.info("Scanning destination directory...")
        files = listdir(directory_path)

        logging.info(f"Found {len(files)} files.")
        [logging.debug(f"File: '{_file}'") for _file in files]

        return Directory(
            path=directory_path, files=[{"name": _file} for _file in files]
        )

    @staticmethod
    def has_excess_files_in_dir(directory_path, limit):
        """Check if the directory has more files than the limit.
        Returns a boolean.
        """

        n_files = len(listdir(directory_path))
        logging.debug(f"Directory has {n_files} files. Limit is {limit} files.")

        return n_files > limit
