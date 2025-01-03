import subprocess
import os
import sys
import signal

class TransformToMp4Error(Exception):
    def __init__(self):
        super().__init__("Error when using Handbrake to convert the file to mp4")


def usage():
    print("Usage: python3 letrip.py <drive_path> <output_dir>")


def prepare_output_dir(output_dir: str) -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # return the full path of the output directory
    return output_dir


def main(mp4_movie_name: str, min_length: int):
    """
    The command will create a folder named 'PolarExpress' in the Movies directory if it doesn't exist and rip the DVD to that folder in a mp4 i.e PolarExpress.mp4
    """
    # Clean up /tmp/makemkv
    exit_code = os.system("rm -rf /tmp/makemkv")

    if exit_code != 0:
        raise Exception("Failed to clean up /tmp/makemkv")

    # Rip DVD using makemkvcon first
    mkv_path = prepare_output_dir("/tmp/makemkv")

    exit_code = os.system(f"makemkvcon mkv disc:0 all {mkv_path} --minlength={min_length} --progress=-same --robot --debug")
    if exit_code != 0:
        raise Exception("Failed to rip DVD using MakeMKV")

    files_created = os.listdir(mkv_path)

    print(f"Files created by MakeMKV: {files_created}")

    # Convert the largest mkv file to mp4 using Handbrake
    largest_file = max(files_created, key=lambda x: os.path.getsize(os.path.join(mkv_path, x)))
    mkv_file = os.path.join(mkv_path, largest_file)

    print(f"Converting {mkv_file} to mp4")

    output_dir = prepare_output_dir(f"/Volumes/Media/Movies/{mp4_movie_name}")
    mp4_file_path = os.path.join(output_dir, f"{mp4_movie_name}.mp4")

    os.system(f"HandBrakeCLI -i '{mkv_file}' -o '{mp4_file_path}'")


def signal_handler(sig, frame):
    print('\nReceived Ctrl+C! Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            usage()
            sys.exit(1)
        min_length = int(os.getenv("MIN_LENGTH", 900))
        main(sys.argv[1], min_length)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
