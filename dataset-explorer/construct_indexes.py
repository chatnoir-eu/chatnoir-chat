#!/usr/bin/env python3
from pathlib import Path
import json

DATASET_IDS = ['argsme-touche-2020-task-1-20230209-training']
CORPUS = []
from pathlib import Path
from typing import Dict, NamedTuple, List


def extract_from_file(path: Path, start: int, end: int) -> str:
    """
    Extracts the content of a file between the given start and end byte range.

    :param path: Path to the file
    :param start: Start byte range
    :param end: End byte range
    :return: Content of the file between the given byte range
    """
    with open(path, "rb") as file:
        file.seek(start)
        return file.read(end - start).decode('utf-8').strip()

def parse_qrels(path: Path) -> Dict:
    """
    Parses a qrel file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the qrel file
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}
    current_qrel = None
    covered_qrels = set()

    with open(path, "rb") as file:
        start = file.tell()
        end_position = 0

        for _, line in enumerate(file):
            q = line.decode().split()[0].strip()
            if not q:
                continue

            if current_qrel is None:
                current_qrel = q
            print(q)
            if q != current_qrel and q in covered_qrels:
                raise ValueError(f'Qrel file is not sorted by topic id. Found multiple occurrences of {q}')

            covered_qrels.add(q)

            if q != current_qrel:
                ret[current_qrel] = {'start': start, 'end': end_position}
                current_qrel = q
                start = end_position + 1
            
            end_position = file.tell() -1

        if current_qrel is not None:
            ret[current_qrel] = {'start': start, 'end': file.tell()}

    return ret

def parse_topics(path: Path) -> Dict:
    """
    Parses a topics file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the topics file in jsonl format as used in TIREx
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}

    with open(path, "rb") as file:
        position = file.tell()

        for _, line in enumerate(file):
            q = json.loads(line.decode())['qid']
            
            if q is None or q in ret:
                raise ValueError(f'Topic contains duplicate or null query ids. Got {q}')

            ret[q] = {'start': position, 'end': file.tell()}
            position = file.tell()

    return ret

def parse_documents(path: Path) -> Dict:
    """
    Parses a documents file and returns a dictionary with the document id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the document file in jsonl format as used in TIREx
    :return: Dictionary with the document id as key and the byte range as value
    """
    ret = {}

    with open(path, "rb") as file:
        position = file.tell()

        for _, line in enumerate(file):
            q = json.loads(line.decode())['docno']
            
            if q is None or q in ret:
                raise ValueError(f'Documents contains duplicate or null document ids. Got {q}')

            ret[q] = {'start': position, 'end': file.tell()}
            position = file.tell()

    return ret

def parse_run(path: Path) -> Dict:
    """
    Parses a topics file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    
    :param path: Path to the run file
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}
    current_query_id = None
    covered_query_ids = set()

    with open(path, "rb") as file:
        start = file.tell()
        end_position = 0

        for _, line in enumerate(file):
            q = line.decode().split()[0].strip()
            if not q:
                continue

            if current_query_id is None:
                current_query_id = q
            print(q)
            if q != current_query_id and q in covered_query_ids:
                raise ValueError(f'Qrel file is not sorted by topic id. Found multiple occurrences of {q}')

            covered_query_ids.add(q)

            if q != current_query_id:
                ret[current_query_id] = {'start': start, 'end': end_position}
                current_query_id = q
                start = end_position + 1
            
            end_position = file.tell() -1

        if current_query_id is not None:
            ret[current_query_id] = {'start': start, 'end': file.tell()}

    return ret

class ArchivedRun(NamedTuple):
    name: str
    url: str
    local_copy: Path


class ArchivedDataset(NamedTuple):
    qrels_url: str
    qrels_local_copy: Path
    topics_url: str
    topics_local_copy: Path
    documents_url: str
    documents_local_copy: Path
    runs: List[ArchivedRun]


def process_archive(archive_dataset: ArchivedDataset):
    pass
