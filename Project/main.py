import Trial as t

import subprocess
import sys

subprocess.run("pip install -r ./requirements.txt")


tmp = t.Trial("0")

tmp.start_trial()