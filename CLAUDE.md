# CLAUDE.md

## Project Overview

Let it Rip - A DVD ripping and conversion automation tool for macOS. Converts DVDs to MP4 using MakeMKV and HandBrake CLI.

## Quick Commands

```bash
# Rip a movie
uv run python letrip.py "MovieTitle"

# Rip with copy destination
uv run python letrip.py "MovieTitle" --copy ~/Movies

# Rip a TV show (Season 1)
uv run python letrip.py "ShowName" --type show

# Rip TV show with specific season
uv run python letrip.py "ShowName" --type show --season 3

# Multi-disc season: disc 2 starting at episode 13
uv run python letrip.py "ShowName" --type show --season 3 --start-episode 13

# TV show with copy destination
uv run python letrip.py "ShowName" --type show --season 2 --copy ~/Shows

# Set minimum track length (seconds)
MIN_LENGTH=600 uv run python letrip.py "MovieTitle"
```

## Development

```bash
# Run all quality checks (lint, type check, tests)
./test.sh

# Or run individually
uv run ruff check        # Linting
uv run pyright           # Type checking
uv run pytest -vv        # Tests
```

## Project Structure

- `letrip.py` - Main script, orchestrates DVD-to-MP4 workflow
- `parse_progress.py` - Utility for parsing MakeMKV progress output
- `tests/test_letrip.py` - Test suite
- `movies/` - Output directory for converted movies (gitignored)
- `shows/` - Output directory for converted TV shows (gitignored)

## External Dependencies

- MakeMKV (`makemkvcon`) - Rips DVD to MKV
- HandBrake CLI (`HandBrakeCLI`) - Converts MKV to MP4

## Output

Movies: `./movies/[MovieTitle]/[MovieTitle].mp4`

TV Shows: `./shows/[ShowName]/Season [N]/[Episode]_[ShowName].mp4`
