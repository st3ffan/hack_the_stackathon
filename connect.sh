#!/bin/bash
# Run your .demo_env file to set the environment variables
# e.g. $ . ./.demo_env

mongosh "$DEMO_CLUSTER/$DEMO_DB?authSource=%24external&authMechanism=MONGODB-X509" \
	--apiVersion 1 \
	--tls \
	--tlsCertificateKeyFile $DEMO_CERT

