#!/usr/bin/python3
"""
This module provides a Fabric script to clean up old archives from both the local
'versions' directory and the '/data/web_static/releases' directory on specified
web servers. It allows keeping a specified number of the most recent archives and
deleting the rest.

Usage:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""


from fabric.api import *
from os import path

# Define the IP addresses of the web servers
env.hosts = ['<IP web-01>', '<IP web-02>']
# Uncomment and set the user and SSH key if needed
# env.user = 'ubuntu'
# env.key_filename = 'my_ssh_private_key'


def do_clean(number=0):
    """
    Cleans up out-of-date archives.

    This function keeps the specified number of the most recent archives in the
    'versions' directory and the '/data/web_static/releases' directory on the
    web servers, deleting any others that are considered out-of-date.

    Args:
        number (int): The number of archives to keep. If number is 0 or 1, only
                      the most recent archive is kept. If number is 2, the most
                      recent and the second-most recent archives are kept, etc.

    Returns:
        None
    """
    # Convert the number argument to an integer
    number = int(number)

    # If number is 0 or 1, keep only the most recent version of the archive
    if number == 0 or number == 1:
        number = 1

    # List all archives in the 'versions' directory and sort them
    archives = sorted(os.listdir("versions"))
    # Remove the most recent archives based on the specified number
    [archives.pop() for i in range(number)]
    # Delete the remaining out-of-date archives locally
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Perform the same cleanup on the web servers
    with cd("/data/web_static/releases"):
        # List and filter archives in the releases directory
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        # Remove the most recent archives based on the specified number
        [archives.pop() for i in range(number)]
        # Delete the remaining out-of-date archives on the web servers
        [run("rm -rf ./{}".format(a)) for a in archives]