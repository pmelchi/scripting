#!/bin/bash

#Mount device
#sudo mount -t ext4 -o defaults /dev/sda1 /media/backup
#/home/rock/bin/myRsync.sh

#Check device
#sudo smartctl -d sat -x /dev/sda1
#sudo smartctl -d sat -i /dev/sda1

#rsync --password-file=/home/rock/local/mybackup.txt -avz --exclude ".recycle" mybackup@10.0.1.101::PabloStorage /media/backup/PabloStorage/

rsyncModule() {
    echo "--------rsync from: $3 ---to---- $4 -----"
    rsync --log-file="$LOG_FILE" \
        --password-file="$RSYNC_SECRET" \
        --exclude "$EXCLUDE_LIST" \
        $RSYNC_OPTIONS $1@$2::$3 $4
    if [ $? -ne 0 ]; then
        echo "Failed to rsync from: $3 to $4"
        exit 1
    fi
}

help(){
    echo "How to use this program"
}

#Main 

LOG_FILE=/var/log/rsync.log
RSYNC_OPTIONS="-avz"
RSYNC_SECRET="/root/local/mybackup.txt"
EXCLUDE_LIST=".recycle"
DEVICE="/dev/sda1"
MNT_PNT="/media/backup"

if [ -z "$RSYNC_SECRET" ]
then
      echo "\$RSYNC_SECRET is empty"
      help
      exit 1
fi

#Check for mounted disk
findmnt "$DEVICE"
if [ $? -eq 0 ]; then
    echo "Device $DEVICE is mounted"
else
    echo "Mounting device $DEVICE"
    mount -t ext4 -o defaults "$DEVICE" "$MNT_PNT"
    if [ $? -ne 0 ]; then
        echo "Cannot mount device $DEVICE into $MNT_PNT"
        exit 1
    fi
fi

echo "------------Starting new rsync process-------------"
rsyncModule mybackup 10.0.1.101 Shared /media/backup/Shared/
rsyncModule mybackup 10.0.1.101 FlorenciaStorage /media/backup/FlorenciaStorage/
rsyncModule mybackup 10.0.1.101 PabloStorage /media/backup/PabloStorage/
rsyncModule mybackup 10.0.1.101 Public /media/backup/Public/
echo "------------Finished rsync succesfully-------------"

echo "Unmounting device $DEVICE"
umount "$DEVICE"