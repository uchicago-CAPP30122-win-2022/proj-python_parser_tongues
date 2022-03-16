PLATFORM=$(python3 -c 'import platform; print(platform.system())')

echo -e "1. Creating new virtual environment..."

python3 -m venv env 

pwd 

echo -e "2. Installing Requirements..."

source env/bin/activate
pip install -r requirements.txt

echo -e "Install is complete."

python3 data/election_crawler/crawler.py


deactivate 
