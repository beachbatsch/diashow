#!/usr/bin/bash

cd $(dirname "$0")/.locks/
rm -rf {*,.[^.]*}
cd ..

/usr/bin/python $(dirname "$0")/scheduler.py

