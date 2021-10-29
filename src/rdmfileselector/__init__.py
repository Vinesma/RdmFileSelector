"""
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
from rdmfileselector.helpers.cache import Cache
from rdmfileselector.helpers.options import Options
from rdmfileselector.classes.directory import Directory 

options = Options()

def main():
    cache = Cache(options.dir_cache, options.file_cache)

    if Directory.has_excess_files_in_dir(options.dir_destination, options.max_files):
        print("Destination directory has too many files, aborting.")
    else:
        directories = cache.load()
        index = Directory.find(options.dir_input, directories)

        if index != -1:
            directory = directories[index]

            directory.increase_all_file_scores()
            if directory.has_changed():
                directory.update()

            directories[index] = directory
        else:
            directory = Directory.scan(options.dir_input)

            logging.debug(f"Adding directory: {directory.path}")
            directories = [*directories, directory]

        if options.quantity > 0:
            directory.pick_random(options.quantity, options.dir_destination)
        else:
            # A quantity of less than 1 means that no files will be picked and only directory scans/updates will be done.
            print("Doing nothing because quantity is < 1")

        cache.save(directories)

if __name__ == "__main__":
    main()
