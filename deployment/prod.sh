#!/bin/sh
echo ---------------------------------------
echo Deployment Start - Production
echo ---------------------------------------
echo Building and Deploying Odin API
echo ---------------------------------------
docker-compose -p odin-api -f docker-compose.yml up -d --build --remove-orphans
echo
echo ---------------------------------------
echo Conntainer Status:
echo ---------------------------------------
docker ps | grep 'odin-api'