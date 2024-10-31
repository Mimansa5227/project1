## GitHub Users in Chicago Analysis

## How I Scraped the Data
This project uses the GitHub API to scrape data on users in Chicago with over 100 followers, collecting their profile information, including details like name, bio, company, and email, along with metadata on each user’s public repositories, including creation date, primary language, and license.

## Interesting Findings
One of the most surprising findings was the number of users with a significant follower count yet limited public repositories, indicating potential untapped talent in the community.

## Recommendations
Based on this analysis, developers should focus on creating documentation and enabling wiki support for their projects, as these features can significantly enhance project credibility, user engagement, and overall usability, which may lead to higher star counts and sustained community interest in the project.

## Project Overview

This project collects and analyzes data from GitHub profiles based in Chicago with a significant following. The data was processed in Python and saved as CSV files to enable further analysis. Key insights are drawn from this data to offer recommendations to developers for better profile engagement.

## Data Files
- **users.csv**: Contains information about users in Chicago with more than 100 followers.
- **repositories.csv**: Contains details about the public repositories of these users.

### `users.csv`
This file contains details for each Chicago-based user, such as:
- **login**: GitHub username
- **name**: Full name
- **company**: Standardized company name
- **location**: City location
- **email**: Contact email
- **hireable**: Whether open to job opportunities
- **bio**: User bio
- **public_repos**: Count of public repositories
- **followers**: Number of followers
- **following**: Number of people they follow
- **created_at**: Account creation date

### `repositories.csv`
This file holds information on each user's public repositories, including:
- **login**: GitHub username of the repository owner
- **full_name**: Full name of the repository
- **created_at**: Creation date of the repository
- **stargazers_count**: Number of stars
- **watchers_count**: Number of watchers
- **language**: Programming language used
- **has_projects**: Whether projects are enabled
- **has_wiki**: Whether wiki is enabled
- **license_name**: License type


## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to GitHub for providing the API that allows us to gather this data easily.
