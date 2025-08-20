#!/bin/bash
# Setup script for Podcast Index API keys

echo "Podcast Index API Key Setup"
echo "=========================="
echo "This script will update your .env file with Podcast Index API credentials."
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it first."
    exit 1
fi

# Ask for API Key
read -p "Enter your Podcast Index API Key: " API_KEY
if [ -z "$API_KEY" ]; then
    echo "Error: API Key cannot be empty."
    exit 1
fi

# Ask for API Secret
read -p "Enter your Podcast Index API Secret: " API_SECRET
if [ -z "$API_SECRET" ]; then
    echo "Error: API Secret cannot be empty."
    exit 1
fi

# Check if the keys are already in the .env file
if grep -q "PODCAST_INDEX_API_KEY" .env; then
    # Update existing keys - properly quote the values to handle spaces
    sed -i "s/PODCAST_INDEX_API_KEY=.*/PODCAST_INDEX_API_KEY=\"$API_KEY\"/" .env
    sed -i "s/PODCAST_INDEX_API_SECRET=.*/PODCAST_INDEX_API_SECRET=\"$API_SECRET\"/" .env
else
    # Add new keys - properly quote the values to handle spaces
    echo "" >> .env
    echo "# Podcast Index API" >> .env
    echo "PODCAST_INDEX_API_KEY=\"$API_KEY\"" >> .env
    echo "PODCAST_INDEX_API_SECRET=\"$API_SECRET\"" >> .env
fi

echo "API keys have been added to your .env file."
echo "Now testing the connection..."

# Run the test script
python test_podcast_api.py

echo
echo "Setup complete! You can now use the Podcast Index API in your application."
