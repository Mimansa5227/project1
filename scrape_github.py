import requests
import csv

# Token and headers for authentication
GITHUB_TOKEN = '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'  
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Function to get users in Chicago with more than 100 followers
def get_users():
    url = 'https://api.github.com/search/users'
    params = {'q': 'location:Chicago followers:>100', 'per_page': 100}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        users = response.json()['items']
        print(f"Fetched {len(users)} users from Chicago with more than 100 followers.")
        return users
    else:
        print("Failed to fetch users:", response.status_code, response.json())
        return []

# Function to get detailed information about a user
def get_user_details(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch details for {username}: {response.status_code}")
        return None  # Return None if the call fails

# Function to save users to CSV
def save_users_to_csv(users):
    with open('users.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        
        for user in users:
            user_details = get_user_details(user['login'])
            if user_details:  # Check if user details were fetched successfully
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

# Function to save repositories to CSV 
def get_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    params = {'per_page': 500}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Repositories for {username}: {response.json()}")  # Debugging line
        return response.json()
    else:
        print(f"Failed to fetch repositories for {username}: {response.status_code}")
        return []  # Return an empty list if the call fails
    
def save_repositories_to_csv(users):
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])

        for user in users:
            repos = get_repositories(user['login'])
            print(f"Fetching repositories for user: {user['login']}")  # Debugging line
            print(f"Repositories fetched: {repos}")  # Debugging line to see the fetched repos
            if repos:
                print(f"Fetched {len(repos)} repositories for user {user['login']}.")
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
                        repo.get('license', {}).get('name', '') if repo.get('license') is not None else ''
                    ])
            else:
                print(f"No repositories found for user {user['login']}.")                

if __name__ == "__main__":
    users = get_users()
    if users:
        save_users_to_csv(users)
        save_repositories_to_csv(users)
        print("Users saved to users.csv")
        print("Repositories saved to repositories.csv")
    else:
        print("No users found.")
