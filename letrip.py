import time
import subprocess
import os
import sys
import signal
import argparse
import shutil

class TransformToMp4Error(Exception):
    def __init__(self):
        super().__init__("Error when using Handbrake to convert the file to mp4")


def usage():
    print("Usage: python3 letrip.py <title> [--copy <destination_directory>]")

def parse_progress(line: str):
    """
    Parses progress output from MakeMKV.
    Example:

    PRGV:40270,20467,65536
    PRGV:40285,20467,65536
    PRGV:40285,20474,65536
    PRGV:40343,20474,65536
    """
    values = line.split(':')[1].split(',')
    value1, value2, max_value = map(int, values)
    percentage = (value1 / max_value) * 100

    return percentage

def get_human_readable_estimated_time(average: float, time_started: float):
    """
    Returns HH:MM:SS format of the estimated time remaining
    """
    estimated_time = (100 - average) * (time.time() - time_started) / average
    output = time.strftime("%H:%M:%S", time.gmtime(estimated_time))

    return output



def shell_command(command: str, retries = 3):
    time_started = time.time()
    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    ) as proc:
        stdout = proc.stdout
        if stdout:
            percentages = []
            for line in stdout:
                if line.startswith('PRGV:'):
                    percentage = parse_progress(line)
                    if percentage > 0 and percentage < 100:
                        percentages.append(percentage)
                        average = sum(percentages) / len(percentages)
                        estimated_time = get_human_readable_estimated_time(average, time_started)
                        print(f'\rProgress: {percentage:.2f}%, Estimated time remaining: {estimated_time}\r', end='')

                    else:
                        percentages = []
                        print(f'\rProgress: {percentage:.2f}%', end='')
                    
                else:
                    print(line)

        stderr = proc.stderr
        if stderr:
            for line in stderr:
                print(line)

        return proc


def prepare_output_dir(output_dir: str) -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # return the full path of the output directory
    return output_dir


def main(mp4_movie_name: str, min_length: int, copy_to: str = None):
    """
    The command will create a folder named 'PolarExpress' in the movies directory if it doesn't exist and rip the DVD to that folder in a mp4 i.e PolarExpress.mp4
    """
    # Clean up /tmp/makemkv
    exit_code = os.system("rm -rf /tmp/makemkv")

    if exit_code != 0:
        raise Exception("Failed to clean up /tmp/makemkv")

    # Rip DVD using makemkvcon first
    mkv_path = prepare_output_dir("/tmp/makemkv")

    shell_command(f"makemkvcon mkv disc:0 all '{mkv_path}' --minlength {min_length} --progress=-same --robot --debug")

    files_created = os.listdir(mkv_path)

    print(f"Files created by MakeMKV: {files_created}")

    # Convert the largest mkv file to mp4 using Handbrake
    largest_file = max(files_created, key=lambda x: os.path.getsize(os.path.join(mkv_path, x)))
    mkv_file = os.path.join(mkv_path, largest_file)

    print(f"Converting {mkv_file} to mp4")

    output_dir = prepare_output_dir(f"./movies/{mp4_movie_name}")
    mp4_file_path = os.path.join(output_dir, f"{mp4_movie_name}.mp4")
    
    """
    -e x264: Uses the x264 encoder
    -q 22.0: Sets the Constant Rate Factor (CRF) to 22, which aims for high quality
    -r 23.976: Sets the frame rate to 23.976 fps (standard for 1080p)
    """
    os.system(f"HandBrakeCLI -i '{mkv_file}' -o '{mp4_file_path}' -e x264 -q 22.0 -r 23.976 -vf 'scale=1920:1080,format=yuv420p,y4:0' -a 1 -E av_aac -b:a 128 -B:a 192 --crop='0:0:0:0'")
    
    # Copy to destination directory if specified
    if copy_to:
        copy_destination = os.path.expanduser(copy_to)
        if not os.path.exists(copy_destination):
            os.makedirs(copy_destination)
        
        destination_file = os.path.join(copy_destination, f"{mp4_movie_name}.mp4")
        print(f"Copying {mp4_file_path} to {destination_file}")
        shutil.copy2(mp4_file_path, destination_file)
        print(f"Successfully copied to {destination_file}")


def signal_handler(sig, frame):
    print('\nReceived Ctrl+C! Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Rip DVD and convert to MP4")
        parser.add_argument("title", help="Movie title for the output file")
        parser.add_argument("--copy", dest="copy_to", help="Directory to copy the final MP4 file to")
        
        args = parser.parse_args()

        min_length = int(os.getenv("MIN_LENGTH", 900))
        title = args.title
        copy_to = args.copy_to
        
        copy_info = f" and copy to {copy_to}" if copy_to else ""
        answer = input(f"Are you sure you want to rip the DVD and convert it to MP4 with the title '{title}'{copy_info}? (yes/no): ").strip().lower()

        if answer == "y" or answer == "yes":
            main(title, min_length, copy_to)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
