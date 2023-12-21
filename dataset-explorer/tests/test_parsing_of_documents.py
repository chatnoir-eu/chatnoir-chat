import importlib
# load construct indexes from ../construct_indexes.py
parse_documents = importlib.import_module('construct_indexes').parse_documents
extract_from_file = importlib.import_module('construct_indexes').extract_from_file
import unittest
import os

def resource(f):
    return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + f

class TestParsingOfQrels(unittest.TestCase):
    def test_parsing_of_documents_for_non_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_documents('path does not exist.')

    def test_parsing_of_documents_for_file_with_duplicates(self):
        with self.assertRaises(ValueError):
            parse_documents(resource('documents_with_duplicates.jsonl'))

    def test_parsing_of_documents(self):
        expected = {
            'doc-1': {'start': 0, 'end': 150},
            'doc-2': {'start': 150, 'end': 282},
            'doc-3': {'start': 282, 'end': 379},
            'doc-4': {'start': 379, 'end': 542},
            'doc-5': {'start': 542, 'end': 742},
            'doc-6': {'start': 742, 'end': 884}
        }
        actual = parse_documents(resource('documents.jsonl'))
        self.assertEqual(expected, actual)

    def test_extraction_first_document(self):
        expected = '{"docno": "doc-1", "text": "Press ESC key, then the : (colon), and type the wq command after the colon and hit the Enter key to save and leave Vim."}'
        expected_range = {'start': 0, 'end': 150}
        actual_range = parse_documents(resource('documents.jsonl'))['doc-1']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('documents.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_fifth_document(self):
        expected = '{"docno": "doc-5", "text": "Common heart attack symptoms include: (1) Chest pain, (2) Pain or discomfort that spreads to the shoulder, arm, back, neck, jaw, teeth or sometimes the upper belly, etc."}'
        expected_range = {'start': 542, 'end': 742}
        actual_range = parse_documents(resource('documents.jsonl'))['doc-5']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('documents.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)

    def test_extraction_sixt_document(self):
        expected = '{"docno": "doc-6", "text": "A heart attack happens when the flow of blood that brings oxygen to your heart muscle suddenly becomes blocked. "}'
        expected_range = {'start': 742, 'end': 884}
        actual_range = parse_documents(resource('documents.jsonl'))['doc-6']
        self.assertEqual(expected_range, actual_range)

        actual = extract_from_file(resource('documents.jsonl'), expected_range['start'], expected_range['end'])
        self.assertEqual(expected, actual)