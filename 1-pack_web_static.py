#!/usr/bin/python3
"""
This module contains the function do_pack which generates a .tgz archive from
the contents of the web_static folder. The archive is stored in the 'versions'
directory and named with a timestamp indicating when it was created.
"""


from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' directory.

    The function first ensures that the 'versions' directory exists and then
    generates a timestamped archive name. It proceeds to create the archive
    and returns the path to the archive if successful, or None if not.

    Returns:
        str: The path to the created archive if successful, otherwise None.
    """
    # Create the 'versions' directory if it doesn't exist
    local("mkdir -p versions")

    # Generate a timestamped archive name
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time_stamp)

    # Create archive
    archive_created = local("tar -cvzf {} web_static".format(archive_path))

    # Return the archive path if the archive has been correctly generated
    if archive_created.succeeded:
        return archive_path
    else:
        return None
