#!/bin/sh
coverage run --source=grammpy-transforms -m unittest discover -s tests -p "*Test.py"; coverage report -m
