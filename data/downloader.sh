max=916971

for i in $(seq 1 $max)
do
    printf "DOWNLOADING %7s..." "$i"
    wget "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=$i" -O tmp.deck &> /dev/null

    if [ 0 -ne $? ]
    then
        printf "    %50s    [FAILED]\n" ""
    else
        title=$(cat ./tmp.deck | head -n 1 | sed s/'\/\/NAME: '/''/g | sed s/' '/'_'/g | tr -d "\n\r\b\f" | sed s/'\/'/'\\\/'/g)

        if [ -z $title ]
        then
            title="$i"
        fi

        mv ./tmp.deck ./scraped_decks/$title.deck
        printf "    %50s    [OKAY]\n" $title
        sleep 1
    fi
done

