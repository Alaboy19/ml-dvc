sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .ml-dvc
source .ml-dvc/bin/activate
pip install -r requirements.txt
