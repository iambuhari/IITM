import requests
import csv

# Constants
GITHUB_TOKEN = "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"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_users_in_city(city, min_followers=100):
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/search/users?q=location:{city}+followers:>{min_followers}&page={page}&per_page=30"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
        
        data = response.json()
        users.extend(data.get("items", []))
        
        if "next" not in response.links:
            break
        
        page += 1
        
    return users
def get_user_repositories(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=30"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Failed to fetch repos for {username}: {response.status_code}")
            break
        
        data = response.json()
        repos.extend(data)
        
        if "next" not in response.links:
            break
        
        page += 1
        
    return repos
def get_barcelona_users_and_repos():
    barcelona_users = get_users_in_city("Barcelona", 100)
    users_data = []

    for user in barcelona_users:
        user_info = {
            "username": user["login"],
            "followers": user["followers_url"],
            "repos": get_user_repositories(user["login"])
        }
        users_data.append(user_info)

    return users_data

# Fetch data
users_data = get_users_in_city("Barcelona", 100)
#data = get_barcelona_users_and_repos()
# Write data to CSV
with open("barcelona_users.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow(["username", "followers", "repos"])
    
    # Write data rows
    for user in users_data:
        writer.writerow([user["username"], user["followers"], ", ".join(user["repos"])])