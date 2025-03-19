#!/bin/bash
until curl -s http://localhost:4444/wd/hub/status | jq -e '.value.ready' > /dev/null; do
    echo "Waiting for Selenium server..."
    sleep 2
done
echo "Selenium server is ready!"
