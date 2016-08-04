#!/usr/bin/bash
PATH_WPS=/your_wps_path
PATH_WAS=/your_was_path
echo WAS
grep -f restart_tokens.txt $PATH_WAS/SystemOut.log | tail -2
echo WPS
grep -f restart_tokens.txt $PATH_WPS/SystemOut.log | tail -2
