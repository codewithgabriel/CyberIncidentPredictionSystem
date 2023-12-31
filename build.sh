#!/usr/bin/env bash
# exit on error
set -o errexit
python -m pip install pip --upgrade
pip uninstall tensorflow-cpu
pip uninstall pycuda
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate