#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Development
echo ---------------------------------------
echo Building and Deploying Odin API
echo ---------------------------------------
docker-compose -p odin-api-dev -f docker-compose.dev.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'odin-api'