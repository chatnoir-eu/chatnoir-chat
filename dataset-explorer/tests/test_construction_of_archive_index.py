import importlib
# load construct indexes from ../construct_indexes.py
process_archive = importlib.import_module('construct_indexes').process_archive
ArchivedDataset = importlib.import_module('construct_indexes').ArchivedDataset
ArchivedRun = importlib.import_module('construct_indexes').ArchivedRun
import unittest
from approvaltests.approvals import verify_as_json
import os

def resource(f):
    return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + f


class TestConstructionOfArchiveIndex(unittest.TestCase):
    def test_on_small_example(self):
        dataset = ArchivedDataset(
            qrels_url='url-here',
            qrels_local_copy=resource('qrels_correct_order.txt'),
            topics_url='url-here',
            topics_local_copy=resource('queries_without_duplicates.jsonl'),
            documents_url='url-here',
            documents_local_copy=resource('documents.jsonl'),
            runs=[ArchivedRun('run-1', 'url-here', resource('run_correct_order.txt'))]
        )
        actual = process_archive(dataset)
        verify_as_json(actual)
