def parse_progress(line: str):
    """
    Parses progress output from MakeMKV.
    Example:

    PRGV:40270,20467,65536
    PRGV:40285,20467,65536
    PRGV:40285,20474,65536
    PRGV:40343,20474,65536
    """
    if line.startswith('PRGV:'):
        values = line.split(':')[1].split(',')
        value1, value2, max_value = map(int, values)
        percentage1 = (value1 / max_value) * 100
        percentage2 = (value2 / max_value) * 100
        return percentage1, percentage2
    else:
        return line
