# --- sub2_delete.py ---
import os
import logging
from sub_system import request_approval

def delete_file(filepath):
    """Deletes a file after approval."""
    try:
        if os.path.exists(filepath):
            request_approval(f"Request to delete file: {filepath}")
            os.remove(filepath)
            logging.info(f"File deleted: {filepath}")
            return True
        else:
            logging.warning(f"File not found: {filepath}")
            return False
    except Exception as e:
        logging.error(f"Error deleting file {filepath}: {e}")
        request_approval(f"Error deleting file {filepath}: {e}. Awaiting Approval.")
        return False

def delete_directory(dirpath):
    """Deletes a directory after approval."""
    try:
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            request_approval(f"Request to delete directory: {dirpath}")
            os.rmdir(dirpath)
            logging.info(f"Directory deleted: {dirpath}")
            return True
        else:
            logging.warning(f"Directory not found or not a directory: {dirpath}")
            return False
    except Exception as e:
        logging.error(f"Error deleting directory {dirpath}: {e}")
        request_approval(f"Error deleting directory {dirpath}: {e}. Awaiting Approval.")
        return False

def delete_multiple_files(filelist):
    """Deletes multiple files after approval."""
    deleted_files = []
    for filepath in filelist:
        if delete_file(filepath):
            deleted_files.append(filepath)
    return deleted_files

def delete_multiple_directories(dirlist):
    """Deletes multiple directories after approval."""
    deleted_dirs = []
    for dirpath in dirlist:
        if delete_directory(dirpath):
            deleted_dirs.append(dirpath)
    return deleted_dirs

def delete_all_files_in_directory(dirpath):
    """Deletes all files within a directory after approval."""
    try:
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            files_to_delete = [os.path.join(dirpath, f) for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
            return delete_multiple_files(files_to_delete)
        else:
            logging.warning(f"Directory not found or not a directory: {dirpath}")
            return []
    except Exception as e:
        logging.error(f"Error deleting files in directory {dirpath}: {e}")
        request_approval(f"Error deleting files in directory {dirpath}: {e}. Awaiting Approval.")
        return []

def delete_all_directories_in_directory(dirpath):
    """Deletes all directories within a directory after approval."""
    try:
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            dirs_to_delete = [os.path.join(dirpath, d) for d in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, d))]
            return delete_multiple_directories(dirs_to_delete)
        else:
            logging.warning(f"Directory not found or not a directory: {dirpath}")
            return []
    except Exception as e:
        logging.error(f"Error deleting directories in directory {dirpath}: {e}")
        request_approval(f"Error deleting directories in directory {dirpath}: {e}. Awaiting Approval.")
        return []
