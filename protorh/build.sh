#brew services start postgresql
#createdb protorh -U 
#psql -d protorh -f database_rh.psql
#psql -U ilyes --password -d protorh

# Installing Python packages listed in requirements.txt
pip3 install -r requirements.txt

# This command migrates the tables from the database_rh file into db postgres.
psql -U postgres -d protorh_api2  < database_rh.psql