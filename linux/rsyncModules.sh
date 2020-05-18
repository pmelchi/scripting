#!/bin/bash

#Mount device
#sudo mount -t ext4 -o defaults /dev/sda1 /media/backup
#/home/rock/bin/myRsync.sh

#Check device
#sudo smartctl -d sat -x /dev/sda1
#sudo smartctl -d sat -i /dev/sda1

#rsync --password-file=/home/rock/local/mybackup.txt -avz --exclude ".recycle" mybackup@10.0.1.101::Shared /media/backup/Shared/

rsyncModule() {
    echo "--------Copy from: $3 ---to---- $4 -----" >> $LOG_FILE
    rsync --log-file=$LOG_FILE \
        --password-file=$RSYNC_SECRET \
        --exlude $EXCLUDE_LIST
        $RSYNC_OPTIONS $1@$2::$3 $4
    if [ $? -ne 0 ]; then
        echo "Failed to copy from: $3 to $4"
        exit 1
    fi
}

help(){
    echo "How to use this program"
}

#Main 

LOG_FILE=/var/log/rsync.log
RSYNC_OPTIONS="-avz"
RSYNC_SECRET="/home/rock/local/mybackup.txt"
EXCLUDE_LIST=".recycle"

if [ -z "$RSYNC_SECRET" ]
then
      echo "\$RSYNC_SECRET is empty"
      help
      exit 1
fi

echo "------------Starting new copy-------------" >> $LOG_FILE
rsyncModule mybackup 10.0.1.101 Shared /media/backup/Shared/
rsyncModule mybackup 10.0.1.101 FlorenciaStorage /media/backup/FlorenciaStorage/
rsyncModule mybackup 10.0.1.101 PabloStorage /media/backup/PabloStorage/
rsyncModule mybackup 10.0.1.101 Public /media/backup/Public/
echo "------------Finished succesfully-------------" >> $LOG_FILE