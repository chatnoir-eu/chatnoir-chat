import importlib
# load construct indexes from ../construct_indexes.py
parse_run = importlib.import_module('construct_indexes').parse_run
extract_from_file = importlib.import_module('construct_indexes').extract_from_file
import unittest
import os

def resource(f):
    return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + f

class TestParsingOfRuns(unittest.TestCase):
    def test_parsing_of_run_for_non_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_run('path does not exist.')

    def test_parsing_of_run_out_of_order(self):
        with self.assertRaises(ValueError):
            parse_run(resource('run_incorrect_order.txt'))

    def test_parsing_of_run_correct_order(self):
        expected = {'1': {'end': 45, 'start': 0}, '2': {'end': 88, 'start': 46}}
        actual = parse_run(resource('run_correct_order.txt'))
        self.assertEqual(expected, actual)

    def test_extraction_of_first_topic(self):
        expected = '1 Q0 doc1 1 6.3 system\n1 Q0 doc2 2 6.4 system'
        expected_range =  {'end': 45, 'start': 0}
        actual_range = parse_run(resource('run_correct_order.txt'))['1']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('run_correct_order.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_of_second_topic(self):
        expected = '2 Q0 doc3 1 8 system\n2 Q0 doc4 2 5 system'
        expected_range =  {'end': 88, 'start': 46}
        actual_range = parse_run(resource('run_correct_order.txt'))['2']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('run_correct_order.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)
