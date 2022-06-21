#!/usr/bin/env python3
# Title:    Move Airtable bases from one workspace to another workspace
# Date :    2022/06/20
# Author:   jean-carol.forato@dataiku.com, lyronn.levy@dataiku.com
# Version:  0.4

from typing import List, Mapping
import requests
import json
import csv
from os import environ
from sys import argv
from pathlib import Path

api_token = environ.get("AIRTABLE_API_TOKEN", None)
if not api_token:
  print("Please set your Airtable API token by typing 'export AIRTABLE_API_TOKEN=MYTOKEN'")
  exit(1)

headers = {"Authorization": f"Bearer {api_token}"}
processed_ids_path = Path() / "processed.txt"
processed_ids = []

if processed_ids_path.exists():
  print(f"{processed_ids_path.name} exists, loading its base ids to avoid processing those again...")
  with open(processed_ids_path, 'r') as f:
    processed_ids = [line.rstrip() for line in f]




def main(args: List):
  """
  Read CSV file, move bases to workspace ID specified as second argument.
  """
  target_workspace_id = argv[2] # "wspFNHbeGzSclvgLi"
  if not target_workspace_id:
    print(f"Target workspace Id is required.")
    exit(1)

  # First argument should be path to CSV file to read
  input_file = Path(args[1])
  
  if not input_file.exists():
    print(f"Input file {input_file.name} is not found.")
    exit(1)

  processed = []
  failed = []

  with open(input_file, 'r') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    if not csv_reader:
      print(f"No data found in input file {input_file.name}. Exiting.")
      exit(1)

    for row in csv_reader:
      base_id = row.get("Base ID")
      workspace_id = row.get("Workspace ID")
      record_count = row.get("Record count", None)

      if base_id in processed_ids:
        # We have processed this one before and successfully moved it
        continue

      if int(record_count):
        print(f"Warning: found {record_count} records in base {base_id}.")

      if not workspace_id or not isinstance(workspace_id, str):
        print(f"Invalid origin workspace id: {workspace_id}. Skipping.")
        continue

      url = "https://api.airtable.com/v0/meta/workspaces/" + workspace_id + "/moveBase"
      body = {
        "baseId": base_id,
        "targetWorkspaceId": target_workspace_id,
      }
      print(
        f"Moving base {base_id} from workspace {workspace_id} "
        f"to workspace {target_workspace_id}..."
      )

      try:
        response = requests.post(url, headers=headers, json=body)
        
        status_code = response.status_code
        if status_code != 200:
          print(f"Status: {response.status_code}")

        try:
          json_response = response.json()
          if json_response:
            print(f"Got response: {json.dumps(json_response, indent=2)}")
        except:
          pass

        response.raise_for_status()

        processed.append(base_id)
        with open(processed_ids_path, 'a') as fp:
          fp.write(f"{base_id}\n")

      except Exception as e:
        print(f"Error sending the request: {e}")
        failed.append(base_id)
  
  print(f"Sucessfully processed {len(processed)} entries from {input_file.name}.")
  if failed:
    print(f"Failed to process {len(failed)} base ids: {failed}.")


if __name__ == "__main__":
  if len(argv) != 3:
    print(
      f"Usage: python3 {__file__.split('/')[-1]} \"path/to/file.csv\" \"Target Workspace ID\"")
    exit(1)
  main(argv)
