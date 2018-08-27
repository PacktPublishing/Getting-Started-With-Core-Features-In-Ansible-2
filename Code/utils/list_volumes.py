#!/usr/bin/env python
import boto3
import argparse
import sys

parser = argparse.ArgumentParser(description='Look for EC2 instances.')
parser.add_argument('--region-name', dest='region_name', action='store', required=True, help='AWS Region name, e.g. eu-west-1')

args = parser.parse_args()

ec2 = boto3.resource('ec2', region_name=args.region_name)
volumes = ec2.volumes.filter(Filters=[])
volume_list = (volume for volume in volumes) # if { 'Key': 'Name', 'Value': args.vpc_name } in instance.vpc.tags]
unattached_volume_list = []
for volume in volume_list:
    volume_is_attached = False
    if volume.attachments:
        continue
    else:
        unattached_volume_list.append(volume.id)

sys.stdout.write(str(unattached_volume_list))
