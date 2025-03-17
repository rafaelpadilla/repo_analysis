import csv
import os
import fire
from github import Github, GithubException
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

class GitHubDataExporter:
    def __init__(self, token: str = GITHUB_TOKEN):
        """Initialize GitHub client."""
        self.g = Github(token)
        self.headers = {"Authorization": f"Bearer {token}"}
        self.validate_token()

    def validate_token(self):
        try:
            self.g.get_user().login
            print("GitHub token is valid")
        except GithubException as e:
            raise ValueError(f"Invalid GitHub token {e}")


    def issues(self, repo_name, output_file="issues.csv"):
        """Fetch issues from a repository and save them to a CSV file."""
        repo = self.g.get_repo(repo_name)
        issues = repo.get_issues(state="all")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Issue or Pull", "Issue Number", "Issue Open Date", "Issue Close Date", "Total Days Open",
                "Opened By", "Closed By", "Issue URL", "Body", "State", "Labels", "Comments Count"
            ])

            for issue in issues:
                open_date = issue.created_at.strftime("%Y-%m-%d %H:%M:%S")
                close_date = issue.closed_at.strftime("%Y-%m-%d %H:%M:%S") if issue.closed_at else "N/A"
                days_open = (issue.closed_at - issue.created_at).days if issue.closed_at else "Still Open"
                opened_by = issue.user.login
                closed_by = issue.closed_by.login if issue.closed_by else "N/A"
                labels = ", ".join([label.name for label in issue.labels])
                comments_count = issue.comments
                issue_or_pull = "issue" if f"{repo_name}/issues" in issue.html_url else "pull"

                # We want to skip pull requests
                if issue_or_pull == "pull":
                    continue

                writer.writerow([
                        issue_or_pull, issue.number, open_date, close_date, days_open, opened_by,
                        closed_by, issue.html_url, issue.body.replace("\n", " ") if issue.body else "",
                        issue.state, labels, comments_count
                    ])

        print(f"CSV file '{output_file}' created successfully with issue data from {repo_name}!")


    def pulls(self, repo_name, output_file="pulls.csv"):
        """Fetch pull requests from a repository and save them to a CSV file."""
        repo = self.g.get_repo(repo_name)
        pulls = repo.get_pulls(state="all")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "PR Number", "PR Open Date", "PR Close Date", "Total Days Open",
                "Opened By", "Merged By", "PR URL", "Body", "State", "Labels", "Comments Count"
            ])

            for pr in pulls:
                open_date = pr.created_at.strftime("%Y-%m-%d %H:%M:%S")
                close_date = pr.closed_at.strftime("%Y-%m-%d %H:%M:%S") if pr.closed_at else "N/A"
                days_open = (pr.closed_at - pr.created_at).days if pr.closed_at else "Still Open"
                opened_by = pr.user.login
                merged_by = pr.merged_by.login if pr.merged_by else "N/A"
                labels = ", ".join([label.name for label in pr.labels])
                comments_count = pr.comments

                writer.writerow([
                    pr.number, open_date, close_date, days_open, opened_by,
                    merged_by, pr.html_url, pr.body.replace("\n", " ") if pr.body else "",
                    pr.state, labels, comments_count
                ])

        print(f"CSV file '{output_file}' created successfully with pull request data from {repo_name}!")


    def discussions(self, repo_name, output_file="discussions.csv"):
        """Fetch discussions from a repository using the GitHub GraphQL API and save them to a CSV file."""
        owner, repo = repo_name.split("/")
        query = """
        query ($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            discussions(first: 100) {
              nodes {
                id
                title
                createdAt
                url
                upvoteCount
                answerChosenAt
                author {
                  login
                }
                category {
                  name
                }
                comments {
                  totalCount
                }
              }
            }
          }
        }
        """

        variables = {"owner": owner, "repo": repo}
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=self.headers
        )

        if response.status_code != 200:
            print(f"Error fetching discussions: {response.json()}")
            return

        data = response.json().get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Discussion ID", "Title", "Created At", "Upvote Count",
                "Answer Chosen At", "Author", "Category", "Comments Count", "Discussion URL"
            ])

            for discussion in data:
                created_at = discussion["createdAt"]
                answer_chosen_at = discussion["answerChosenAt"] if discussion["answerChosenAt"] else "N/A"
                author = discussion["author"]["login"] if discussion["author"] else "Unknown"
                category = discussion["category"]["name"]
                comments_count = discussion["comments"]["totalCount"]
                upvote_count = discussion["upvoteCount"]

                writer.writerow([
                    discussion["id"], discussion["title"], created_at, upvote_count,
                    answer_chosen_at, author, category, comments_count, discussion["url"]
                ])

        print(f"CSV file '{output_file}' created successfully with discussion data from {repo_name}!")

if __name__ == "__main__":
    fire.Fire(GitHubDataExporter)