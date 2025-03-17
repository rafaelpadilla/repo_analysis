# Github Repository Analysis

This project collects data from GitHub repositories using Python.

## 🚀 Features
- GitHub repository data collection for further analysis
- Data processing and storage in CSV
- Collection of Issues, Pull Requests, and Discussions data

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/repo_analysis.git
cd repo_analysis
```

2. Create and activate a Conda environment:
```bash
conda create -n repo_analysis python=3.13
conda activate repo_analysis
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔑 GitHub Token Setup

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with the following permissions:
   - repo (full access)
   - read:discussion
3. Copy the token and add it to your .env file:
```bash
GITHUB_TOKEN=your_token_here
```

## 📊 Usage Examples

The `eval_repo.py` script can collect different types of data from GitHub repositories. Here are some examples:

### Collecting Issues
```bash
python scripts/eval_repo.py issues "owner/repository" "output_issues.csv"
```

### Collecting Pull Requests
```bash
python scripts/eval_repo.py pulls "owner/repository" "output_pulls.csv"
```

### Collecting Discussions
```bash
python scripts/eval_repo.py discussions "owner/repository" "output_discussions.csv"
```

### Output Format

The script generates CSV files with the following information:

- **Issues**: Issue number, open/close dates, duration, authors, labels, etc.
- **Pull Requests**: PR number, open/close dates, duration, authors, merge status, etc.
- **Discussions**: Discussion ID, title, creation date, upvotes, category, etc.

## 📝 Note

Make sure you have sufficient GitHub API rate limits for large repositories. The script will notify you if you encounter any API limitations.