""" Handle scored files in this application's context.
"""

import shutil
import logging
from os import path


# pylint: disable=logging-fstring-interpolation
class File:
    """Represents one file."""

    MAX_SCORE = 30

    def __init__(self, path_directory, name, score=None):
        self.path_directory = path_directory
        self.name = name
        self.path = path.join(self.path_directory, self.name)

        if score is None:
            score = self.MAX_SCORE

        self.score = score

    def to_dict(self):
        """Transform this instance into a dict"""
        return {"name": self.name, "score": self.score}

    def copy(self, dir_to):
        """Copy this file from one place to another.
        Automatically decreases the score.
        """

        logging.info(f"Copying {self.name} to {dir_to}")
        shutil.copy(self.path, dir_to)
        self._score_decrease()

    def score_increase(self):
        """Increase file score by one."""

        if self.score < self.MAX_SCORE:
            self.score += 1
            logging.debug(f"Increased the score of '{self.name}' to {self.score}")

    def _score_decrease(self):
        """Decrease file score to lowest possible."""

        self.score = 0
        logging.debug(f"Lowered the score of '{self.name}' to {self.score}.")
