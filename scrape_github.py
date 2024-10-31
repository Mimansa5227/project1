import requests
import csv

# Token and headers for authentication
GITHUB_TOKEN = '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'  
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Function to get users in Chicago with more than 100 followers, with pagination
def get_users():
    url = 'https://api.github.com/search/users'
    users = []
    page = 1

    while True:
        params = {'q': 'location:Chicago followers:>100', 'per_page': 100, 'page': page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            items = response.json().get('items', [])
            if not items:  # Break if no more users are returned
                break
            users.extend(items)
            print(f"Fetched {len(items)} users on page {page}.")
            page += 1
        else:
            print("Failed to fetch users:", response.status_code, response.json())
            break

    print(f"Total users fetched: {len(users)}")
    return users

# Function to get detailed information about a user
def get_user_details(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch details for {username}: {response.status_code}")
        return None

# Function to save users to CSV
def save_users_to_csv(users):
    with open('users.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        
        for user in users:
            user_details = get_user_details(user['login'])
            if user_details:
                writer.writerow([
                    user_details['login'],
                    user_details.get('name', ''),
                    clean_company(user_details.get('company', '')),
                    user_details.get('location', ''),
                    user_details.get('email', ''),
                    user_details.get('hireable', ''),
                    user_details.get('bio', ''),
                    user_details.get('public_repos', 0),
                    user_details.get('followers', 0),
                    user_details.get('following', 0),
                    user_details.get('created_at', '')
                ])

def clean_company(company):
    if company:
        return company.strip().lstrip('@').upper()
    return ''

# Function to get repositories for a user
def get_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    params = {'per_page': 100}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories for {username}: {response.status_code}")
        return []

# Function to save repositories to CSV 
def save_repositories_to_csv(users):
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])

        for user in users:
            repos = get_repositories(user['login'])
            if repos:
                for repo in repos:
                    writer.writerow([
                        user['login'],
                        repo.get('full_name', ''),
                        repo.get('created_at', ''),
                        repo.get('stargazers_count', 0),
                        repo.get('watchers_count', 0),
                        repo.get('language', ''),
                        repo.get('has_projects', False),
                        repo.get('has_wiki', False),
                        repo.get('license', {}).get('name', '') if repo.get('license') else ''
                    ])

if __name__ == "__main__":
    users = get_users()
    if users:
        save_users_to_csv(users)
        save_repositories_to_csv(users)
        print("Users saved to users.csv")
        print("Repositories saved to repositories.csv")
    else:
        print("No users found.")
