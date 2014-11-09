#!/bin/sh


"$(which gunicorn)" -c gunicorn.conf.py wsgi:application
