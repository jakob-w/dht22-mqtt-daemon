#!/bin/bash
git stash
git pull
chmod u+x mqtt-dht.py
cp config.ini.bak config.ini
