import unittest
from unittest.mock import Mock

from src.Utilities.Utilities import FileHandler


class Test_CanaryIOHandler(unittest.TestCase):
    def setUp(self) -> None:
        mock = Mock()
        self.fileHandler: FileHandler = mock
        self.mock = mock
        return super().setUp()