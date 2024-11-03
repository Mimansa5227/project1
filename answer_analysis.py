import pandas as pd
import numpy as np
import statsmodels.api as sm
from collections import Counter

# Load Data
def load_user_data(filename='users.csv'):
    return pd.read_csv(filename)

def load_repository_data(filename='repositories.csv'):
    return pd.read_csv(filename)

# 1. Top 5 users in Chicago with the highest number of followers
def top_users_by_followers(users_df):
    chicago_users = users_df[users_df['location'].str.contains("Chicago", case=False, na=False)]
    top_users = chicago_users.nlargest(5, 'followers')['login']
    return ', '.join(top_users)

# 2. 5 earliest registered GitHub users in Chicago
def earliest_registered_users(users_df):
    chicago_users = users_df[users_df['location'].str.contains("Chicago", case=False, na=False)]
    earliest_users = chicago_users.nsmallest(5, 'created_at')['login']
    return ', '.join(earliest_users)

# 3. 3 most popular licenses
def most_popular_licenses(repos_df):
    license_counts = repos_df['license_name'].value_counts().head(3)
    return ', '.join(license_counts.index)

# 4. Majority company developers work at
def majority_company(users_df):
    company_counts = users_df['company'].value_counts().idxmax()
    return company_counts

# 5. Most popular programming language
def most_popular_language(repos_df):
    language_counts = repos_df['language'].value_counts().idxmax()
    return language_counts

# 6. Second most popular language among users who joined after 2020
def second_most_popular_language_post_2020(users_df, repos_df):
    post_2020_users = users_df[users_df['created_at'] > '2020-01-01']
    post_2020_repos = repos_df[repos_df['login'].isin(post_2020_users['login'])]
    language_counts = post_2020_repos['language'].value_counts()
    return language_counts.index[1]

# 7. Language with highest average stars per repo
def language_highest_avg_stars(repos_df):
    avg_stars = repos_df.groupby('language')['stars'].mean()
    return avg_stars.idxmax()

# 8. Top 5 in terms of leader_strength
def top_leader_strength(users_df):
    users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])
    top_users = users_df.nlargest(5, 'leader_strength')['login']
    return ', '.join(top_users)

# 9. Correlation between followers and repos
def followers_repos_correlation(users_df):
    chicago_users = users_df[users_df['location'].str.contains("Chicago", case=False, na=False)]
    correlation = chicago_users['followers'].corr(chicago_users['public_repos'])
    return round(correlation, 3)

# 10. Regression slope of followers on repos
def regression_followers_on_repos(users_df):
    X = users_df[['public_repos']]
    y = users_df['followers']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return round(model.params['public_repos'], 3)

# 11. Correlation between projects and wiki enabled
def correlation_projects_wiki(repos_df):
    return round(repos_df['has_projects'].corr(repos_df['has_wiki']), 3)

# 12. Average following difference for hireable vs non-hireable users
def avg_following_hireable_difference(users_df):
    hireable_avg = users_df[users_df['hireable'] == True]['following'].mean()
    non_hireable_avg = users_df[users_df['hireable'] == False]['following'].mean()
    return round(hireable_avg - non_hireable_avg, 3)

# 13. Regression slope of followers on bio word count
def regression_bio_followers(users_df):
    users_df['bio_word_count'] = users_df['bio'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
    X = users_df[['bio_word_count']]
    y = users_df['followers']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return round(model.params['bio_word_count'], 3)

# 14. Top 5 users creating most repos on weekends
def top_users_weekend_repos(repos_df):
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
    repos_df['weekday'] = repos_df['created_at'].dt.dayofweek
    weekend_repos = repos_df[repos_df['weekday'].isin([5, 6])]
    top_users = weekend_repos['login'].value_counts().head(5)
    return ', '.join(top_users.index)

# 15. Email sharing difference for hireable vs non-hireable users
def email_sharing_difference(users_df):
    hireable_with_email = users_df[users_df['hireable'] == True]['email'].notnull().mean()
    non_hireable_with_email = users_df[users_df['hireable'] == False]['email'].notnull().mean()
    return round(hireable_with_email - non_hireable_with_email, 3)

# 16. Most common surname
def most_common_surname(users_df):
    users_df['surname'] = users_df['name'].apply(lambda x: str(x).strip().split()[-1] if pd.notnull(x) else '')
    surname_counts = Counter(users_df['surname'])
    most_common = surname_counts.most_common()
    max_count = most_common[0][1]
    common_surnames = sorted([name for name, count in most_common if count == max_count])
    return ', '.join(common_surnames)

if __name__ == "__main__":
    users_df = load_user_data()
    repos_df = load_repository_data()
    
    print("1. Top 5 users in Chicago with highest followers:", top_users_by_followers(users_df))
    print("2. 5 earliest registered GitHub users in Chicago:", earliest_registered_users(users_df))
    print("3. 3 most popular licenses:", most_popular_licenses(repos_df))
    print("4. Company with most developers:", majority_company(users_df))
    print("5. Most popular programming language:", most_popular_language(repos_df))
    print("6. Second most popular language for users joined after 2020:", second_most_popular_language_post_2020(users_df, repos_df))
    print("7. Language with highest average stars per repo:", language_highest_avg_stars(repos_df))
    print("8. Top 5 users by leader_strength:", top_leader_strength(users_df))
    print("9. Correlation between followers and repos:", followers_repos_correlation(users_df))
    print("10. Regression slope of followers on repos:", regression_followers_on_repos(users_df))
    print("11. Correlation between projects and wiki enabled:", correlation_projects_wiki(repos_df))
    print("12. Average following difference (hireable vs non-hireable):", avg_following_hireable_difference(users_df))
    print("13. Regression slope of followers on bio word count:", regression_bio_followers(users_df))
    print("14. Top 5 users with most repos on weekends:", top_users_weekend_repos(repos_df))
    print("15. Email sharing difference (hireable vs non-hireable):", email_sharing_difference(users_df))
    print("16. Most common surname(s):", most_common_surname(users_df))
