#!/bin/bash

echo "----- Media Restoration Script Started -----"

# 1. Make sure media folder exists
mkdir -p media

# 2. Remove old media files
if [ "$(ls -A media 2>/dev/null)" ]; then
    echo "Cleaning old media files..."
    rm -rf media/*
else
    echo "Media folder is empty. Nothing to remove."
fi

# 3. Restore default media
if [ -d "media_defaults" ]; then
    echo "Restoring default media files..."
    cp -r media_defaults/* media/
else
    echo "Error: media_defaults folder not found!"
    exit 1
fi

echo "----- Media Restoration Completed -----"
