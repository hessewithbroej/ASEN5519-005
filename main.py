import subprocess
import os
import pathlib

print(pathlib.Path(__file__).parent.resolve())

fpath  = pathlib.Path(__file__).parent.resolve()
print("pip install -r" + fpath.__str__() + "/requirements.txt")

subprocess.run("pip install -r" + fpath.__str__() + "/requirements.txt")

import Trial as t

tmp = t.Trial("0")

tmp.start_trial()