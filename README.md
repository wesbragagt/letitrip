# Let it Rip

## Description

This is a project that automates the process of ripping a dvd using MakeMKV and Handbreak through one simple script.

## Requirements

* [MakeMKV](https://www.makemkv.com/)
* [Handbrake](https://handbrake.fr/)

## MacOS

### Install Handbrake CLI

```
brew install handbrake
```

Make sure that you create a symlink for the makemkvcon binary located in the /Applications/MakeMKV.app/Contents/MacOS/makemkvcon. 

```bash
ln -s /Applications/MakeMKV.app/Contents/MacOS/makemkvcon /opt/homebrew/bin/makemkvcon
```

## Quick Start

1. Insert a DVD into an optical drive.
2. Locate the drive path by running the following command:

```bash
# MacOS
mount

# Linux
lsblk
```

3. Run the script with the drive path as an argument:

```bash
bash let-it-rip.sh /dev/disk4 '~/Movies/PolarExpress'

```

The command will create a folder named 'PolarExpress' in the Movies directory if it doesn't exist and rip the DVD to that folder in a mp4 i.e PolarExpress.mp4
