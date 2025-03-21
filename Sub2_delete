"""
Sub2_delete Module

This module provides functions for deleting files and directories, both individually
and based on filename patterns. It includes error handling and integrates with an
alerting system for notifications in case of failures.

Functions:
    delete_files(file_paths, alertmanager_url=None): Deletes specified files or directories.
    delete_files_by_pattern(directory, pattern, alertmanager_url=None): Deletes files matching a pattern.
"""

import logging
import os
import shutil

from sub_system import shutdown

def delete_files(file_paths, alertmanager_url=None):
    """
    Deletes specified files or directories.

    Args:
        file_paths (list): A list of file or directory paths to delete.
        alertmanager_url (str, optional): URL of Alertmanager for notifications. Defaults to None.

    Raises:
        Exception: If an error occurs during deletion, logs the error and triggers a shutdown.
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    logging.info(f"File deleted: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    logging.info(f"Directory deleted: {path}")
                else:
                    logging.warning(f"Path is neither a file nor a directory: {path}")
            else:
                logging.warning(f"Path does not exist: {path}")
        except Exception as e:
            logging.error(f"Error deleting {path}: {e}")
            shutdown(f"Error deleting {path}: {e}", alertmanager_url, severity="error", grouping_key="file_deletion")

def delete_files_by_pattern(directory, pattern, alertmanager_url=None):
    """
    Deletes files in a directory that match a given pattern.

    Args:
        directory (str): The directory to search for files.
        pattern (str): The pattern to match filenames against.
        alertmanager_url (str, optional): URL of Alertmanager for notifications. Defaults to None.

    Raises:
        Exception: If an error occurs during deletion, logs the error and triggers a shutdown.
    """
    try:
        if not os.path.exists(directory):
            logging.warning(f"Directory does not exist: {directory}")
            return

        for filename in os.listdir(directory):
            if pattern in filename:
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"File deleted: {file_path}")
                else:
                    logging.warning(f"Matched item is not a file: {file_path}")
    except Exception as e:
        logging.error(f"Error deleting files in {directory}: {e}")
        shutdown(f"Error deleting files in {directory}: {e}", alertmanager_url, severity="error", grouping_key="file_pattern_deletion")

if __name__ == "__main__":
    # Example usage (for testing purposes)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Example 1: Deleting specific files/directories
    files_to_delete = ["test_file.txt", "test_directory"]
    for file in files_to_delete:
        if not os.path.exists(file):
            open(file,'a').close()

    if not os.path.exists("test_directory"):
        os.makedirs("test_directory")

    delete_files(files_to_delete)

    # Example 2: Deleting files by pattern
    if not os.path.exists("test_pattern_dir"):
        os.makedirs("test_pattern_dir")

    for i in range(5):
        with open(f"test_pattern_dir/file_{i}_pattern.txt", "w") as f:
            f.write("test content")

    delete_files_by_pattern("test_pattern_dir", "pattern")
