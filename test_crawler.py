import unittest
from unittest.mock import patch
import os
import sqlite3

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.url = "https://example.com"
        self.output_file = "test_output.txt"
        self.db_file = "test_crawl_results.db"

    def test_file_output(self):
        crawl_and_extract_parameters(self.url, output_file=self.output_file, db_file=self.db_file)
        self.assertTrue(os.path.isfile(self.output_file))

    def test_database_output(self):
        crawl_and_extract_parameters(self.url, output_file=self.output_file, db_file=self.db_file)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM CrawledLinks")
        self.assertGreater(cursor.fetchone()[0], 0)
        conn.close()

    def tearDown(self):
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)

if __name__ == '__main__':
    unittest.main()
