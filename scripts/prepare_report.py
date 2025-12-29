import os
import shutil

SOURCE_DIR = os.getcwd()
TARGET_DIR = os.path.join(SOURCE_DIR, 'report_materials')

# List of files identified by finding .py
FILES = [
    "headless_learn.py",
    "learn.py",
    "main.py",
    os.path.join("scripts", "build_exe.py"),
    os.path.join("scripts", "generate_assets.py"),
    os.path.join("src", "food.py"),
    os.path.join("src", "game.py"),
    os.path.join("src", "mlAgent", "config.py"),
    os.path.join("src", "mlAgent", "qAgent.py"),
    os.path.join("src", "mlAgent", "utils.py"),
    os.path.join("src", "settings.py"),
    os.path.join("src", "snake.py"),
    os.path.join("src", "spatial.py"),
    os.path.join("src", "ui.py")
]

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")

    for file_path in FILES:
        full_source_path = os.path.join(SOURCE_DIR, file_path)
        
        if not os.path.exists(full_source_path):
            print(f"Skipping missing file: {file_path}")
            continue

        # Create a flat filename: src/game.py -> src_game.txt
        # Replace path separators with underscores
        flat_name = file_path.replace(os.sep, "_").replace("/", "_").replace(".py", ".txt")
        target_path = os.path.join(TARGET_DIR, flat_name)

        try:
            shutil.copy2(full_source_path, target_path)
            print(f"Copied {file_path} -> {flat_name}")
        except Exception as e:
            print(f"Error copying {file_path}: {e}")

if __name__ == "__main__":
    main()
