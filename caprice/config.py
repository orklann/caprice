import os
import pathlib

name = "Caprice"

# data folder path
cwd = pathlib.Path(__file__).resolve().parent
data_dir = os.path.join(cwd, "data")
