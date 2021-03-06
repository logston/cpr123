#! /bin/bash

export DJANGO_SETTINGS_MODULE=cpr123.settings
export PYTHONPATH=/home/paul/djprojs/cpr123

python=/home/paul/.virtualenvs/cpr123/bin/python
manager=/home/paul/djprojs/cpr123/libs/cron/updateclass.py

if ! [ -f $python ]; then
    echo "No python executable at $python"
    exit 1	
fi

if ! [ -f $manager ]; then
    echo "No pester manager found at $manager"
    exit 1
fi

exec $python $manager

exit 0
