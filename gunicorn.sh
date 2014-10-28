#!/bin/sh

gunicorn -c gunicorn.conf.py wsgi:application
