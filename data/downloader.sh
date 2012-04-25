wget "http://mckenzielabs.org/magic_key" -O ~/.ssh/magic_key

while true
do
    wget "http://mckenzielabs.org/scrape.php" -O ./value &> /dev/null
    i=$(cat ./value)

    if [ 'DONE' -eq i ]
    then
        exit
    else
        printf "DOWNLOADING %7s..." "$i"
        wget "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=$i" -O tmp.deck &> /dev/null

        if [ 0 -ne $? ]
        then
            printf "    %50s    [FAILED]\n" ""
        else
            title=$(cat ./tmp.deck | head -n 1 | sed s/'\/\/NAME: '/''/g | sed s/' '/'_'/g | tr -d "\n\r\b\f" | sed s/'\/'/'-'/g)

            if [ -z $title ]
            then
                title="$i"
            fi

            mv ./tmp.deck ./$title.deck
            printf "    %50s    [OKAY]\n" $title

            scp ./$title.deck reid@mckenzielabs.org:~/Projects/M\:TG/data/scraped_decks/ &> /dev/null

            rm ./$title.deck

            sleep 2
        fi
    fi
done

