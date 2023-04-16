import dotenv, unittest

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dotenv.load_dotenv()