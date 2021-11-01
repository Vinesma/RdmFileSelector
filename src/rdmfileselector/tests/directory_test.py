""" Tests for directories """

import os
import pytest
from rdmfileselector.classes.directory import Directory

abs_path = os.path.abspath(".")
TEST_FILE_1 = "test_file1.txt"
TEST_FILE_2 = "test_file2.txt"
TEST_DIR_FROM = "test_dir_from"
TEST_DIR_TO = "test_dir_to"


def create_file(name):
    """Create a file"""
    open(os.path.join(abs_path, TEST_DIR_FROM, name), "w", encoding="utf-8").close()


@pytest.fixture
def directory():
    """Fixture that returns a new directory"""
    try:
        os.mkdir(os.path.join(abs_path, TEST_DIR_FROM))
        create_file(TEST_FILE_1)
        create_file(TEST_FILE_2)
    except FileExistsError:
        pass

    yield Directory(
        os.path.join(abs_path, TEST_DIR_FROM),
        files=[{"name": TEST_FILE_1, "score": 10}, {"name": TEST_FILE_2, "score": 5}],
    )

    try:
        os.remove(os.path.join(abs_path, TEST_DIR_FROM, TEST_FILE_1))
        os.remove(os.path.join(abs_path, TEST_DIR_FROM, TEST_FILE_2))
    except (FileNotFoundError, OSError):
        pass

    try:
        os.rmdir(os.path.join(abs_path, TEST_DIR_FROM))
    except (FileNotFoundError, OSError):
        pass


def test_initialization(directory):
    """Test if initialization creates a proper instance."""

    assert directory.path == os.path.join(abs_path, TEST_DIR_FROM)
    assert len(directory.files) == 2


def test_has_changed(directory):
    """Test if directory modification is detected"""

    assert directory.has_changed() is False

    create_file("new_file.txt")

    assert directory.has_changed() is True

    os.remove(os.path.join(abs_path, TEST_DIR_FROM, "new_file.txt"))
