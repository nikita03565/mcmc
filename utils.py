import logging
import sys
from typing import List


def get_logger(name):
    logger = logging.Logger(name)
    handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger


def find_best_match(actual_results: List[str], expected: str) -> str:
    """
    Finds string from `actual_results` with most characters matching `expected` string
    """
    best_error = None
    best_result = None
    for result in actual_results:
        error = 0
        if len(result) != len(expected):
            raise ValueError("Strings lengths dont match")
        for actual_char, expected_char in zip(result.lower(), expected.lower()):
            if actual_char != expected_char:
                error += 1
        if best_error is None or best_error > error:
            best_error = error
            best_result = result

    return best_result
