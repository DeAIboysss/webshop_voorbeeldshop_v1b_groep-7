#!/bin/sh
echo "Shell script for configuring remote connections for this project."
echo "Please respond to the prompts as they come up."
echo "If you want to connect to a remote MongoDB cluster, provide its name below:"
echo "e.g. huwebshoptest-neick.mongodb.net, or leave blank if not applicable."
read -p 'Cluster name: ' MONGODBSERVER
echo ""
echo "If you want to connect to a remote MongoDB cluster, provide your username below:"
echo "e.g. accessUser, or leave blank if not applicable."
read -p 'Username: ' MONGODBUSER
echo ""
echo "If you want to connect to a remote MongoDB cluster, provide your password below:"
echo "Leave blank if not applicable."
read -sp 'Password: ' MONGODBPASSWORD
echo ""
echo ""
echo "If you want to connect to a different recommendation service,"
echo "provide its location below:"
echo "Default (preset) is http://127.0.0.1:5001, leave blank to use default."
read -p 'External service: ' RECOMADDRESS
rm -f .env
echo "MONGODBSERVER=$MONGODBSERVER" >> .env
echo "MONGODBUSER=$MONGODBUSER" >> .env
echo "MONGODBPASSWORD=$MONGODBPASSWORD" >> .env
echo "RECOMADDRESS=$RECOMADDRESS" >> .env
echo ""
echo "Thank you! Please run the huw.sh and huw_recommend.sh scripts again if you want to start using these settings."