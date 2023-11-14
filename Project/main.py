import Trial as t

import subprocess
import sys

try:
    subprocess.run("pip install -r ./requirements.txt")
except Exception as error:
    print(error)
    print("Attempting to use a UTF-8 encoded version instead")
    subprocess.run("pip install -r ./requirementsUTF8.txt")


tmp = t.Trial("0")

tmp.start_trial()