# GitHub Deployment Guide

## Push or Replace Existing Repo

Run these commands from the folder that directly contains `app.py`:

```bash
git add .
git commit -m "Fix transaction deletion and data cleaning persistence"
git push --force origin main
```

If this is a new local folder:

```bash
git init
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git add .
git commit -m "Deploy LedgerPro AI bookkeeping app"
git push --force origin main
```

## Streamlit Cloud Settings

```text
Branch: main
Main file path: app.py
```

## Important Data Note

The `data/` folder is runtime storage. It is ignored by Git so private bookkeeping records, temporary receipt images, and local audit files are not pushed to GitHub.

This version includes a one-time legacy migration marker so deleted sample/legacy transactions do not regenerate after cleanup.
