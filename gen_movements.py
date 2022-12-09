import os
import shutil
import subprocess
import sys

for subdir, dirs, files in os.walk(os.path.join('eye-tracking', 'results')):
    for file in files:
        if file == 'gaze_converted.json':
            shutil.copyfile(os.path.join(subdir,file), os.path.join('GazeToolkit', 'build', 'Release',file))
            os.chdir(os.path.join('GazeToolkit','build','Release'))
            subprocess.call([os.path.join('tobii_cmd.bat')])
            os.chdir(os.path.join(sys.path[0]))
            shutil.copyfile(os.path.join('GazeToolkit','build','Release','movements.json'), os.path.join(subdir,'movements.json'))
            