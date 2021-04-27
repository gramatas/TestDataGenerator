# Bonobo
from bonobo.constants import NOT_MODIFIED

# Utilities
import csv


class DestinationCSV:
    """
    Bonobo CSV Loader
    """
    def __init__(self, filename, schema):
        """
        :param filename: CSV filename
        """
        self.file = open(filename, 'w')
        self.writer = csv.DictWriter(self.file, fieldnames=schema.keys())
        self.writer.writeheader()

    def __call__(self, *row):
        """
        Writes csv rows
        :param row: Row from graph
        :return: NOT_MODIFIED Bonobo element
        """

        self.writer.writerow(row[0])

        return NOT_MODIFIED
