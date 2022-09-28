#!/bin/bash
goodimg=0
while [ $goodimg == 0 ]; do
    printf -v day "%02d" $(( $(($RANDOM % 28)) + 1))
    printf -v month "%02d" $(( $(($RANDOM % 12)) + 1))
    year=$(( $(($RANDOM % 5)) + 2015))
    url=$(curl -s "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=$year-$month-$day" | jq '.url' | sed 's/^\"//; s/\"$//')
    if [[ "$url" == https://apod.nasa.gov/apod/image* ]]; then
        goodimg=1
    else
        echo retry
        sleep 5
    fi
done
joke=$(curl -s "http://api.icndb.com/jokes/random?escape=javascript" | jq ".value.joke" | sed 's/^\"//; s/\"$//; s/\\//g')
curl  -s "$url" -o ./tmpspacecacaimage
img2txt ./tmpspacecacaimage
echo "$joke"
rm ./tmpspacecacaimage
