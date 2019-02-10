#!/bin/bash
for arg in "$@"
do
    python commands.py --command "$arg"
done
