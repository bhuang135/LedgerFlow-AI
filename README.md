# LedgerPro AI Commercial Bookkeeping

QuickBooks/Xero-style commercial bookkeeping app with user account management, transaction-level currency fields, manual entry, Gemini receipt/screenshot capture, data cleaning, reports, exports, and strict multilingual switching.

## Latest Fixes

- Transaction deletion is now permanent. Legacy/demo rows will not regenerate after deletion.
- Added a one-time legacy migration marker so bundled sample CSV data is not re-imported after cleanup.
- Duplicate transactions are now blocked instead of being saved after a warning.
- The Data Cleaning Center supports reviewing, editing, and deleting transaction details for the active user account.
- Runtime data files and temporary images are excluded from GitHub by `.gitignore`.

## Transaction Entry Sources

1. Manual entry
2. Mobile receipt photo capture or receipt image upload
3. Income/expense screenshot upload

Gemini API is used only after the user enters an API key in the sidebar. The key is session-only and is cleared whenever the active user account changes. After a confirmed transaction is saved, temporary image files are deleted.

## Strict Language Switching

The app uses the left sidebar for language selection.

- Traditional Chinese: all application control text is Traditional Chinese.
- Simplified Chinese: all application control text is Simplified Chinese.
- English: all application control text is English.

## Main File

```text
app.py
```

## Local Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

Use:

```text
Main file path: app.py
```
