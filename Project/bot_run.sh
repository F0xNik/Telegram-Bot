#!../../bin/bash
set echo off
virtualenv venv -p python3
. venv/bin/activate
python3 main.py
sleep 