#!/usr/bin/env sh

pip install -r /app/requirements.txt -q 2>&1
python /app/initdb.py
/usr/bin/supervisord
tail -f /dev/null