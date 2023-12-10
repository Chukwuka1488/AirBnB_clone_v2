#!/usr/bin/python3
"""
This module automates the deployment of web static content to web servers.
It contains the do_deploy function which, given the path to an archive file,
will distribute and deploy the contents to the specified web servers.
"""

from fabric.api import env, put, run, local
from os.path import isfile

env.hosts = ['xx-web-01', 'xx-web-02']
# env.user = 'ubuntu'
# env.key_filename = 'my_ssh_private_key'

def do_deploy(archive_path):
    """
    Deploys the web static content to the web servers.

    This function takes an archive path, checks if the file exists, and then
    proceeds to upload, uncompress, and deploy the content to the specified
    web servers. It also updates the symbolic link to point to the new version
    of the content.

    Args:
        archive_path (str): The path to the .tgz archive to be deployed.

    Returns:
        bool: True if the deployment succeeded, False otherwise.
    """
    # Check if the archive_path exists and is a file
    if not isfile(archive_path):
        return False

    # Extract the archive filename without extension
    archive_filename = archive_path.split("/")[-1]
    archive_wo_ext = archive_filename.split(".")[0]

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/{}".format(archive_filename))

    # Uncompress the archive to the folder on the web server
    release_dir = "/data/web_static/releases/{}".format(archive_wo_ext)
    run("mkdir -p {}".format(release_dir))
    run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_dir))

    # Delete the archive from the web server
    run("rm /tmp/{}".format(archive_filename))

    # Move the content out from the archive folder to its parent
    run("mv {0}/web_static/* {0}/".format(release_dir))
    run("rm -rf {}/web_static".format(release_dir))

    # Delete the symbolic link from the web server
    run("rm -rf /data/web_static/current")

    # Create a new symbolic link on the web server
    run("ln -s {} /data/web_static/current".format(release_dir))

    print("New version deployed!")
    return True