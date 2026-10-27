"""
This module provides utility functions used throughout the project.
These include [functionality of the module, e.g., file I/O, data processing].

Example:
    Describe how to use module, if applicable.

Functions:
    * read_file - Reads a file in chunks.
    * another_function - [Description of another function].

"""


def read_file(file_to_read, chunk_size=5242880):
    """
    Generator function to read a file in chunks.

    Args:
        file_to_read (str): Path to the file to read.
        chunk_size (int, optional): Size of chunks to read in bytes.
        Defaults to 5 MB.

    Yields:
        bytes: Chunks of file contents.
    """

    # The 'with' statement is used here to ensure that the file is properly
    # closed after its suite finishes. 'rb' means the file is opened for
    # reading in binary mode. This is crucial for non-text files like audio
    # files.
    with open(file_to_read, "rb") as _file:
        # The 'while' loop continues to read the file in chunks until
        # there is nothing left to read.
        while True:
            # Read 'chunk_size' bytes of the file. If the file size
            # is not a multiple of 'chunk_size', the final chunk will
            # be smaller than 'chunk_size' bytes.
            data = _file.read(chunk_size)

            # 'if not data' is True when the end of the file is reached
            # and 'data' is an empty bytes object. In this case, the
            # loop breaks and the function stops yielding data.
            if not data:
                break

            # If data was read, it is yielded to the caller. This allows
            # the function to start reading the next chunk while the
            # caller is processing the current one, which can lead to
            # performance improvements, especially for large files.
            yield data
