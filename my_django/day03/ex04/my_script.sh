#!/bin/bash

LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENV_DIR="django_venv"

# setup venv
$PYTHON_PATH -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# pip version
python3 -m pip --version

# pip install
python3 -m pip install --log $LOG_FILE --force-reinstall -r requirement.txt
