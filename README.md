# LedgerFlow AI — Cloud-Persistent Bookkeeping App

LedgerFlow AI is a QuickBooks/Xero-style Streamlit bookkeeping app with strict multilingual UI support and Google Sheets cloud persistence.

## Core Features

- User account management with duplicate-name validation
- Manual transaction entry
- Receipt photo / screenshot capture with Gemini AI recognition
- AI-suggested income/expense treatment with final user review
- Multi-currency transaction fields and exchange-rate-to-base-currency tracking
- Transaction nature, payment method, review status, tax flag, attachment reference, and notes
- Data Cleaning Center for editing and deleting transactions
- Dashboard, P&L, cash flow, category breakdown, close readiness, and audit log
- Strict language switching: Traditional Chinese, Simplified Chinese, and English
- Google Sheets cloud persistence for accounts, transactions, and audit logs

## Cloud Persistence

When deployed to Streamlit Cloud, local CSV files can reset after restart or redeploy. This version stores operational bookkeeping records in Google Sheets when secrets are configured.

The app writes these worksheets automatically:

- `user_accounts`
- `transactions`
- `audit_log`

## Streamlit Secrets

Create a Google Sheet, share it with your Google Cloud service account email, then add secrets in Streamlit Cloud:

```toml
[google_sheets]
spreadsheet_id = "YOUR_GOOGLE_SHEET_ID"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

Do not commit real secrets to GitHub.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Local CSV mode is still supported for development, but production persistence should use Google Sheets.
