#!/bin/bash

DROIDTRAIL_HOME="./"
rm -Rf $DROIDTRAIL_HOME"droidtrail.env"
virtualenv $DROIDTRAIL_HOME"droidtrail.env"
source $DROIDTRAIL_HOME"droidtrail.env/bin/activate"

pip install -r requirements.txt

echo "Installing chilkat-lib..."
cp lib/chilkat-9.5.0-python-2.7-x86_64-linux/_chilkat.so lib/chilkat-9.5.0-python-2.7-x86_64-linux/chilkat.py droidtrail.env/lib/python2.7/site-packages/
echo "Successfully installed chilkat-lib"

python -c "from droidtrail.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "done"
