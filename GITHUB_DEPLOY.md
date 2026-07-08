# GitHub and Streamlit Deployment

## 1. Push to GitHub

```bash
cd C:\Users\Desktop\Git_Bookeeping\ledgerpro_user_accounts_multilingual

git add .
git commit -m "Add Google Sheets cloud persistence"
git push --force origin main
```

## 2. Streamlit Cloud Settings

- Repository: `bhuang135/LedgerFlow-AI`
- Branch: `main`
- Main file path: `app.py`

## 3. Configure Google Sheets Persistence

1. Create a Google Sheet.
2. Copy the spreadsheet ID from the Sheet URL.
3. Create a Google Cloud service account JSON key.
4. Share the Google Sheet with the service account `client_email` as Editor.
5. In Streamlit Cloud, open App → Settings → Secrets.
6. Paste the TOML secrets from `.streamlit/secrets.toml.example` and replace placeholders.
7. Reboot the app.

The app will create and maintain these worksheets:

- `user_accounts`
- `transactions`
- `audit_log`

After this, bookkeeping records persist in Google Sheets and should not disappear after GitHub updates, Streamlit restarts, or redeploys.
