#!/bin/bash
# Credit: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572

ENV_FILE=.env

# Loads the environment variables set in the file $ENV_FILE as environment variables.
set -a; source $ENV_FILE; set +a
