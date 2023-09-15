from operator import itemgetter

import boto3
import schedule as schedule

ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

instance_id = ""  # or u can grap it with ec2_describe function with reservation and do loop

# fetch all volumes belongs to ec2 instance
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]  # assume the first element of Volumes list is our needed volumes

# fetch all snapshots belongs to volume that belongs to ec2 instance
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Value': [instance_volume['VolumeId']]
        }
    ]
)
# fetch the latest snapshot which is the first item in list [0]
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

# create volume from the latest snapshot
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-2",  # fetch h from instance
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

# attach new volume that created upon the latest snapshot to ec2_instance
# you should do logic for hold on process of attach for couple of seconds till the new volume turns to available state.
# do while loop, or async
ec2_resource.Instance(instance_id).attach_volume(
    VolumeId=new_volume['VolumeId'],  # or do describe_volume and other staff.
    Device='/dev/xvdb'

)
