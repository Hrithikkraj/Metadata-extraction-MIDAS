import os
from mutagen.mp3 import MP3
import datetime

def calculate_total_duration(folder_path):
    """
    Calculates the total duration of all MP3 files in a given folder and its subfolders.
    """
    total_seconds = 0.0

    # Check if the provided path is a valid directory
    if not os.path.isdir(folder_path):
        print(f"Error: The path '{folder_path}' is not a valid directory.")
        return

    print(f"Scanning for MP3 files in '{folder_path}'...")

    # os.walk recursively goes through the directory and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Check if the file is an MP3 file
            if filename.lower().endswith('.mp3'):
                file_path = os.path.join(root, filename)
                try:
                    # Load the MP3 file to get its info
                    audio = MP3(file_path)
                    # Add the duration (in seconds) to the total
                    total_seconds += audio.info.length
                except Exception as e:
                    print(f"Could not process file: {file_path} | Error: {e}")

    return total_seconds

# --- MAIN PART OF THE SCRIPT ---
if __name__ == "__main__":
    # !!! IMPORTANT: CHANGE THIS to the path of your folder containing MP3s !!!
    # You can use a relative path './my_music' or an absolute path 'C:/Users/YourUser/Music'
    directory_to_scan = r"C:\Users\lenovo\Desktop\sem 5\IP\output"  # The '.' means the current directory where the script is run

    total_duration_seconds = calculate_total_duration(directory_to_scan)

    if total_duration_seconds is not None:
        # Convert total seconds into a more readable format (HH:MM:SS)
        readable_duration = str(datetime.timedelta(seconds=round(total_duration_seconds)))
        
        # Or you can calculate hours, minutes, seconds manually
        hours = int(total_duration_seconds // 3600)
        minutes = int((total_duration_seconds % 3600) // 60)
        seconds = int(total_duration_seconds % 60)

        print("\n--- Calculation Complete ---")
        print(f"Total duration (seconds): {total_duration_seconds:.2f}")
        print(f"Total duration (HH:MM:SS): {readable_duration}")
        print(f"Which is: {hours} hours, {minutes} minutes, and {seconds} seconds. ")