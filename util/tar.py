import tarfile

def extract_tar(tar_file_path, extract_path='.'):
    """
    Extracts a tar file to the specified path.
    
    :param tar_file_path: Path to the tar file
    :param extract_path: Path to extract the files to (default: current directory)
    """
    try:
        with tarfile.open(tar_file_path, 'r:*') as tar:
            tar.extractall(path=extract_path)
        print(f"Successfully extracted '{tar_file_path}' to '{extract_path}'.")
    except tarfile.TarError as e:
        print(f"Error occurred while extracting tar file: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
