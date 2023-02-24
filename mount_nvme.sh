#/bin/bash

sudo rm -rf /nvme
sudo mkdir /nvme
sudo chown -R ray /nvme

python mount_nvme.py