LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENV_DIR="local_lib"
MY_PROGRAM="roads_to_philosophy.py"

# setup venv
$PYTHON_PATH -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# pip version
python3 -m pip --version

# pip install
# python3 -m pip install --log $LOG_FILE --force-reinstall -r requirement.txt
python3 -m pip install --log $LOG_FILE -r requirement.txt

# execute my program
# python3 $MY_PROGRAM "philosophy"
python3 $MY_PROGRAM "existence"
# python3 $MY_PROGRAM "idea"
# python3 $MY_PROGRAM "ontology"
