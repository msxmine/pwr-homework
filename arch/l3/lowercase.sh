#!/bin/bash

find . -mindepth 1 -maxdepth 1 -type f -exec sh -c 'mv -n -- "$1" "$(sed "s/./\l&/g" <<< "$1")"' zamiana "{}" \;

