import importlib
# load construct indexes from ../construct_indexes.py
construct_indexes = importlib.import_module('construct_indexes').parse_qrels
extract_from_file = importlib.import_module('construct_indexes').extract_from_file
import unittest
import os

def resource(f):
    return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + f

class TestParsingOfQrels(unittest.TestCase):
    def test_parsing_of_qrels_for_non_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            construct_indexes('path does not exist.')

    def test_parsing_of_qrels_for_empty_file(self):
        expected = {}
        actual = construct_indexes(resource('qrels_empty.txt'))
        self.assertEqual(expected, actual)

    def test_parsing_of_qrels_for_unsorted_file(self):
        with self.assertRaises(ValueError):
            construct_indexes(resource('qrels_incorrect_order.txt'))

    def test_parsing_of_qrels_correct_file(self):
        expected = {'q1': {'end': 29, 'start': 0}, 'q2': {'end': 49, 'start': 30}}
        actual = construct_indexes(resource('qrels_correct_order.txt'))
        self.assertEqual(expected, actual)

    def test_extraction_first_qrels(self):
        expected = 'q1 0 d1 1\nq1 0 d2 0\nq1 0 d3 1'
        actual = extract_from_file(resource('qrels_correct_order.txt'), 0, 29)
        self.assertEqual(expected, actual)

    def test_extraction_second_qrels(self):
        expected = 'q2 0 d5 0\nq2 0 d6 1'
        actual = extract_from_file(resource('qrels_correct_order.txt'), 30, 49)
        self.assertEqual(expected, actual)

    def test_parsing_of_qrels_correct_file_larger(self):
        expected = {'q1': {'end': 29, 'start': 0}, 'q2': {'end': 49, 'start': 30}, 'q3': {'end': 59, 'start': 50}, 'q4': {'end': 79, 'start': 60}, 'q5': {'end': 89, 'start': 80}}
        actual = construct_indexes(resource('qrels_correct_order_larger.txt'))
        self.assertEqual(expected, actual)

    def test_extraction_first_qrels_from_larger(self):
        expected = 'q1 0 d1 1\nq1 0 d2 0\nq1 0 d3 1'
        expected_range = {'end': 29, 'start': 0}
        actual_range = construct_indexes(resource('qrels_correct_order_larger.txt'))['q1']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('qrels_correct_order_larger.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_second_qrels_from_larger(self):
        expected = 'q2 0 d5 0\nq2 0 d6 1'
        expected_range =  {'end': 49, 'start': 30}
        actual_range = construct_indexes(resource('qrels_correct_order_larger.txt'))['q2']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('qrels_correct_order_larger.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_third_qrels_from_larger(self):
        expected = 'q3 0 d1 1'
        expected_range =  {'end': 59, 'start': 50}
        actual_range = construct_indexes(resource('qrels_correct_order_larger.txt'))['q3']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('qrels_correct_order_larger.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_fourth_qrels_from_larger(self):
        expected = 'q4 0 d2 1\nq4 0 d1 1'
        expected_range =  {'end': 79, 'start': 60}
        actual_range = construct_indexes(resource('qrels_correct_order_larger.txt'))['q4']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('qrels_correct_order_larger.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_fifth_qrels_from_larger(self):
        expected = 'q5 0 d1 1'
        expected_range =  {'end': 89, 'start': 80}
        actual_range = construct_indexes(resource('qrels_correct_order_larger.txt'))['q5']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('qrels_correct_order_larger.txt'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)