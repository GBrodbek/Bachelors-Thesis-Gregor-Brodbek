#!/bin/bash

# if [ "$(ls logs/errors/ | wc -l)" -gt 5 ]; 
#     then 
#         echo "More than 5 files. Deleting"; rm -r logs/*  
# else echo "5 or fewer files. Not deleting logs"; fi

mkdir -p logs/{errors,outputs,logs}

find logs/errors/ -type f -mmin +3 -delete
find logs/logs/ -type f -mtime +2 -delete
find logs/outputs/ -type f -mtime +0.5 -delete

#rm -r qae_hep
rm .tar.gz

mkdir qae_hep
cp ${QML}/*.py qae_hep/
cp -r ${QML}/{helpers,quantum,hydra_configs} qae_hep/

tar -czf qae_hep.tar.gz qae_hep
#xrdcp qae_hep.tar.gz root://eosuser.cern.ch://eos/user/a/aritra/QML/qae_hep.tar.gz

condor_submit submit.sub

condor_watch_q