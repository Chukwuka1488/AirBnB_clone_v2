#!/usr/bin/python3
"""
This module automates the deployment process of web static content to web servers.
It contains the functions do_pack, do_deploy, and deploy, which work together to
create an archive from the web_static folder, upload it to the web servers, and
set up the web servers to serve the new content.

To execute the deployment, run the following command:
fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import isfile

env.hosts = ['xx-web-01', 'xx-web-02']
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' directory.

    The function creates the 'versions' directory if it doesn't exist and then
    generates a timestamped archive name. It proceeds to create the archive
    and returns the path to the archive if successful, or None if not.

    Returns:
        str: The path to the created archive if successful, otherwise None.
    """
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

def deploy():
    """
    Creates and deploys an archive to the web servers.

    This function calls do_pack to create an archive from the 'web_static'
    directory and then calls do_deploy to distribute and deploy the archive
    to the web servers. If the archive is not created, the function returns
    False.

    Returns:
        bool: True if the archive was created and deployed successfully,
              False otherwise.
    """
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)