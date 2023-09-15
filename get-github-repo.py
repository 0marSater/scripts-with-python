
import requests

response = requests.get("https://api.github.com/users/0marSater/repos")
if response.status_code == 200:
    repositories = response.json()

    # Print the names of all the repositories
    print(f"Repositories for user omar sater:")
    for repo in repositories:
        if repo['name'] == '0marSater':
            continue
        else:
            print(f"Project Name: {repo['name']}\nURL: {repo['html_url']}\n")
else:
    print(f"Request failed with status code: {response.status_code}")