import os
import subprocess


def cli_streamlit_windaq(argv: list | dict | None = None, /):
    path_to_file = os.path.dirname(__file__)
    subprocess.call(["streamlit", "run", f"{path_to_file}/windaq_streamlit.py"])
