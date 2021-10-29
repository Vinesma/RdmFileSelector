import shutil, logging
from os import path

class File:
    """ Represents one file.
    """
    
    max_score = 30

    def __init__(self, path_directory, name, score = None):
        self.path_directory = path_directory
        self.name = name
        self.path = path.join(self.path_directory, self.name)

        if score is None:
            score = self.max_score

        self.score = score

    def copy(self, dir_to):
        """ Copy this file from one place to another.
        """

        logging.info(f"Copying {self.name} to {dir_to}")
        shutil.copy(self.path, dir_to)

    def score_increase(self):
        """ Increase file score by one.
        """

        if (self.score < self.max_score):
            self.score += 1
            logging.debug(f"Increased the score of '{self.name}' to {self.score}")

    def score_decrease(self):
        """ Decrease file score to lowest possible.
        """

        self.score = 0
        logging.debug(f"Lowered the score of '{self.name}' to {self.score}.")
    
    def to_dict(self):
        """ Return a dictionary version of this instance.
        """
        
        return {
            "name": self.name,
            "score": self.score
        }