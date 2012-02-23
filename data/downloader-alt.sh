while true
do
    wget "http://mckenzielabs.org/scrape.php" -O ./value &> /dev/null
    i=$(cat ./value | sed s/' '/''/g)

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
            scp -i /u/reid/.ssh/magic_key ./$i.deck reid@basement.mckenzielabs.org:~/

            rm ./$i.deck

            sleep 1
        fi
    fi
done

