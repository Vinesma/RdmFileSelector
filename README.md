# rdm-file-selector
Randomly selects files and copies them to a destination, in a way that's less likely to pick previous files.

### How it works

Scans the directory passed into it and assigns a maximum score to each file inside. If that file is randomly picked the score is dropped to 0, which makes the file way less likely to be picked for a long time, as the algorithm heavily favors files with a higher score.

The script saves everything to a cache file, and remembers each directory as it is called in. It can recognize file changes and removals and updates accordingly.

### How to use

Pass the `--help` flag to the script to learn the options available.


### TODO

Handle directories inside directories better
More options to use