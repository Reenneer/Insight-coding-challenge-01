#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
#python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
#!/bin/bash

# source "/Users/qinli/tensorflows/bin/activate"   # This is needed in my local as I used Virtualenv
GRADER_ROOT=$(dirname ${BASH_SOURCE})
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 ./src/WebUsersSufTime.py
