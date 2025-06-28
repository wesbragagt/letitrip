# Let it Rip

## Description

This is a project that automates the process of ripping a DVD using MakeMKV and HandBrake through a Python script.

## Requirements

### Dependencies
* Python 3.x
* [MakeMKV](https://www.makemkv.com/)
* [HandBrake CLI](https://handbrake.fr/)

### Python Dependencies
The script uses only built-in Python modules:
* `subprocess` - for running external commands
* `os` - for file system operations
* `sys` - for system operations and command line arguments
* `time` - for time calculations and progress tracking
* `signal` - for handling interrupt signals

## Installation

### macOS

1. Install HandBrake CLI:
```bash
brew install handbrake
```

2. Install MakeMKV from the official website and create a symlink:
```bash
ln -s /Applications/MakeMKV.app/Contents/MacOS/makemkvcon /opt/homebrew/bin/makemkvcon
```

## Getting Started

1. Insert a DVD into your optical drive
2. Run the Python script with a movie title:

```bash
python3 letrip.py "MovieTitle"
```

### Environment Variables

* `MIN_LENGTH` - Minimum length in seconds for tracks to rip (default: 900 seconds/15 minutes)

```bash
MIN_LENGTH=1200 python3 letrip.py "MovieTitle"
```

### How it works

1. The script cleans up temporary files in `/tmp/makemkv`
2. Uses MakeMKV to rip all tracks from the DVD to MKV format
3. Selects the largest MKV file (typically the main movie)
4. Converts it to MP4 using HandBrake with optimized settings:
   - x264 encoder with CRF 22 (high quality)
   - 1920x1080 resolution
   - 23.976 fps frame rate
   - AAC audio encoding
5. Saves the final MP4 to `./movies/[MovieTitle]/[MovieTitle].mp4`

### Progress Tracking

The script displays real-time progress during the MakeMKV ripping process, including:
- Current completion percentage
- Estimated time remaining
