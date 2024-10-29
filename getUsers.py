import requests
import csv
# Add your GitHub token here
GITHUB_TOKEN = ''
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
def get_users_in_barcelona(min_followers=100):
    users = []
    page = 1

    while True:
        url = f"https://api.github.com/search/users?q=location:Barcelona+followers:>{min_followers}&per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Stop if no more users
        if 'items' not in data or not data['items']:
            break

        users.extend(data['items'])
        page += 1

    return users


def clean_company(company_name):
    if company_name:
        return company_name.strip().lstrip('@').upper()
    return ""

def get_user_details(user_login):
    url = f"https://api.github.com/users/{user_login}"
    response = requests.get(url, headers=headers)
    return response.json()

def save_users_to_csv(users, filename="users.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])
        writer.writeheader()

        for user in users:
            details = get_user_details(user['login'])
            writer.writerow({
                "login": details.get('login'),
                "name": details.get('name'),
                "company": clean_company(details.get('company')),
                "location": details.get('location'),
                "email": details.get('email'),
                "hireable": details.get('hireable'),
                "bio": details.get('bio'),
                "public_repos": details.get('public_repos'),
                "followers": details.get('followers'),
                "following": details.get('following'),
                "created_at": details.get('created_at')
            })

def get_user_repositories(user_login):
    repositories = []
    page = 1

    while len(repositories) < 500:
        url = f"https://api.github.com/users/{user_login}/repos?sort=pushed&per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if not data:
            break

        repositories.extend(data)
        page += 1

    return repositories[:500]

def save_repositories_to_csv(users, filename="repositories.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"])
        writer.writeheader()

        for user in users:
            repositories = get_user_repositories(user['login'])

            for repo in repositories:
                # Check if license is None, and handle it accordingly
                license_name = repo['license']['key'] if repo.get('license') else None
                writer.writerow({
                    "login": user['login'],
                    "full_name": repo.get('full_name'),
                    "created_at": repo.get('created_at'),
                    "stargazers_count": repo.get('stargazers_count'),
                    "watchers_count": repo.get('watchers_count'),
                    "language": repo.get('language'),
                    "has_projects": repo.get('has_projects'),
                    "has_wiki": repo.get('has_wiki'),
                    "license_name": license_name
                })

users = get_users_in_barcelona()
save_users_to_csv(users)
save_repositories_to_csv(users)
