for i in $(seq 900000 911621)
do
    #wget "http://mckenzielabs.org/scrape.php" -O ./value &> /dev/null
    #i=$(cat ./value | sed s/' '/''/g)

    if [ 'DONE' == $i ]
    then
        exit
    else
        printf "DOWNLOADING %7s...\n" "$i"

        echo "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=$i"
        wget "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=$i" -O $i.deck &> /dev/null

        if [ 0 -ne $? ]
        then
            printf "    %50s    [FAILED]\n" ""
        else
            #scp -i /u/reid/.ssh/magic_key ./$i.deck reid@mckenzielabs.org:~/Projects/M\:TG/data/scraped_decks/
            echo "DECK OKAY"
            #rm ./$i.deck
        fi
	sleep 3
    fi
done

