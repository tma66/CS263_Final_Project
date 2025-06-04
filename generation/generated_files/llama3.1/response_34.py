import os
import json
from docker import DockerClient
from requests import Session

# Replace with your account credentials and environment variables
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'

class CloudDeploy:
    def __init__(self):
        self.client = DockerClient(base_url='unix:///var/run/docker.sock')

    def deploy_docker_container(self, container_name, image_name):
        try:
            # Get the ID of the running container
            container_id = self.client.containers.run(
                image=image_name,
                detach=True,
                name=container_name
            )
            print(f"Container {container_name} is deployed.")
        except Exception as e:
            print(f"Failed to deploy container: {e}")

    def create_ec2_instance(self, instance_type, ami_id):
        try:
            # Create an EC2 client session using the AWS credentials
            ec2_session = Session()
            ec2_session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Authorization': f'AWS {AWS_ACCESS_KEY}:{AWS_SECRET_KEY}'
            })

            # Create a new EC2 instance
            instance_id = self.create_ec2_instance(ec2_session, instance_type, ami_id)
            print(f"Instance created: {instance_id}")
        except Exception as e:
            print(f"Failed to create instance: {e}")

    def create_ec2_instance(self, session, instance_type, ami_id):
        url = f'https://ec2.amazonaws.com/'
        params = {
            'Action': 'RunInstances',
            'Version': '2016-11-12',
            'InstanceId': '',
            'ImageId': ami_id,
            'InstanceType': instance_type
        }
        response = session.post(url, data=params)

        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data['Instances'][0]['InstanceId']
        else:
            print(f"Failed to create EC2 instance. Status code: {response.status_code}")
            return None

if __name__ == '__main__':
    deploy = CloudDeploy()
    deploy.deploy_docker_container('my-container', 'nginx:latest')
    # You can call the create_ec2_instance method here