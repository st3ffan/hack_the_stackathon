# Hack the Stackathon demo examples

This directory contains sample applications used for the *MongoDB Hack the Stackathon* demo


Note the `.demo_env` file which should be populated with credentials from your Atlas cluster and then sourced before attempting to connect to either Atlas or Voyage APIs.

It can be executed in the current shell by using
`. .dbenv` if *.demo_env* is in your current directory, or `. ~/.demo_env`


## webapp
This demonstrates two variants of a simple Python webapp - one uses sample data in an array, the other demonstrates minimal code changes to connect to an Atlas database.  This app will listens on port 8080

## voyage
This is a Python example that generates embeddings for the images 
## voyage_search
This is Python web app demonstrates using the Voyage API to generate an embedding for a query and performing a search using MongoDB's Vector Search.  This app listens on port *8081*

## gemini_app
This is an example of a web app "Vibe coded" using the Gemini CLI.  It successfully connects, retrieves documents and displays them on the terminal in a tabular form.

## assets
Contains some Creative Commons licensed images used for the voyage_search demo


## connect.sh
Small bash script to open a `mongosh` connection to your configured cluster and database

## import.sh
Bash script to import the corporation data into the cluster
