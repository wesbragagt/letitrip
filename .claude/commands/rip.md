---
description: Rip a DVD to MP4 format
model: claude-haiku-4-5-20250514
arguments:
  - name: name
    description: Movie or show name
    required: true
  - name: output
    description: Output folder location (optional)
    required: false
---

Before running the ripper, use WebSearch to look up "$name" to find the official movie or show title. Use the properly formatted title (with correct capitalization and punctuation) for the output filename.

Run the DVD ripper with the corrected title:

```bash
{{#if output}}
MIN_LENGTH=1200 uv run python letrip.py "<corrected_title>" --copy "$output"
{{else}}
MIN_LENGTH=1200 uv run python letrip.py "<corrected_title>"
{{/if}}
```

The output will be saved to `./movies/<title>/<title>.mp4`{{#if output}} and copied to `$output/<title>/<title>.mp4`{{/if}}.
