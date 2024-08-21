# legalaibot/src/run_app.py
import os
import subprocess

if __name__ == "__main__":
    os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ.get("PYTHONPATH", "")
    subprocess.run(["streamlit", "run", "src/app/main.py"])