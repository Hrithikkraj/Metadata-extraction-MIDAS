import os
from collections import defaultdict

# --- CONFIGURATION ---
# IMPORTANT: Make sure this path is correct!
OUTPUT_DIR = r"D:\output"
# --- END CONFIGURATION ---


def analyze_and_clean_directory(directory, dry_run=True):
    """
    Finds pairs of (.mp3, _metadata.json) files and deletes EVERYTHING else.
    """
    if not os.path.isdir(directory):
        print(f"❌ Error: Directory not found at '{directory}'")
        return

    print(f"🔎 Analyzing directory for perfect pairs: {directory}\n")
    
    all_files = [os.path.join(directory, f) for f in os.listdir(directory)]
    
    # Group files by their base name to find potential pairs
    grouped_files = defaultdict(list)
    for file_path in all_files:
        filename = os.path.basename(file_path)
        # Create a base name by removing known extensions/suffixes
        base_name = os.path.splitext(filename.replace('_metadata.json', ''))[0]
        grouped_files[base_name].append(file_path)

    files_to_keep = set()

    # Identify the specific files that should be kept
    for base_name, files_in_group in grouped_files.items():
        # Check if the essential files exist in this group
        has_metadata = any(f.endswith('_metadata.json') for f in files_in_group)
        has_audio = any(f.endswith('.mp3') for f in files_in_group)

        if has_audio and has_metadata:
            print(f"✅ VALID PAIR: Found for '{base_name}'.")
            # If the pair is valid, find the specific files to save
            for f in files_in_group:
                if f.endswith('.mp3') or f.endswith('_metadata.json'):
                    files_to_keep.add(f)
                    print(f"    └── Marked to KEEP: {os.path.basename(f)}")
    
    # Any file not explicitly marked to be kept will be deleted
    files_to_delete = [f for f in all_files if f not in files_to_keep]

    print("\n" + "="*40)
    print("ANALYSIS COMPLETE")
    print(f"Total files to keep: {len(files_to_keep)}")
    print(f"Total files to delete: {len(files_to_delete)}")
    print("="*40 + "\n")

    if not files_to_delete:
        print("🎉 Nothing to clean up. The folder is already perfect!")
        return

    # Deletion logic
    if dry_run:
        print("DRY RUN MODE: The following files would be deleted:")
        for f in sorted(files_to_delete):
            print(f"  - {os.path.basename(f)}")
        print("\nTo actually delete files, run the script with dry_run=False.")
    else:
        # Ask for final confirmation
        confirm = input(f"Proceed with deleting {len(files_to_delete)} files? (yes/no): ").lower()
        if confirm == 'yes':
            print("\n🗑️ Deleting files...")
            deleted_count = 0
            for f in files_to_delete:
                try:
                    os.remove(f)
                    print(f"  - Deleted: {os.path.basename(f)}")
                    deleted_count += 1
                except OSError as e:
                    print(f"  - ❌ Error deleting {os.path.basename(f)}: {e}")
            print(f"\n✨ Cleanup complete. Deleted {deleted_count} files.")
        else:
            print("\n🚫 Deletion cancelled by user.")


# === Main Execution ===
if __name__ == "__main__":
    # By default, this runs in "Dry Run" mode. It will only show you
    # what it would delete without actually doing anything.
    #
    # ‼️ ONCE YOU ARE SURE IT'S CORRECT, CHANGE `dry_run=True` to `dry_run=False` ‼️
    analyze_and_clean_directory(OUTPUT_DIR, dry_run=True)