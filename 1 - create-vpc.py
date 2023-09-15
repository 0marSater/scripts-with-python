import boto3

ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

new_vpc = ec2_resource.create_vpc(
    CidrBlock="10.0.0.0/16"
)



all_available_vpcs = ec2_client.describe_vpcs()
vpcs = all_available_vpcs["Vpcs"]

for vpc in vpcs:
    print(vpc['VpcId'])
    cidr_block_assoc_sets = vpc["CidrBlockAssociationSet"]
    for assoc_sets in cidr_block_assoc_sets:
        print(assoc_sets['CidrBlockState'])
