import requests

def deploy_docker_container(api_url, api_key, image_name, container_name):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "image": image_name,
        "name": container_name
    }
    response = requests.post(f'{api_url}/deploy', json=data, headers=headers)
    if response.status_code == 201:
        print("Container deployed successfully")
    else:
        print(f"Failed to deploy container: {response.text}")

# Example usage
api_url = 'https://your-cloud-platform-api.com'
api_key = 'your_api_key_here'
image_name = 'nginx:latest'
container_name = 'my-nginx-container'

deploy_docker_container(api_url, api_key, image_name, container_name)