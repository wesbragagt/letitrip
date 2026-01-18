# Let it Rip

## Description

This is a project that automates the process of ripping a DVD using MakeMKV and HandBrake through a Python script.

## Quick Start

### Rip a Movie
```bash
python3 letrip.py "Inception"
# Output: ./movies/Inception/Inception.mp4
```

### Rip a TV Show Season
```bash
python3 letrip.py "Friends" --type show --season 1
# Output: ./shows/Friends/Season 1/1_Friends.mp4
#         ./shows/Friends/Season 1/2_Friends.mp4
#         ./shows/Friends/Season 1/3_Friends.mp4
#         ...
```

### Multi-Disc TV Season
For seasons that span multiple discs, use `--start-episode` to continue numbering:
```bash
# Disc 1 (episodes 1-12)
python3 letrip.py "Friends" --type show --season 2
# Output: ./shows/Friends/Season 2/1_Friends.mp4 ... 12_Friends.mp4

# Disc 2 (episodes 13-24)
python3 letrip.py "Friends" --type show --season 2 --start-episode 13
# Output: ./shows/Friends/Season 2/13_Friends.mp4 ... 24_Friends.mp4
```

### Copy to External Drive
```bash
# Movie
python3 letrip.py "Inception" --copy ~/Movies
# Output: ~/Movies/Inception/Inception.mp4

# TV Show
python3 letrip.py "Friends" --type show --season 1 --copy /Volumes/Media/Shows
# Output: /Volumes/Media/Shows/Friends/Season 1/1_Friends.mp4 ...
```

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
2. Run the Python script with a title:

```bash
# Rip a movie
python3 letrip.py "MovieTitle"

# Rip a TV show (all episodes on disc)
python3 letrip.py "ShowName" --type show

# Rip a specific season
python3 letrip.py "ShowName" --type show --season 3

# Multi-disc season: start numbering at episode 13
python3 letrip.py "ShowName" --type show --season 3 --start-episode 13

# Copy output to another directory
python3 letrip.py "MovieTitle" --copy ~/Movies
python3 letrip.py "ShowName" --type show --season 2 --copy ~/Shows
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `title` | Title for the output file(s) | (required) |
| `--type` | Content type: `movie` or `show` | `movie` |
| `--season` | Season number for TV shows | `1` |
| `--start-episode` | Starting episode number (for multi-disc seasons) | `1` |
| `--copy` | Directory to copy the final file(s) to | (none) |

### Environment Variables

* `MIN_LENGTH` - Minimum length in seconds for tracks to rip (default: 900 seconds/15 minutes)

```bash
MIN_LENGTH=1200 python3 letrip.py "MovieTitle"
```

### How it works

1. The script cleans up temporary files in `/tmp/makemkv`
2. Uses MakeMKV to rip all tracks from the DVD to MKV format
3. Selects files to convert:
   - **Movies**: Selects the largest MKV file (typically the main feature)
   - **TV Shows**: Converts all MKV files, sorted by filename to preserve disc order
4. Converts to MP4 using HandBrake with optimized settings:
   - x264 encoder with CRF 22 (high quality)
   - 1920x1080 resolution
   - 23.976 fps frame rate
   - AAC audio encoding
5. Saves the output:
   - **Movies**: `./movies/[Title]/[Title].mp4`
   - **TV Shows**: `./shows/[Title]/Season [N]/[Episode]_[Title].mp4`

### Progress Tracking

The script displays real-time progress during the MakeMKV ripping process, including:
- Current completion percentage
- Estimated time remaining
