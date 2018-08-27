#!/usr/bin/env python
import boto3
import botocore
import argparse
import sys

parser = argparse.ArgumentParser(description='Check if the given AWS VPC exists.')
parser.add_argument('--region_name', dest='region_name', action='store', required=True, help='AWS Region name, e.g. eu-west-1')
parser.add_argument('--vpc_name', dest='vpc_name', action='store', required=True, help='AWS VPC name, e.g. backend_vpc')

args = parser.parse_args()

try:
    conn_ec2 = boto3.resource('ec2', region_name=args.region_name)
except botocore.exceptions.EndpointConnectionError as e:
    sys.stderr.write("EC2: Could not connect to AWS region: %s, check credentials, IAM role privileges, region name." % args.region_name)
    sys.stderr.write(str(e))
    sys.exit(1)

instances = conn_ec2.instances
instances = conn_ec2.instances.filter(Filters=[])
all_vpc_ids = [instance.vpc_id for instance in instances]
all_vpc_ids = list(set(all_vpc_ids))

if len(all_vpc_ids) == 0:
    sys.stderr.write("No VPCs found. Please verify that VPC %s exists and/or create one and try again." % args.vpc_name)
    sys.exit(1)

target_vpc = []
for vpc_id in all_vpc_ids:
    if vpc_id is not None:
        if conn_ec2.Vpc(vpc_id).tags:
            if {'Key': 'Name', 'Value': args.vpc_name} in conn_ec2.Vpc(vpc_id).tags:
                target_vpc.append(vpc_id)

if len(target_vpc) == 0:
    sys.stderr.write("No VPC found. Please verify that VPC %s exists and/or create one and then try again." % args.vpc_name)
    sys.exit(1)

if len(target_vpc) > 1:
    sys.stderr.write("More than one %s VPC found. Please investigate. There can be only one..." % args.vpc_name)
    sys.exit(1)

sys.stdout.write(target_vpc[0])
