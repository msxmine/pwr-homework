#!/bin/bash
clear
GRAPHNETIF="enp1s0"
GRAPHHEIGHT=7
GRAPHMAXWIDTH=1000

function bytes_human {
    if [ $1 -gt 1000000 ]; then
        echo "$(( $1 / 1000000)).$(($(( $1 / 100000)) - $((10 * $(( $1 / 1000000)) )) )) MB"
    elif [ $1 -gt 1000 ]; then
        echo "$(( $1 / 1000)).$(($(( $1 / 100)) - $((10 * $(( $1 / 1000)) )) )) kB"
    else
        echo "$1 B"
    fi
}


loopindx=1
recvindx=-1
sendindx=-1
for line in `cat /proc/net/dev | sed -n "2p" | sed  "s/^\s\+//g;  s/\s\+/|/g; s/|\+/\n/g"`; do
    if [ "$line" == "bytes" ]; then
        if [ $recvindx == -1 ]; then
            recvindx=$loopindx;
        else
            sendindx=$loopindx;
        fi
    fi
    loopindx=$(($loopindx + 1))
done

loopindx=3
netifline=4
for interface in `cat /proc/net/dev | sed -n "3~1p" | sed "s/://g; s/^\s\+//g; s/\s.*//"`; do
    if [ "$interface" == "$GRAPHNETIF" ]; then
        netifline=$loopindx;
    fi
    loopindx=$(($loopindx + 1))
done

declare -a prevrecv
declare -a prevsend
lastindex=0


maxdownband=0
nextmaxdownband=100000000
maxupband=0
nextmaxupband=100000000
samples=0

while true; do
tput civis
tput cup 0 0
echo $(cat /proc/net/dev | sed -n "$netifline p" | sed "s/\s\+/|/g" | cut -d "|" -f 1)
cols=$(tput cols)


lastindex=$(($lastindex + 1))
if [ $lastindex == $GRAPHMAXWIDTH ]; then
    lastindex=0;
fi
recvbytes=$(cat /proc/net/dev | sed -n "$netifline p" | sed "s/\s\+/|/g" | cut -d "|" -f $recvindx)
sendbytes=$(cat /proc/net/dev | sed -n "$netifline p" | sed "s/\s\+/|/g" | cut -d "|" -f $sendindx)
prevrecv[$lastindex]=$recvbytes
prevsend[$lastindex]=$sendbytes
if [ $samples -lt $GRAPHMAXWIDTH ]; then
    samples=$(($samples + 1));
fi

period=$cols
if [ $period -gt $samples ]; then
    period=$samples
fi

maxdownband=$nextmaxdownband
nextmaxdownband=$(($GRAPHHEIGHT * 8 ))
maxupband=$nextmaxupband
nextmaxupband=$(($GRAPHHEIGHT * 8 ))

maxdownhuman=$(bytes_human $maxdownband)
echo "$maxdownhuman/s                                                                    "

deltadownsum=0

for (( row=$GRAPHHEIGHT; row > 0; row--)); do
    for (( col=$cols; col > 0; col--)); do
        dataaddr=$(( $lastindex - $col ))
        if [[ $dataaddr -lt 0 ]]; then
            dataaddr=$(($dataaddr + $GRAPHMAXWIDTH));
        fi
        dataaddr2=$(( $(( $lastindex - $col)) + 1 ))
        if [[ $dataaddr2 -lt 0 ]]; then
            dataaddr2=$(($dataaddr2 + $GRAPHMAXWIDTH));
        fi

        if [ -z ${prevrecv[$dataaddr]+abc} ]; then
            delta=0;
        else
            delta=$(( ${prevrecv[$dataaddr2]} - ${prevrecv[$dataaddr]} ));
        fi
        if [ $row == $GRAPHHEIGHT ]; then
            deltadownsum=$(($deltadownsum + $delta));
        fi
        if [ $delta -gt $nextmaxdownband ]; then
            nextmaxdownband=$delta;
        fi
        lower=$((  $(($maxdownband / $GRAPHHEIGHT)) * $(($row - 1)) ))
        blockval=$(( $delta - $lower ))
        blockdis=$(( $blockval /  $(($maxdownband / $(( $GRAPHHEIGHT * 8 )) ))  ))
        #echo lower $lower val $blockval dis $blockdis
        block="█"
        if [ $blockdis == 7 ]; then block="▇"; fi
        if [ $blockdis == 6 ]; then block="▆"; fi
        if [ $blockdis == 5 ]; then block="▅"; fi
        if [ $blockdis == 4 ]; then block="▄"; fi
        if [ $blockdis == 3 ]; then block="▃"; fi
        if [ $blockdis == 2 ]; then block="▂"; fi
        if [ $blockdis == 1 ]; then block="▁"; fi
        if [ $blockdis -le 0 ]; then block=" "; fi
        echo -n "$block"
        
    done
    echo
