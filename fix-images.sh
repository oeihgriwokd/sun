#!/bin/sh
# Downloads all product photos, then rebuilds the site (run once, needs internet)
cd "$(dirname "$0")" && python3 download_images.py && python3 build.py
