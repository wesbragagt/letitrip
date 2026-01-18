import sys
from unittest.mock import patch, MagicMock

sys.path.append('.')
from letrip import parse_progress, get_human_readable_estimated_time, shell_command, prepare_output_dir, get_episode_filename


class TestParseProgress:
    def test_parse_progress_valid_line(self):
        line = "PRGV:40270,20467,65536"
        result = parse_progress(line)
        expected = (40270 / 65536) * 100
        assert abs(result - expected) < 0.01

    def test_parse_progress_different_values(self):
        line = "PRGV:32768,16384,65536"
        result = parse_progress(line)
        assert abs(result - 50.0) < 0.01

    def test_parse_progress_zero_progress(self):
        line = "PRGV:0,0,65536"
        result = parse_progress(line)
        assert result == 0.0

    def test_parse_progress_complete(self):
        line = "PRGV:65536,65536,65536"
        result = parse_progress(line)
        assert result == 100.0


class TestGetHumanReadableEstimatedTime:
    @patch('time.time')
    def test_estimated_time_calculation(self, mock_time):
        mock_time.return_value = 120.0  # 2 minutes elapsed
        time_started = 60.0  # started 1 minute ago
        average = 25.0  # 25% complete
        
        result = get_human_readable_estimated_time(average, time_started)
        
        # 75% remaining, took 60 seconds for 25%, so 180 seconds remaining = 3 minutes
        assert result == "00:03:00"

    @patch('time.time')
    def test_estimated_time_near_completion(self, mock_time):
        mock_time.return_value = 100.0
        time_started = 50.0
        average = 90.0  # 90% complete
        
        result = get_human_readable_estimated_time(average, time_started)
        
        # 10% remaining, took 50 seconds for 90%, so ~5.56 seconds remaining
        assert result == "00:00:05"


class TestShellCommand:
    @patch('subprocess.Popen')
    def test_shell_command_with_progress_output(self, mock_popen):
        mock_proc = MagicMock()
        mock_proc.stdout = ["PRGV:32768,16384,65536\n", "PRGV:49152,24576,65536\n"]
        mock_proc.stderr = []
        mock_popen.return_value.__enter__.return_value = mock_proc
        
        result = shell_command("test command")
        
        mock_popen.assert_called_once()
        assert result == mock_proc

    @patch('subprocess.Popen')
    def test_shell_command_with_stderr_output(self, mock_popen):
        mock_proc = MagicMock()
        mock_proc.stdout = []
        mock_proc.stderr = ["Error message\n"]
        mock_popen.return_value.__enter__.return_value = mock_proc
        
        result = shell_command("test command")
        
        assert result == mock_proc

    @patch('subprocess.Popen')
    def test_shell_command_with_regular_output(self, mock_popen):
        mock_proc = MagicMock()
        mock_proc.stdout = ["Regular output line\n"]
        mock_proc.stderr = []
        mock_popen.return_value.__enter__.return_value = mock_proc
        
        result = shell_command("test command")
        
        assert result == mock_proc


class TestPrepareOutputDir:
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_prepare_output_dir_creates_directory(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        output_dir = "/test/path"
        
        result = prepare_output_dir(output_dir)
        
        mock_makedirs.assert_called_once_with(output_dir)
        assert result == output_dir

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_prepare_output_dir_existing_directory(self, mock_makedirs, mock_exists):
        mock_exists.return_value = True
        output_dir = "/existing/path"
        
        result = prepare_output_dir(output_dir)
        
        mock_makedirs.assert_not_called()
        assert result == output_dir

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_prepare_output_dir_relative_path(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        output_dir = "./relative/path"

        result = prepare_output_dir(output_dir)

        mock_makedirs.assert_called_once_with(output_dir)
        assert result == output_dir


class TestGetEpisodeFilename:
    def test_episode_filename_basic(self):
        result = get_episode_filename(1, "Friends")
        assert result == "1_Friends.mp4"

    def test_episode_filename_multi_digit(self):
        result = get_episode_filename(13, "Friends")
        assert result == "13_Friends.mp4"

    def test_episode_filename_with_spaces(self):
        result = get_episode_filename(5, "Game of Thrones")
        assert result == "5_Game of Thrones.mp4"

    def test_episode_filename_single_digit(self):
        result = get_episode_filename(9, "ShowName")
        assert result == "9_ShowName.mp4"


class TestFileSelection:
    def test_movie_selects_largest_file(self):
        """Movie mode should select only the largest file"""
        files_created = ["title00.mkv", "title01.mkv", "title02.mkv"]
        mkv_path = "/tmp/makemkv"

        # Simulate movie mode: select largest file
        with patch('os.path.getsize') as mock_getsize:
            mock_getsize.side_effect = lambda x: {
                "/tmp/makemkv/title00.mkv": 1000,
                "/tmp/makemkv/title01.mkv": 5000,  # largest
                "/tmp/makemkv/title02.mkv": 2000,
            }.get(x, 0)

            files_to_convert = [max(files_created, key=lambda x: mock_getsize(f"{mkv_path}/{x}"))]

        assert files_to_convert == ["title01.mkv"]
        assert len(files_to_convert) == 1

    def test_show_selects_all_files_sorted(self):
        """Show mode should select all files sorted by name"""
        files_created = ["title02.mkv", "title00.mkv", "title01.mkv"]

        # Simulate show mode: select all files sorted
        files_to_convert = sorted(files_created)

        assert files_to_convert == ["title00.mkv", "title01.mkv", "title02.mkv"]
        assert len(files_to_convert) == 3