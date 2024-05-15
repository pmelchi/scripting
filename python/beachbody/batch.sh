#! /bin/bash

cd /srv/dev-disk-by-label-HDDStorage/OMV-Downloader/downloader
source venv/bin/activate


#Regular programs
# python download-bodi.py ./5er/5er.json ./5er/ > /var/log/beachbody.log
# python download-bodi.py ./the-20s/the-20s.json ./the-20s/ >> /var/log/beachbody.log
# python download-bodi.py ./chopwood-carrywater/chopwood-carrywater.json ./chopwood-carrywater/ >> /var/log/beachbody.log

#Super-block
python download-superblock.py ./superblock-liifmore.json ./superblock-liifmore > /var/log/beachbody.log


# Archive 
#python download-bodi.py ./dig-deeper/dig-deeper.json ./dig-deeper/ >> /var/log/beachbody.log