done

downhumanavg=$(bytes_human $(($deltadownsum / $period)) )
echo DOWN AVG: $downhumanavg/s "                                "
downhumancur=$(bytes_human $delta)
echo DOWN CUR: $downhumancur/s "                                   "

maxuphuman=$(bytes_human $maxupband)
echo "$maxuphuman/s                                                      "

deltaupsum=0

for (( row=$GRAPHHEIGHT; row > 0; row--)); do
    for (( col=$cols; col > 0; col--)); do
        dataaddr=$(( $lastindex - $col ))
        if [[ $dataaddr -lt 0 ]]; then
            dataaddr=$(($dataaddr + $GRAPHMAXWIDTH));
        fi
        dataaddr2=$(( $(( $lastindex - $col)) + 1 ))
        if [[ $dataaddr2 -lt 0 ]]; then
            dataaddr2=$(($dataaddr2 + $GRAPHMAXWIDTH));
        fi

        if [ -z ${prevsend[$dataaddr]+abc} ]; then
            delta=0;
        else
            delta=$(( ${prevsend[$dataaddr2]} - ${prevsend[$dataaddr]} ));
        fi
        if [ $row == $GRAPHHEIGHT ]; then
            deltaupsum=$(($deltaupsum + $delta));
        fi
        if [ $delta -gt $nextmaxupband ]; then
            nextmaxupband=$delta;
        fi
        lower=$((  $(($maxupband / $GRAPHHEIGHT)) * $(($row - 1)) ))
        blockval=$(( $delta - $lower ))
        blockdis=$(( $blockval /  $(($maxupband / $(( $GRAPHHEIGHT * 8 )) ))  ))
        #echo lower $lower val $blockval dis $blockdis
        block="█"
        if [ $blockdis == 7 ]; then block="▇"; fi
        if [ $blockdis == 6 ]; then block="▆"; fi
        if [ $blockdis == 5 ]; then block="▅"; fi
        if [ $blockdis == 4 ]; then block="▄"; fi
        if [ $blockdis == 3 ]; then block="▃"; fi
        if [ $blockdis == 2 ]; then block="▂"; fi
        if [ $blockdis == 1 ]; then block="▁"; fi
        if [ $blockdis -le 0 ]; then block=" "; fi
        echo -n "$block"
        
    done
    echo
done

uphumanavg=$(bytes_human $(($deltaupsum / $period)) )
echo UP AVG: $uphumanavg/s "                                   "
uphumancur=$(bytes_human $delta)
echo UP CUR: $uphumancur/s "                                   "

upsecondstotal=$(cat /proc/uptime | cut -d " " -f 1 | sed "s/\..*//g")
updays=$(( $upsecondstotal / $(( 60 * 60 * 24 )) ))
uphours=$(( $(( $upsecondstotal / $(( 60 * 60 )) )) % 24 ))
upminutes=$(( $(($upsecondstotal / 60  )) % 60  ))
upseconds=$(( $upsecondstotal  % 60 ))
echo UPTIME $updays DAYS $uphours HOURS $upminutes MINUTES $upseconds SECONDS
echo loadavg: $(cat /proc/loadavg)
tput cnorm
sleep 1
done


recvhuman=$(bytes_human $recvbytes)
sendhuman=$(bytes_human $sendbytes)

#echo $recvhuman $sendhuman

