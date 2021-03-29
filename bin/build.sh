#!/usr/bin/env sh

pip install -r /app/requirements.txt -q 2>&1
tail -f /dev/null