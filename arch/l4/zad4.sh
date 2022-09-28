#!/bin/bash
addr="$1"
#addr="https://news.ycombinator.com/"
if [[ ! -d ./.webtrace ]]; then
    mkdir ./.webtrace
fi
if [[ ! -d ./.webtrace/.git ]]; then
    git init ./.webtrace/
    git -C ./.webtrace config user.email "wt@localhost"
    git -C ./.webtrace config user.name "Webtrace"
fi
sha256=$(echo "$addr" | sha256sum | sed 's/\s-//g')
touch ./.webtrace/$sha256
git -C ./.webtrace add -A
git -C ./.webtrace commit -m "WebTrace"
while true; do
    lynx -dump "$addr" > ./.webtrace/$sha256
    diff=$( git -C ./.webtrace --no-pager diff)
    if [[ ! -z $diff ]]; then
        git -C ./.webtrace --no-pager diff
        git -C ./.webtrace add -A
        git -C ./.webtrace commit -m "WebTrace"
        notify-send "WebTrace: Zmiana"
    fi
    #echo czekam
    sleep $2
done

