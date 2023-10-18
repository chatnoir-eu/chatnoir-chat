#!/usr/bin/bash

PREV_DIR=${PWD}
cd "$(dirname "$0")"
export PYTHONPATH=':../:.'
export DJANGO_SETTINGS_MODULE=settings_test

python3 ../manage.py reset_db --no-input
python3 ../manage.py makemigrations chatnoir_chat

python3 ../manage.py migrate chatnoir_chat

coverage run --data-file=test-coverage/.coverage ../manage.py test --failfast
coverage report --data-file=test-coverage/.coverage > test-coverage/coverage-report
cd test-coverage

rm -Rf coverage.svg
coverage-badge -o coverage.svg

cd ${PREV_DIR}
