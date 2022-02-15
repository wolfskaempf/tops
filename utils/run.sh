#!/bin/sh

flask db upgrade
gunicorn tops:app --bind=0.0.0.0:80