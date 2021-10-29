import os, pytest
from rdmfileselector.classes.directory import Directory

abs_path = os.path.abspath('.')
test_file_1 = "test_file1.txt"
test_file_2 = "test_file2.txt"
test_dir_from = "test_dir_from"
test_dir_to = "test_dir_to"

def create_file(name):
    with open(os.path.join(abs_path, test_dir_from, name), 'w'): pass

@pytest.fixture
def directory():
    try:
        os.mkdir(os.path.join(abs_path, test_dir_from))
        create_file(test_file_1)
        create_file(test_file_2)
    except FileExistsError: pass

    yield Directory(
        os.path.join(abs_path, test_dir_from),
        files=[
            { "name": test_file_1, "score": 10 },
            { "name": test_file_2, "score": 5  }
        ]
    )
    
    try:
        os.remove(os.path.join(abs_path, test_dir_from, test_file_1))
        os.remove(os.path.join(abs_path, test_dir_from, test_file_2))
    except (FileNotFoundError, OSError): pass
    
    try:
        os.rmdir(os.path.join(abs_path, test_dir_from))
    except (FileNotFoundError, OSError): pass

def test_initialization(directory):
    """ Test if initialization creates a proper instance.
    """

    assert directory.path == os.path.join(abs_path, test_dir_from)
    assert len(directory.files) == 2

def test_has_changed(directory):
    """ Test if directory modification is detected
    """

    assert directory.has_changed() is False

    create_file("new_file.txt")

    assert directory.has_changed() is True

    os.remove(os.path.join(abs_path, test_dir_from, "new_file.txt"))