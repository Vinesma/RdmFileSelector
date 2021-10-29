import logging, os, json
from rdmfileselector.classes.directory import Directory

class Cache:
    """ Handle saving and loading of cache.
    """
    def __init__(self, dir_cache, file_cache):
        self.dir_cache = dir_cache
        self.file_cache = file_cache
    
    def save(self, directories):
        if not os.path.isdir(self.dir_cache):
            os.mkdir(self.dir_cache)

        with open(os.path.join(self.dir_cache, self.file_cache), 'w') as _file:
            _file.write(json.dumps(directories, cls=Directory))

        logging.info("Save to cache successful!")
        
    def load(self):
        if os.path.isfile(os.path.join(self.dir_cache, self.file_cache)):
            logging.info("Cache found!")

            with open(os.path.join(self.dir_cache, self.file_cache), 'r') as _file:
                directories = json.load(_file)

            return [Directory(path=directory["path"], files=directory["files"]) for directory in directories]

        logging.info("No savedata found...")
        return []
