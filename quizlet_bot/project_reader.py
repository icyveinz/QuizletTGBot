import os

ignored_dirs = {".venv", ".idea", ".ruff_cache", "__pycache__"}


def is_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            f.read()  # Try to read the file
        return True
    except (UnicodeDecodeError, PermissionError):
        return False  # Skip if not a text file or permission is denied


def merge_files(directory, output_file="merged_code.txt"):
    with open(output_file, "w", encoding="utf-8") as out_f:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for file in files:
                file_path = os.path.join(root, file)

                if is_text_file(file_path):
                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            out_f.write(f"\n\n### {file_path} ###\n")  # Add file header
                            out_f.write(f.read())  # Copy content
                            out_f.write("\n\n" + "=" * 80 + "\n")  # Separator
                    except Exception as e:
                        print(f"Skipped file {file_path} due to error: {e}")

    print(f"✅ Merged files saved to: {output_file}")


# Get the current working directory
directory_to_scan = os.getcwd()

# Run the merge_files function
merge_files(directory_to_scan)
