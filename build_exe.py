import os
import shutil
import subprocess
import sys

# Configuration
MAIN_SCRIPT = "learn.py"  
EXE_NAME = "SnakeEater_AI"
ICON_PATH = "icon.ico" # Optional, if exists
DIST_DIR = "dist"
BUILD_DIR = "build"

def print_step(msg):
    print(f"\n{'='*50}\n{msg}\n{'='*50}")

def check_pyinstaller():
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def build():
    print_step("SnakeEater AI - EXE Builder")

    # 1. Check for PyInstaller
    if not check_pyinstaller():
        print("Error: PyInstaller is not installed or not in PATH.")
        print("Please run: pip install pyinstaller")
        return

    # 2. Check for Trained Model
    model_path = os.path.join("mlAgent", "qTable.pkl")
    if not os.path.exists(model_path):
        print(f"警告: 找不到訓練好的模型 {model_path}")
        print("請確保你已經將 Kaggle 下載的 'qTable_trained_100.pkl' 改名為 'qTable.pkl' 並放入 mlAgent 資料夾。")
        val = input("是否繼續打包? (AI 會是笨笨的) [y/N]: ")
        if val.lower() != 'y':
            return
    else:
        print(f"已偵測到模型: {model_path}")

    # 3. Clean previous builds
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    # 4. Construct PyInstaller Command
    # We need to bundle mlAgent folder so config and qTable are accessible
    # --add-data "source;dest"
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed", # No console window
        "--name", EXE_NAME,
        "--add-data", f"mlAgent{os.pathsep}mlAgent", # Bundle entire mlAgent folder
        "--add-data", f"assets{os.pathsep}assets", # Bundle assets
        "learn.py" # Entry point
    ]

    print_step(f"Running Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print_step("Build Success!")
        print(f"Executable is located at: {os.path.abspath(os.path.join(DIST_DIR, EXE_NAME + '.exe'))}")
    except subprocess.CalledProcessError as e:
        print_step("Build Failed")
        print(e)

if __name__ == "__main__":
    build()
