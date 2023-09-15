import boto3

ec2_client_london = boto3.client('ec2', region_name="eu-west-2")
ec2_resource_london = boto3.resource('ec2', region_name="eu-west-2")

reservations = ec2_client_london.describe_instances()

for reservation in reservations['Reservations']:
    instances = reservation['Instances']
    instance_id = []
    for instance in instances:
        instance_id.append(instance['InstanceId'])

# print(instance_id)

response = ec2_resource_london.create_tags(
    Resource=instance_id,
    Tags=[
        {
            'Key': 'env',
            'Value': 'prod'
        },
    ]
)
