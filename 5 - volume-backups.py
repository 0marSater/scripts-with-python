import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='eu-west-2')


def create_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',  # Name here takes many parameters, tag one of them
                'Values': ['prod']  # values of tag
            }
        ]
    )
    for volume in volumes['Volumes']:
        print(volume)
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(new_snapshot)


schedule.every().monday.do(create_snapshots())

while True:
    schedule.run_pending()
