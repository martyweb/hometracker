[![Python package](https://github.com/martyweb/hometracker/actions/workflows/workflow.yml/badge.svg)](https://github.com/martyweb/hometracker/actions/workflows/workflow.yml)

# Overview
Get data from various API's, pumps data into influxdb

## Air Quality
Pulls data from purpleair

## Weather
Pulls data from openweathermap.org

## Speedtest
Uses speedtest-cli to get internet speeds

## Pollution
Pulls data from openweathermap.org

# Docker Notes
docker exec -it hometracker_web_1 bash

docker-compose up --force-recreate --build
