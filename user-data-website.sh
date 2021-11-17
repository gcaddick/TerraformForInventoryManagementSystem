#! /bin/bash
sudo yum -y update
pip3 install Flask

mkdir /home/ec2-user/website/
aws s3 sync s3://template-bucket-5623 /home/ec2-user/website/
cd /home/ec2-user/website/
pip3 install -r requirements.txt

python3 WebAppForUsers.py
