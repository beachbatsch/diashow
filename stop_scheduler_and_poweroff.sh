#!/usr/bin/bash

# sudo visudo
# username        ALL=(ALL)       NOPASSWD: /usr/sbin/poweroff


/usr/bin/python $(dirname "$0")/stop_scheduler.py

sleep 20

sudo /usr/sbin/poweroff