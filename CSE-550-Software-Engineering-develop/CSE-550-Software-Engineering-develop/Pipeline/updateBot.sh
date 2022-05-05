while :
do
        if git pull 2>&1 | grep "Already up to date."; then
                :
        else
                echo Update detected, restarting bot
                sudo service butlerBot restart
        fi
        sleep 10
done
