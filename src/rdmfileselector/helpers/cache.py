""" Provides helpers for loading and saving cache.
"""

import logging
import os
import json
from rdmfileselector.classes.directory import Directory

class Cache:
    """ Handle saving and loading of cache.
    """
    def __init__(self, dir_cache, file_cache):
        self.dir_cache = dir_cache
        self.file_cache = file_cache

    def save(self, directories):
        """ Save a list of directories to the cache file.
        """
        if not os.path.isdir(self.dir_cache):
            os.mkdir(self.dir_cache)

        with open(os.path.join(self.dir_cache, self.file_cache), 'w', encoding="utf-8") as _file:
            _file.write(json.dumps(directories, cls=Directory))

        logging.info("Save to cache successful!")

    def load(self):
        """ Load a list of directories from the cache file.
        """
        if os.path.isfile(os.path.join(self.dir_cache, self.file_cache)):
            logging.info("Cache found!")
            load_path = os.path.join(self.dir_cache, self.file_cache)

            with open(load_path, 'r', encoding="utf-8") as _file:
                directories = json.load(_file)

            return [
                Directory(
                    path=directory["path"], files=directory["files"]
                ) for directory in directories
            ]

        logging.info("No savedata found...")
        return []
