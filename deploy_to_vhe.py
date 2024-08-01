#!/usr/bin/env python3

"""
Deploys source controlled files to the configured virtual headend.

This is intended for quick feedback during development only.
"""

import argparse
import subprocess


def main():
    """
    Application entrypoint.
    """
    parser = argparse.ArgumentParser(prog="PROG", description="Deployment tool.", conflict_handler="resolve")
    parser.add_argument("-b", "--branch", default="origin/main")
    args = parser.parse_args()

    branch_to_compare_against = args.branch
    # "192.168.199.164", "192.168.199.134"
    ip_addresses = [ "192.168.199.182"]
    
    changed_files = get_changed_files(branch_to_compare_against)
    print(f"Deploying the {len(changed_files)} files that were changed.")
    for ip_address in ip_addresses:
        print(f"Deploying changes files to the VHE at {ip_address}")
        
        for file in changed_files:
            copy_file_to_pi(file, ip_address)


def copy_file_to_pi(local_path, ip_address):
    """
    Copy the file to the remote VHE.

    Very limited in its knowledge of the correct destination.
    """
    
    remote_path = "/home/ubuntu/robot_ws/src/my_package/" + local_path if ip_address != "192.168.199.182" else "/home/yiming/dev_ws/src/my_package/" + local_path
    user_name = "ubuntu" if ip_address != "192.168.199.182" else "yiming"
    print(f"Deploying to {remote_path}")
    subprocess.check_output(["rsync", "--rsync-path=sudo rsync", local_path, f"{user_name}@{ip_address}:{remote_path}"])


def get_changed_files(branch_to_compare_against):
    """
    Get all files changed between current branch and the remote 'origin' master branch.
    """
    changed_files = subprocess.check_output(["git", "diff", branch_to_compare_against, "--name-only"])
    return changed_files.decode(encoding="utf-8").splitlines()



if __name__ == "__main__":
    main()
