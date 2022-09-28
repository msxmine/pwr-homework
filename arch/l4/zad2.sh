#!/bin/bash
shopt -s extglob
for file in /proc/+([0-9]) ; do
name=$(cat $file/status | sed -n "s/^Name:\s\+\(.*\)/\1/p")
pid=$(cat $file/status | sed -n "s/^Pid:\s\+\(.*\)/\1/p")
ppid=$(cat $file/status | sed -n "s/^PPid:\s\+\(.*\)/\1/p")
ram=$(cat $file/status | sed -n "s/^VmSize:\s\+\(.*\)/\1/p")
test=$(ls $file/fd/ 2>/dev/null)
if [ $? == 0 ]; then
    descriptors=$(ls $file/fd/ | wc -l);
fi
printf "PID $pid"
tput cub 999999
tput cuf 15
printf "Name $name"
tput cub 999999
tput cuf 50
printf "PPID $ppid"
tput cub 999999
tput cuf 70
printf "RAM $ram"
tput cub 999999
tput cuf 90
printf "File descriptors  $descriptors\n"
done
