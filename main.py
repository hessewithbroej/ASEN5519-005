import subprocess
import os
import pathlib

fpath  = pathlib.Path(__file__).parent.resolve()

subprocess.run("pip install -r " + fpath.__str__() + "/lib/requirements.txt")


import Trial as t

tmp = t.Trial("0")

tmp.start_trial()