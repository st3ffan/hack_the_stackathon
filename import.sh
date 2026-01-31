#!/bin/bash

# Run your .demo_env file to set the environment variables
# e.g. $ . ./.demo_env

JSON_FILE=fortune_10.json

# Execute the import
mongoimport --uri  "$DEMO_CLUSTER/$DEMO_DB?authSource=%24external&authMechanism=MONGODB-X509&tlsCertificateKeyFile=$DEMO_CERT" \
	--collection corporations \
	--type JSON \
	--jsonArray \
	--file $JSON_FILE
