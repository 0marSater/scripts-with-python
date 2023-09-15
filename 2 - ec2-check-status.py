import boto3
import schedule as schedule

ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

reservations = ec2_client.describe_instances()

def check_instance_status():
    for reservation in reservations['Reservations']:
        instances = reservation['Instances']
        for instance in instances:
            print(f"Instance {instance['InstanceId']} is {instance['State']['Name']}")
    statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['systemStatus']['Status']
        print(f"Status of {instance['InstanceId']} is {ins_status} and system status is {sys_status}")

check_instance_status()
# schedule.every(5).minute.do(check_instance_status())
# while True:
#    schedule.run_pending()
