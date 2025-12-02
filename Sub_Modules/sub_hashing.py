"""
Sub_hashing Module

This module provides a function for generating SHA-256 hashes of input strings.

Functions:
    generate_sha256_hash(input_string): Generates a SHA-256 hash of the input string.
"""

import hashlib
import logging

def generate_sha256_hash(input_string):
    """
    Generates a SHA-256 hash of the input string.

    Args:
        input_string (str): The string to be hashed.

    Returns:
        str: The SHA-256 hash of the input string, or None if an error occurs.
    """
    try:
        sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
        return sha256_hash
    except Exception as e:
        logging.error(f"Error generating SHA-256 hash: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    test_string = "This is a test string"
    hash_value = generate_sha256_hash(test_string)
    if hash_value:
        print(f"SHA-256 hash of '{test_string}': {hash_value}")
