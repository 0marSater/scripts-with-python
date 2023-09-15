from operator import itemgetter

import boto3


def delete_snapshot():
    ec2_client = boto3.client('ec2', region_name="eu-west-2")

    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',  # Name here takes many parameters, tag one of them
                'Values': ['prod']  # values of tag
            }
        ]
    )
    for volume in volumes['Volumes']:
        snapshots = ec2_client.describe_snapshots(
            OwnerIds=['self'],
            Filters=[
                {
                    'Name': 'volume-id',
                    'Value': [volume['VolumeId']]
                }
            ]
        )

        for snap in snapshots['Snapshots']:
            print(snap['StartTime'])  # to print unsorted list

        print("################################")

        sorted_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)
        for snap in sorted_snapshot:
            print(snap['StartTime'])

    # for snap in snapshots[2:]:  # start looping at the third element
    #     ec2_client.delete_snapshot(
    #         SnapshotId=snap['SnapshotId']
    #     )
