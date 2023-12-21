import importlib
# load construct indexes from ../construct_indexes.py
parse_topics = importlib.import_module('construct_indexes').parse_topics
extract_from_file = importlib.import_module('construct_indexes').extract_from_file
import unittest
import os

def resource(f):
    return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + f

class TestParsingOfTopics(unittest.TestCase):
    def test_parsing_of_qrels_for_non_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_topics('path does not exist.')

    def test_parsing_of_queries_with_duplicates(self):
        with self.assertRaises(ValueError):
            parse_topics(resource('queries_with_duplicates.jsonl'))

    def test_parsing_of_queries_without_duplicates(self):
        expected = {"1": {"start": 0, "end": 55}, "2": {"start": 55, "end": 97}, "3": {"start": 97, "end": 140}}
        actual = parse_topics(resource('queries_without_duplicates.jsonl'))
        self.assertEqual(expected, actual)

    def test_extraction_of_first_topic(self):
        expected = '{"qid": "1", "query": "hubble telescope achievements"}'
        expected_range =  {'end': 55, 'start': 0}
        actual_range = parse_topics(resource('queries_without_duplicates.jsonl'))['1']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('queries_without_duplicates.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_of_second_topic(self):
        expected = '{"qid": "2", "query": "how to exit vim?"}'
        expected_range =  {'end': 97, 'start': 55}
        actual_range = parse_topics(resource('queries_without_duplicates.jsonl'))['2']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('queries_without_duplicates.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_of_third_topic(self):
        expected = '{"qid": "3", "query": "signs heart attack"}'
        expected_range =  {'end': 140, 'start': 97}
        actual_range = parse_topics(resource('queries_without_duplicates.jsonl'))['3']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('queries_without_duplicates.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)