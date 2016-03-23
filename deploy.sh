#!/bin/sh
rsync -r --progress --partial --delete --exclude "venv" ./* root@104.236.77.115:/root/space-tabs

