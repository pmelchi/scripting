#! /bin/bash

cd /srv/dev-disk-by-label-HDDStorage/OMV-Downloader/downloader
source venv/bin/activate
python download-bodi.py ./liifmore/liif-more.json ./liifmore/ >> /var/log/beachbody.log