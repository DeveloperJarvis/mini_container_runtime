import os
import io
import tokenize

# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = "."          # Root folder to traverse
OUTPUT_FILE = "code.txt"    # Output file
INCLUDE_EXTENSIONS = {".py"}    # file types to include

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    ".env",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
}


def remove_python_comments(source: str) -> str:
    output = []
    tokens = tokenize.generate_tokens(
        io.StringIO(source).readline
    )

    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        output.append(tok)
    
    code = tokenize.untokenize(output)

    lines = [
        line for line in code.splitlines()
        if line.strip() != ""
    ]

    return "\n".join(lines)


# --------------------------------------------------
# Core dump logic
# --------------------------------------------------

def dump_project_code(root_dir: str, output_file: str):
    with open(output_file, "w", encoding="utf-8") as out:
        for current_root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for filename in sorted(files):
                ext = os.path.splitext(filename)[1]
                if ext not in INCLUDE_EXTENSIONS:
                    continue

                if filename == "dump_project_code.py":
                    continue  # Skip this file

                file_path = os.path.join(current_root, filename)
                rel_path = os.path.relpath(file_path, root_dir)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                except (UnicodeDecodeError, OSError):
                    # Skip binary or unreadable files
                    continue
                
                cleaned_code = remove_python_comments(code)

                # Write path header
                out.write(f"# {rel_path}:\n")
                out.write(cleaned_code.rstrip())
                out.write("\n\n\n")

    print(f"✅ Project code dumped to '{output_file}'")

# --------------------------------------------------
# entry point
# --------------------------------------------------

if __name__ == "__main__":
    dump_project_code(PROJECT_ROOT, OUTPUT_FILE)
