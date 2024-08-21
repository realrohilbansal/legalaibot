import unittest
from notebooks.model import qa

class TestLawGPT(unittest.TestCase):
    def test_basic_query(self):
        query = "What is Section 302 in IPC?"
        response = qa.invoke(input=query)
        self.assertIn("Section 302", response["answer"])

if __name__ == "__main__":
    unittest.main()
