#! /bin/bash

# This is a simple script to update discord in my machine
# I'm assuming that 
# - Permissions are already set for the account running the script
# - Discord is installed in the same folder than flatpack did
# - No, flatpack is not installed (I removed it because it was not updating fast enough)
# - Link in the desktop was manually set to this folder/location
# - I'll try to post about this

# TODO Check if wget or curl is a better option
# TODO Use timestamp to avoid downloading again the same file
# TODO create a temp folder as an option 

discord_file="/tmp/discord.tar.gz"
install_path="/usr/share/discord"
download_path="https://discord.com/api/download/stable?platform=linux&format=tar.gz"

wget -O "$discord_file" --progress=bar  $download_path


# Fix issue with path
tar -xvzf "$discord_file" -C /tmp

cp -rf /tmp/Discord/* "$install_path"

# TODO Cleanup