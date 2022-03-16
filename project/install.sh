PLATFORM=$(python3 -c 'import platform; print(platform.system())')

echo -e "1. Creating new virtual environment..."

python3 -m venv env 



echo -e "2. Installing Requirements..."

source env/bin/activate
pip install -r requirements.txt

echo -e "Install is complete."

echo -e "3. Running Crawler..."


python3 data/election_crawler/crawler.py


echo -e "4. Getting Data from CDC and merging with Control/Election Data.. "


python3 data/merge.py 


echo -e "5. Running Regression.. "


cp data/data.csv regression

python3 regression/regression.py


echo -e "6. Creating Map.. "

python3 visualization/map_dem_rep.py







deactivate 
