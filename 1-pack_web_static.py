#!/usr/bin/python3
    """_summary_

    Returns:
        _type_: _description_
    """
    

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create the 'versions' directory if it doesn't exist"""
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
