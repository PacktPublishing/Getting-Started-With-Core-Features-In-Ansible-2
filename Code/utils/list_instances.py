#!/usr/bin/env python
import boto3
import argparse
import json
import sys

parser = argparse.ArgumentParser(description='Look for EC2 instances.')
parser.add_argument('--region-name', dest='region_name', action='store',
                    required=True, help='AWS Region name, e.g. eu-west-1')
parser.add_argument('--environment', dest='environment', action='store',
                    required=True, help='Environment name, e.g. dev')
parser.add_argument('--org', dest='org', action='store', required=True,
                    help='Organisation name, e.g. org')
parser.add_argument('--application', dest='application', action='store',
                    required=True, help='Application name, e.g. bijou')
parser.add_argument('--application-type', dest='application_type',
                    action='store', required=True,
                    help='Application type, e.g. server, template, api')
parser.add_argument('--instance-state-name', dest='instance_state_name',
                    action='store', required=True,
                    help='AWS EC 2 instance state name, e.g. running')
parser.add_argument('--vpc-name', dest='vpc_name', action='store',
                    required=True, help='VPC name, e.g. bijou-dev-vpc')

args = parser.parse_args()

ec2 = boto3.resource('ec2', region_name=args.region_name)
instances = ec2.instances.filter(Filters=[
    {'Name': 'instance-state-name', 'Values': [args.instance_state_name]},
    {'Name': 'tag:application', 'Values': [args.application]},
    {'Name': 'tag:org', 'Values': [args.org]},
    {'Name': 'tag:environment', 'Values': [args.environment]},
    {'Name': 'tag:type', 'Values': [args.application_type]},
])
instance_list = [instance.id for instance in instances if {'Key': 'Name', 'Value': args.vpc_name} in instance.vpc.tags]
# sys.stdout.write(str(instance_list))
sys.stdout.write(json.dumps(instance_list))
