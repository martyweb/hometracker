[![Python package](https://github.com/martyweb/hometracker/actions/workflows/workflow.yml/badge.svg)](https://github.com/martyweb/hometracker/actions/workflows/workflow.yml)

# Overview
Flask application that will collect data from various API's and store data in influxdb for reporting

Note: this project still needs a lot of work
<BR>
<img src="/static/images/home_screen.png" width=200 alt="Home Screen"><BR>
<img src="/static/images/grafana_sample.png" width=200 alt="Grafana Sample">

## Prerequisites
- InfluxDB
- Grafana (Optional) 

## Configuration
A lot of the config is hard coded (for now) into these files:
- config-app.json
- config-plugins.json

# Plugins
Semi-flexible plugin system allows you to bring your own plugin

Located in plugins directory

## Air Quality
Pulls data from purpleair

## Weather
Pulls data from openweathermap.org

## Speedtest
Uses speedtest-cli to get internet speeds

## Pollution
Pulls data from openweathermap.org

# Running container
Containers are built and published, you can run them like this:

docker-compose up --force-recreate --build

or

docker run \
  --name hometracker \
  -p 80:5000 \
  -d ghcr.io/martyweb/hometracker:master