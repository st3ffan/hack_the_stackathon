brew tap mongodb/brew

brew install mongodb-atlas-cli

atlas auth login

atlas dbusers create --username demo_user --role readWrite@hts --x509Type MANAGED

atlas dbusers certs create --username demo_user | tee X509_Cert

atlas clusters connectionStrings describe hts-cluster
