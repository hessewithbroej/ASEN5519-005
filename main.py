import subprocess
import os



subprocess.run("pip install -r ./requirements.txt")

import Trial as t

tmp = t.Trial("0")

tmp.start_trial()