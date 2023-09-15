import os
import requests
import smtplib
import paramiko
import boto3
import schedule

EMAIL_ADD = os.environ.get('EMAIL_ADD')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
response = requests.get('http://ec2-35-177-55-14.eu-west-2.compute.amazonaws.com:8080/')


def restart_application(hostname, port, username, key_filename):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, key_filename=key_filename)
    stdin, stdout, stderr = ssh.exec_command('sudo -i docker ps')
    data = stdout.read().splitlines()
    # print all running containers
    for line in data:
        containers = line.decode()
        print(containers)

        # extract container id
        columns = containers.split()
        container_id = columns[0]
        image = columns[1]
        if image == 'nginx':
            print(f"\nrestarting container {container_id}")
            stdin, stdout, stderr = ssh.exec_command(f'docker restart {container_id}')
            ssh.close()


def reboot_server(ec2_instance_id):
    ec2_client = boto3.client('ec2', region_name="eu-west-2")
    res = ec2_client.stop_instances(
        InstanceIds=[
            ec2_instance_id,
        ],
    )
    return res


def send_notification(msg):
    global smtp
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADD, EMAIL_PASS)
        smtp.sendmail(EMAIL_ADD, EMAIL_ADD, msg)


def monitor_app():
    try:
        if response.status_code == 200:
            print(f"App is running, Status is {response.status_code}")
            msg = "subject: Site UP\n All things Good!"
            # send_notification(msg)
        else:
            print(f"App is down, Status is {response.status_code}")
            msg = "subject: Site DOWN\n Check the container!"
            # send_notification(msg)
            restart_application('35.177.55.14', 22, 'ec2-user', 'F:\server 1.pem')
    except Exception as ex:
        print(f'Connection error happened {ex}')
        msg = "App not accessible, check the server"
        # send_notification(msg)
        reboot_server("i-0d8e88f754068bd12")


# schedule it every 5 minute
schedule.every(5).minute.do(monitor_app())
while True:
    schedule.run_pending()
