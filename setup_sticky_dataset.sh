#!/bin/bash

set -e

echo "=== Creating Python virtual environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Upgrading pip ==="
pip install --upgrade pip

echo "=== Installing Kaggle and YOLO (ultralytics) libraries ==="
pip install kaggle ultralytics

echo "=== Setting up kaggle.json ==="
KAGGLE_CONFIG_DIR="$HOME/.kaggle"
mkdir -p $KAGGLE_CONFIG_DIR

if [ ! -f "$KAGGLE_CONFIG_DIR/kaggle.json" ]; then
    echo "Please copy your kaggle.json file to this directory and press ENTER."
    read -p "Press ENTER after you have copied kaggle.json here..." DUMMY
    cp ./kaggle.json $KAGGLE_CONFIG_DIR/
fi

chmod 600 $KAGGLE_CONFIG_DIR/kaggle.json

echo "=== Downloading Yellow Sticky Traps dataset from Kaggle ==="
kaggle datasets download -d friso1987/yellow-sticky-traps -p sticky_dataset --unzip

echo "=== All done! ==="
echo "Dataset downloaded to ./sticky_dataset"
echo "YOLO and Kaggle Python packages installed in your venv."
echo "To activate the virtualenv again later, run: source venv/bin/activate"
