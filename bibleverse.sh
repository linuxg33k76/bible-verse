#!/bin/bash

# Define the virtual environment directory name
VENV_DIR="venv"
CURRENT_DIR=$(pwd)
SOURCE_PATH="$CURRENT_DIR/$VENV_DIR/bin/activate"

# Define the command to run the Python application
CMD="bibleverse.py"

# 1. Check if the virtual environment exists, create it if not
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# 2. Activate the virtual environment
source $SOURCE_PATH
pip list -q

# 3. Install or update dependencies
pip install -r requirements.txt -q

# 4. Run the Python application
"$CURRENT_DIR/$VENV_DIR/bin/python" $CMD $1