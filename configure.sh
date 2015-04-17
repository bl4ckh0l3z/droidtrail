#!/bin/bash

DROIDTRAIL_HOME="./"
rm -Rf $DROIDTRAIL_HOME"droidtrail.env"
virtualenv $DROIDTRAIL_HOME"droidtrail.env"
source $DROIDTRAIL_HOME"droidtrail.env/bin/activate"

pip install -r requirements.txt
python -c "from droidtrail.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "done"
