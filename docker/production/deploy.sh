#!/usr/bin/env bash

if [ -f ".disable-deploy" ]; then
	echo "Automatic deploy disabled"
	exit 0
fi

./beforedeploy.sh &&
docker-compose stop &&
docker-compose pull &&
docker-compose up -d
