# Airtable utils

Script to automate various things by leveraging the Airtable API.

## move_bases.py

Move bases from or to a workspace. Bases are definted in a CSV file exported from the Airtable web interface.

Usage: `python3 move_bases.py path/to/file.csv [to|from] WORKSPACE_ID`

Examples: 

Move each base found in file.csv to WORKSPACE_ID:

`python3 move_bases.py file.csv to WORKSPACE_ID` 

Move each base from a specified WORKSPACE_ID to each workspace IDs found in the csv file. This is typically used to rollback a migration done with the "to" keyword:

`python3 move_bases.py file.csv from WORKSPACE_ID` 

## deactivate_users.py

For a list of users in a CSV file, set their state to 'deactivated'.
