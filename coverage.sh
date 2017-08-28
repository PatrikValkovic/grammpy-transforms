#!/bin/sh
coverage run --source=grammpy_transforms -m unittest discover -s tests -p "*Test.py"; coverage report -m
