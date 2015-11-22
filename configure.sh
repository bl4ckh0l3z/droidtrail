#!/bin/bash

DROIDTRAIL_HOME="/home/xxx/srv_xxx/droidtrail/"
cd $DROIDTRAIL_HOME
rm -Rf droidtrail.env
virtualenv droidtrail.env
source droidtrail.env/bin/activate

pip install -r requirements.txt

echo "Installing chilkat-lib..."
cp lib/chilkat-9.5.0-python-2.7-x86_64-linux/_chilkat.so lib/chilkat-9.5.0-python-2.7-x86_64-linux/chilkat.py droidtrail.env/lib/python2.7/site-packages/
echo "Successfully installed chilkat-lib"

sudo apt-get install p7zip-full
sudo apt-get install logrotate

logrotate_conf="/etc/logrotate.d/$(pwd | rev | cut -d"/" -f1-2 | rev | tr '/' '_')"
if [ ! -e $logrotate_conf ];then
    echo "- Configuring logrotate..."
    sudo echo $DROIDTRAIL_HOME"logs/*.log {
    missingok
    rotate 2
    size 20M
    compress
}" > $logrotate_conf
else
    echo "- Logrotate is already configured..."
fi

python -c "from droidtrail.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "Done"
