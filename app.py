from __future__ import annotations

import uuid
import json
import os
import re
from datetime import date, datetime, timedelta
from io import BytesIO, StringIO
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except Exception:  # Google Sheets support is optional for local development.
    gspread = None
    Credentials = None

from translations import (
    ACCOUNT_LABELS,
    ACTION_LABELS,
    CATEGORY_LABELS,
    ENTITY_TYPE_LABELS,
    LANG_NAMES,
    LANG_OPTIONS,
    PAYMENT_METHOD_LABELS,
    STATUS_LABELS,
    TRANSACTION_NATURE_LABELS,
    TYPE_LABELS,
    label,
    reverse_label,
    t,
)

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "user_accounts.csv"
TRANSACTION_FILE = DATA_DIR / "transactions.csv"
AUDIT_FILE = DATA_DIR / "audit_log.csv"
TEMP_DIR = DATA_DIR / "temp_images"
TEMP_DIR.mkdir(exist_ok=True)
LEGACY_FILE = APP_DIR / "finance_ledger.csv"
MIGRATION_SENTINEL = DATA_DIR / ".legacy_migration_completed"

GOOGLE_SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
GSHEET_USERS_TAB = "user_accounts"
GSHEET_TRANSACTIONS_TAB = "transactions"
GSHEET_AUDIT_TAB = "audit_log"

USER_COLUMNS = [
    "user_id",
    "display_name",
    "entity_type",
    "email",
    "country_region",
    "tax_id",
    "industry",
    "base_currency",
    "opening_balance",
    "notes",
    "created_at",
    "updated_at",
]

TRANSACTION_COLUMNS = [
    "transaction_id",
    "user_id",
    "user_name",
    "date",
    "type",
    "account",
    "category",
    "payee",
    "description",
    "amount",
    "currency",
    "exchange_rate",
    "base_amount",
    "transaction_nature",
    "payment_method",
    "status",
    "tax_related",
    "attachment_ref",
    "notes",
    "created_at",
    "updated_at",
]
AUDIT_COLUMNS = ["timestamp", "action", "transaction_id", "user_id", "user_name", "details"]

TYPE_TO_ACCOUNTS = {
    "Income": ["Sales Revenue", "Service Revenue", "Other Income"],
    "Expense": [
        "Cost of Goods Sold",
        "Rent Expense",
        "Utilities Expense",
        "Meals & Entertainment",
        "Travel & Transportation",
        "Software & Subscriptions",
        "Professional Fees",
        "Office Expense",
        "Other Expense",
    ],
}
TYPE_TO_CATEGORIES = {
    "Income": ["Salary", "Client Payment", "Investment", "Bonus", "Freelance", "Other"],
    "Expense": [
        "Food",
        "Transport",
        "Rent",
        "Utilities",
        "Entertainment",
        "Software",
        "Professional Services",
        "Office Supplies",
        "Other",
    ],
}
PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "ACH", "Other"]
STATUSES = ["Reviewed", "Needs Review"]
CURRENCIES = ["USD", "TWD", "CNY", "EUR", "JPY", "GBP", "CAD", "AUD"]
ENTITY_TYPES = ["Individual", "Sole Proprietor", "LLC", "Corporation", "Client Account"]
TRANSACTION_NATURES = [
    "Operating",
    "Owner Contribution",
    "Owner Draw",
    "Reimbursable",
    "Refund",
    "Transfer",
    "Tax Payment",
    "Non-operating",
]

st.set_page_config(
    page_title="LedgerPro AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
[data-testid="stSidebar"] {background: #F8FBFE;}
[data-testid="collapsedControl"] {display: block;}
.block-container {padding-top: 1.3rem; padding-bottom: 3rem; max-width: 1280px;}
.lp-hero {
    padding: 1.35rem 1.55rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #12385C 0%, #1D5C96 48%, #2F9F6A 100%);
    color: white;
    box-shadow: 0 18px 44px rgba(18, 56, 92, 0.20);
    margin: 1.0rem 0 1.0rem 0;
}
.lp-hero h1 {font-size: 2.05rem; margin: 0 0 0.28rem 0; letter-spacing: -0.02em;}
.lp-hero p {margin: 0; opacity: 0.94; font-size: 1rem; line-height: 1.55;}
.lp-card {
    border: 1px solid rgba(49, 87, 125, 0.13);
    border-radius: 18px;
    padding: 1.05rem 1.15rem;
    background: white;
    box-shadow: 0 8px 24px rgba(22, 36, 54, 0.06);
    min-height: 112px;
}
.lp-mini-title {font-size: 0.82rem; color: #5B6776; margin-bottom: 0.35rem;}
.lp-value {font-size: 1.45rem; font-weight: 800; color: #182334;}
.lp-note {font-size: 0.90rem; line-height: 1.55; color: #3F4A58;}
.lp-profile-box {
    border: 1px solid rgba(20,70,112,0.13);
    background: #FBFDFF;
    border-radius: 20px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab-list"] {gap: 0.55rem;}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 999px;
    padding: 0.55rem 1rem;
    background: #F3F7FB;
}
.stTabs [aria-selected="true"] {background: #E6F4EF; color: #0F5132;}
button[kind="primary"], button[kind="secondary"] {border-radius: 999px;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


SIDEBAR_LANG_NAMES = {
    "zh-TW": {"zh-TW": "繁體中文", "zh-CN": "簡體中文", "en": "英文"},
    "zh-CN": {"zh-TW": "繁体中文", "zh-CN": "简体中文", "en": "英文"},
    "en": {"zh-TW": "Traditional Chinese", "zh-CN": "Simplified Chinese", "en": "English"},
}
SIDEBAR_TITLE = {
    "zh-TW": "語言設定",
    "zh-CN": "语言设置",
    "en": "Language Settings",
}
SIDEBAR_SELECT_LABEL = {
    "zh-TW": "選擇介面語言",
    "zh-CN": "选择界面语言",
    "en": "Select Interface Language",
}
SIDEBAR_HELP = {
    "zh-TW": "選擇後，系統介面會切換為繁體中文。",
    "zh-CN": "选择后，系统界面会切换为简体中文。",
    "en": "After selection, the full application interface switches to English.",
}
SIDEBAR_APP_NOTE = {
    "zh-TW": "LedgerPro AI 商業帳務系統",
    "zh-CN": "LedgerPro AI 商业账务系统",
    "en": "LedgerPro AI Commercial Bookkeeping",
}


def init_session_state() -> None:
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if st.session_state.lang not in LANG_OPTIONS:
        st.session_state.lang = "en"
    if "selected_user_id" not in st.session_state:
        st.session_state.selected_user_id = None
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""
    if "api_reset_notice" not in st.session_state:
        st.session_state.api_reset_notice = False
    if "pending_clear_gemini_api_key" not in st.session_state:
        st.session_state.pending_clear_gemini_api_key = False
    if "ai_capture_suggestion" not in st.session_state:
        st.session_state.ai_capture_suggestion = None
    if "ai_capture_source" not in st.session_state:
        st.session_state.ai_capture_source = None
    if "ai_temp_image_path" not in st.session_state:
        st.session_state.ai_temp_image_path = None
    if "capture_widget_nonce" not in st.session_state:
        st.session_state.capture_widget_nonce = str(uuid.uuid4())[:8]


def render_language_sidebar() -> str:
    current_lang = st.session_state.get("lang", "en")
    if current_lang not in LANG_OPTIONS:
        current_lang = "en"
        st.session_state.lang = current_lang
    names = SIDEBAR_LANG_NAMES.get(current_lang, SIDEBAR_LANG_NAMES["en"])
    with st.sidebar:
        st.markdown(f"### 🌐 {SIDEBAR_TITLE[current_lang]}")
        selected_lang = st.radio(
            SIDEBAR_SELECT_LABEL[current_lang],
            LANG_OPTIONS,
            index=LANG_OPTIONS.index(current_lang),
            format_func=lambda code: names[code],
            key="sidebar_language_radio",
        )
        st.caption(SIDEBAR_HELP[selected_lang])
        st.divider()
        st.markdown(f"### 🤖 {t('gemini_sidebar_title', selected_lang)}")
        st.caption(t('gemini_api_notice', selected_lang))
        # Streamlit does not allow changing a widget-backed session_state key
        # after the widget is instantiated in the same run.  When the active
        # account changes, we set a pending flag, rerun, and clear the key
        # here before rendering the password input.
        if st.session_state.get('pending_clear_gemini_api_key'):
            st.session_state['gemini_api_key'] = ''
            st.session_state.pending_clear_gemini_api_key = False
        if st.session_state.get('api_reset_notice'):
            st.warning(t('api_reset_notice', selected_lang))
            st.session_state.api_reset_notice = False
        st.text_input(
            t('gemini_api_key', selected_lang),
            type='password',
            key='gemini_api_key',
            placeholder=t('gemini_api_placeholder', selected_lang),
            help=t('api_key_account_only', selected_lang),
        )
        st.divider()
        st.markdown(f"### ☁️ {t('cloud_storage', selected_lang)}")
        if google_sheets_enabled():
            st.success(t('cloud_connected', selected_lang))
            sid = google_spreadsheet_id() or ''
            st.caption(f"{t('spreadsheet_id', selected_lang)}: {sid[:8]}…")
            err = st.session_state.get('cloud_storage_error', '')
            if err:
                st.warning(err[:220])
        else:
            st.warning(t('cloud_not_connected', selected_lang))
            err = st.session_state.get('cloud_storage_error', '')
            if err:
                st.caption(err[:220])
            st.caption(t('cloud_setup_hint', selected_lang))
        st.divider()
        st.caption(SIDEBAR_APP_NOTE[selected_lang])
    if selected_lang != current_lang:
        st.session_state.lang = selected_lang
        st.rerun()
    return selected_lang


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def default_user_df() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "user_id": "USER-DEFAULT",
            "display_name": "Demo Business",
            "entity_type": "Client Account",
            "email": "",
            "country_region": "United States",
            "tax_id": "",
            "industry": "Small Business",
            "base_currency": "USD",
            "opening_balance": 0.0,
            "notes": "Default demo account",
            "created_at": now_str(),
            "updated_at": now_str(),
        }
    ], columns=USER_COLUMNS)


def _secret_section(name: str) -> Optional[dict]:
    try:
        if name in st.secrets:
            return dict(st.secrets[name])
    except Exception:
        return None
    return None


def _secret_value(*names: str) -> Optional[str]:
    for name in names:
        try:
            value = st.secrets.get(name)
            if value:
                return str(value)
        except Exception:
            pass
    return None


def google_credentials_info() -> Optional[dict]:
    service_account = _secret_section("gcp_service_account") or _secret_section("google_service_account")
    if service_account:
        info = dict(service_account)
        if "private_key" in info and isinstance(info["private_key"], str):
            info["private_key"] = info["private_key"].replace("\\n", "\n")
        return info

    raw_json = _secret_value("gcp_service_account_json", "GOOGLE_SERVICE_ACCOUNT_JSON") or os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw_json:
        try:
            info = json.loads(raw_json)
            if "private_key" in info and isinstance(info["private_key"], str):
                info["private_key"] = info["private_key"].replace("\\n", "\n")
            return info
        except Exception:
            return None
    return None


def google_spreadsheet_id() -> Optional[str]:
    gs = _secret_section("google_sheets") or _secret_section("gsheets")
    if gs:
        for key in ["spreadsheet_id", "sheet_id", "id"]:
            if gs.get(key):
                return str(gs[key]).strip()
    return (
        _secret_value("google_sheet_id", "GOOGLE_SHEET_ID", "spreadsheet_id")
        or os.environ.get("GOOGLE_SHEET_ID")
    )


def is_google_sheets_configured() -> bool:
    return gspread is not None and Credentials is not None and bool(google_credentials_info()) and bool(google_spreadsheet_id())


@st.cache_resource(show_spinner=False)
def _cached_spreadsheet(credentials_json: str, spreadsheet_id: str):
    info = json.loads(credentials_json)
    creds = Credentials.from_service_account_info(info, scopes=GOOGLE_SHEETS_SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id)


def get_google_spreadsheet():
    if not is_google_sheets_configured():
        return None
    try:
        info = google_credentials_info()
        spreadsheet_id = google_spreadsheet_id()
        credentials_json = json.dumps(info, sort_keys=True)
        st.session_state["cloud_storage_error"] = ""
        return _cached_spreadsheet(credentials_json, spreadsheet_id)
    except Exception as exc:
        st.session_state["cloud_storage_error"] = str(exc)
        return None


def google_sheets_enabled() -> bool:
    return get_google_spreadsheet() is not None


def get_or_create_worksheet(title: str, columns: List[str]):
    spreadsheet = get_google_spreadsheet()
    if spreadsheet is None:
        return None

    try:
        try:
            worksheet = spreadsheet.worksheet(title)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=title, rows=1000, cols=max(20, len(columns)))

        try:
            values = worksheet.get_all_values()
        except Exception:
            values = []

        if not values:
            try:
                worksheet.update(values=[columns], range_name="A1")
            except TypeError:
                worksheet.update("A1", [columns])
        else:
            header = values[0]
            missing = [col for col in columns if col not in header]
            if missing:
                new_header = header + missing
                try:
                    worksheet.update(values=[new_header], range_name="A1")
                except TypeError:
                    worksheet.update("A1", [new_header])
        st.session_state["cloud_storage_error"] = ""
        return worksheet
    except Exception as exc:
        # Surface the real reason (permission denied, API not enabled, quota,
        # wrong spreadsheet_id, etc.) instead of letting it crash the app.
        st.session_state["cloud_storage_error"] = (
            f"[{title}] {exc.__class__.__name__}: {exc}"
        )
        return None


def read_google_sheet(title: str, columns: List[str]) -> Optional[pd.DataFrame]:
    worksheet = get_or_create_worksheet(title, columns)
    if worksheet is None:
        return None
    try:
        records = worksheet.get_all_records(default_blank="")
        df = pd.DataFrame(records)
    except Exception as exc:
        st.session_state["cloud_storage_error"] = str(exc)
        return None
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns] if not df.empty else pd.DataFrame(columns=columns)


def write_google_sheet(title: str, columns: List[str], df: pd.DataFrame) -> bool:
    worksheet = get_or_create_worksheet(title, columns)
    if worksheet is None:
        return False
    output = df.copy()
    for col in columns:
        if col not in output.columns:
            output[col] = ""
    output = output[columns].fillna("")
    for col in output.columns:
        output[col] = output[col].apply(lambda x: x.isoformat() if hasattr(x, "isoformat") else x)
    values = [columns] + output.astype(str).values.tolist()
    try:
        worksheet.clear()
        try:
            worksheet.update(values=values, range_name="A1", value_input_option="USER_ENTERED")
        except TypeError:
            worksheet.update("A1", values, value_input_option="USER_ENTERED")
        return True
    except Exception as exc:
        st.session_state["cloud_storage_error"] = str(exc)
        return False


def save_audit_log(df: pd.DataFrame) -> None:
    output = df.copy()
    for col in AUDIT_COLUMNS:
        if col not in output.columns:
            output[col] = ""
    output = output[AUDIT_COLUMNS]
    if google_sheets_enabled():
        write_google_sheet(GSHEET_AUDIT_TAB, AUDIT_COLUMNS, output)
    output.to_csv(AUDIT_FILE, index=False, encoding="utf-8-sig")


def ensure_files() -> None:
    if not USER_FILE.exists():
        default_user_df().to_csv(USER_FILE, index=False, encoding="utf-8-sig")
    if not TRANSACTION_FILE.exists():
        pd.DataFrame(columns=TRANSACTION_COLUMNS).to_csv(TRANSACTION_FILE, index=False, encoding="utf-8-sig")
    if not AUDIT_FILE.exists():
        pd.DataFrame(columns=AUDIT_COLUMNS).to_csv(AUDIT_FILE, index=False, encoding="utf-8-sig")

    # When Google Sheets is configured, create the required cloud tables and
    # seed the user table once.  Runtime data is then read from/written to the
    # cloud sheet so Streamlit restarts or redeploys do not wipe the ledger.
    if google_sheets_enabled():
        users_cloud = read_google_sheet(GSHEET_USERS_TAB, USER_COLUMNS)
        if users_cloud is not None and users_cloud.empty:
            try:
                local_users = pd.read_csv(USER_FILE, dtype={"user_id": str})
            except Exception:
                local_users = pd.DataFrame(columns=USER_COLUMNS)
            write_google_sheet(GSHEET_USERS_TAB, USER_COLUMNS, local_users if not local_users.empty else default_user_df())

        tx_cloud = read_google_sheet(GSHEET_TRANSACTIONS_TAB, TRANSACTION_COLUMNS)
        if tx_cloud is not None and tx_cloud.empty:
            try:
                local_tx = pd.read_csv(TRANSACTION_FILE, dtype={"transaction_id": str, "user_id": str})
            except Exception:
                local_tx = pd.DataFrame(columns=TRANSACTION_COLUMNS)
            if not local_tx.empty:
                write_google_sheet(GSHEET_TRANSACTIONS_TAB, TRANSACTION_COLUMNS, local_tx)

        audit_cloud = read_google_sheet(GSHEET_AUDIT_TAB, AUDIT_COLUMNS)
        if audit_cloud is not None and audit_cloud.empty:
            try:
                local_audit = pd.read_csv(AUDIT_FILE)
            except Exception:
                local_audit = pd.DataFrame(columns=AUDIT_COLUMNS)
            if not local_audit.empty:
                write_google_sheet(GSHEET_AUDIT_TAB, AUDIT_COLUMNS, local_audit)


def read_users() -> pd.DataFrame:
    ensure_files()
    if google_sheets_enabled():
        cloud_df = read_google_sheet(GSHEET_USERS_TAB, USER_COLUMNS)
        if cloud_df is not None:
            df = cloud_df
        else:
            try:
                df = pd.read_csv(USER_FILE, dtype={"user_id": str})
            except Exception:
                df = pd.DataFrame(columns=USER_COLUMNS)
    else:
        try:
            df = pd.read_csv(USER_FILE, dtype={"user_id": str})
        except Exception:
            df = pd.DataFrame(columns=USER_COLUMNS)
    for col in USER_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col != "opening_balance" else 0.0
    df = df[USER_COLUMNS]
    df["opening_balance"] = pd.to_numeric(df["opening_balance"], errors="coerce").fillna(0.0)
    if df.empty:
        df = default_user_df()
        save_users(df)
    df.to_csv(USER_FILE, index=False, encoding="utf-8-sig")
    return df


def save_users(df: pd.DataFrame) -> None:
    output = df.copy()
    for col in USER_COLUMNS:
        if col not in output.columns:
            output[col] = "" if col != "opening_balance" else 0.0
    output = output[USER_COLUMNS]
    if google_sheets_enabled():
        write_google_sheet(GSHEET_USERS_TAB, USER_COLUMNS, output)
    output.to_csv(USER_FILE, index=False, encoding="utf-8-sig")


def normalize_user_name(name: object) -> str:
    return " ".join(str(name or "").strip().lower().split())


def user_name_exists(users: pd.DataFrame, display_name: str, exclude_user_id: Optional[str] = None) -> bool:
    target = normalize_user_name(display_name)
    if not target or users.empty:
        return False
    temp = users.copy()
    if exclude_user_id is not None:
        temp = temp[temp["user_id"].astype(str) != str(exclude_user_id)]
    existing_names = temp["display_name"].apply(normalize_user_name)
    return bool((existing_names == target).any())


def read_audit_log() -> pd.DataFrame:
    ensure_files()
    if google_sheets_enabled():
        cloud_df = read_google_sheet(GSHEET_AUDIT_TAB, AUDIT_COLUMNS)
        if cloud_df is not None:
            return cloud_df
    try:
        return pd.read_csv(AUDIT_FILE)
    except Exception:
        return pd.DataFrame(columns=AUDIT_COLUMNS)


def log_audit(action: str, transaction_id: str, user_id: str, user_name: str, details: str) -> None:
    ensure_files()
    row = pd.DataFrame([
        {
            "timestamp": now_str(),
            "action": action,
            "transaction_id": transaction_id,
            "user_id": user_id,
            "user_name": user_name,
            "details": details,
        }
    ])
    save_audit_log(pd.concat([read_audit_log(), row], ignore_index=True))


def account_from_category(category: str) -> str:
    return {
        "Food": "Meals & Entertainment",
        "Transport": "Travel & Transportation",
        "Rent": "Rent Expense",
        "Utilities": "Utilities Expense",
        "Entertainment": "Meals & Entertainment",
        "Software": "Software & Subscriptions",
        "Professional Services": "Professional Fees",
        "Office Supplies": "Office Expense",
    }.get(category, "Other Expense")


def normalize_type(raw: str) -> str:
    raw = str(raw).strip().lower()
    return "Income" if raw in ["income", "收入", "revenue", "sale", "sales"] else "Expense"


def normalize_category(raw: str) -> str:
    raw_clean = str(raw).strip()
    for key, labels in CATEGORY_LABELS.items():
        if raw_clean == key or raw_clean.lower() == key.lower() or raw_clean in labels.values():
            return key
    return "Other"


def normalize_payment(raw: str) -> str:
    raw_clean = str(raw).strip()
    for key, labels in PAYMENT_METHOD_LABELS.items():
        if raw_clean == key or raw_clean.lower() == key.lower() or raw_clean in labels.values():
            return key
    return "Other"


def normalize_nature(raw: str) -> str:
    raw_clean = str(raw).strip()
    for key, labels in TRANSACTION_NATURE_LABELS.items():
        if raw_clean == key or raw_clean.lower() == key.lower() or raw_clean in labels.values():
            return key
    return "Operating"


def mark_legacy_migration_complete(reason: str = "") -> None:
    """Prevent demo/legacy seed rows from being recreated after users delete them."""
    try:
        MIGRATION_SENTINEL.write_text(f"{now_str()} {reason}".strip(), encoding="utf-8")
    except Exception:
        pass


def legacy_migration_already_logged() -> bool:
    if not AUDIT_FILE.exists():
        return False
    try:
        audit = pd.read_csv(AUDIT_FILE)
        if "action" not in audit.columns:
            return False
        return bool((audit["action"].astype(str) == "MIGRATE_LEGACY").any())
    except Exception:
        return False


def migrate_legacy_if_needed() -> None:
    """
    Import the bundled legacy CSV only once.

    Previous versions recreated legacy/demo transactions whenever the transaction
    table became empty. That caused deleted rows to come back after a cleanup.
    The sentinel file makes deletion permanent while still allowing a first-run
    migration for new installations.
    """
    ensure_files()

    if google_sheets_enabled():
        # In cloud mode, do not seed demo/legacy rows automatically.
        # Real bookkeeping data must remain user-controlled and persistent in Google Sheets.
        mark_legacy_migration_complete("google sheets cloud storage enabled")
        return

    if MIGRATION_SENTINEL.exists():
        return

    try:
        existing = pd.read_csv(TRANSACTION_FILE)
    except Exception:
        existing = pd.DataFrame(columns=TRANSACTION_COLUMNS)

    # If the app already has transactions, consider migration completed so that
    # deleting all transactions later does not trigger another legacy import.
    if not existing.empty:
        mark_legacy_migration_complete("existing transactions detected")
        return

    # If an older app version already logged a migration, do not import again.
    if legacy_migration_already_logged():
        mark_legacy_migration_complete("previous migration audit found")
        return

    if not LEGACY_FILE.exists():
        mark_legacy_migration_complete("no legacy file")
        return

    users = read_users()
    default_user = users.iloc[0]

    try:
        legacy = pd.read_csv(LEGACY_FILE)
    except Exception:
        mark_legacy_migration_complete("legacy file unreadable")
        return

    if legacy.empty:
        mark_legacy_migration_complete("legacy file empty")
        return

    rows = []
    for _, row in legacy.iterrows():
        tx_type = normalize_type(row.get("Type", "Expense"))
        category = normalize_category(row.get("Category", "Other"))
        amount = abs(float(row.get("Amount", 0) or 0))
        currency = str(row.get("Currency", default_user["base_currency"]) or default_user["base_currency"])
        exchange_rate = float(row.get("Exchange Rate", 1) or 1)
        rows.append(
            {
                "transaction_id": str(uuid.uuid4())[:8].upper(),
                "user_id": default_user["user_id"],
                "user_name": default_user["display_name"],
                "date": pd.to_datetime(row.get("Date", date.today()), errors="coerce").date(),
                "type": tx_type,
                "account": "Service Revenue" if tx_type == "Income" else account_from_category(category),
                "category": category,
                "payee": str(row.get("Payee", "Legacy Import")),
                "description": str(row.get("Item", row.get("Description", "Legacy transaction"))),
                "amount": amount,
                "currency": currency,
                "exchange_rate": exchange_rate,
                "base_amount": amount * exchange_rate,
                "transaction_nature": normalize_nature(row.get("Transaction Nature", "Operating")),
                "payment_method": normalize_payment(row.get("Payment Method", "Other")),
                "status": "Reviewed",
                "tax_related": False,
                "attachment_ref": "",
                "notes": "Migrated from legacy ledger",
                "created_at": now_str(),
                "updated_at": now_str(),
            }
        )

    pd.DataFrame(rows, columns=TRANSACTION_COLUMNS).to_csv(TRANSACTION_FILE, index=False, encoding="utf-8-sig")
    log_audit("MIGRATE_LEGACY", "MULTIPLE", str(default_user["user_id"]), str(default_user["display_name"]), f"Imported {len(rows)} legacy rows")
    mark_legacy_migration_complete(f"imported {len(rows)} legacy rows")

def read_transactions() -> pd.DataFrame:
    ensure_files()
    migrate_legacy_if_needed()
    if google_sheets_enabled():
        cloud_df = read_google_sheet(GSHEET_TRANSACTIONS_TAB, TRANSACTION_COLUMNS)
        if cloud_df is not None:
            df = cloud_df
        else:
            try:
                df = pd.read_csv(TRANSACTION_FILE, dtype={"transaction_id": str, "user_id": str})
            except Exception:
                df = pd.DataFrame(columns=TRANSACTION_COLUMNS)
    else:
        try:
            df = pd.read_csv(TRANSACTION_FILE, dtype={"transaction_id": str, "user_id": str})
        except Exception:
            df = pd.DataFrame(columns=TRANSACTION_COLUMNS)
    # Backward compatibility for older versions of this app.
    if "user" in df.columns and "user_name" not in df.columns:
        df["user_name"] = df["user"]
    for col in TRANSACTION_COLUMNS:
        if col not in df.columns:
            if col == "user_id":
                df[col] = "USER-DEFAULT"
            elif col == "user_name":
                df[col] = "Demo Business"
            elif col == "currency":
                df[col] = "USD"
            elif col == "exchange_rate":
                df[col] = 1.0
            elif col == "base_amount":
                df[col] = pd.to_numeric(df.get("amount", 0), errors="coerce").fillna(0.0)
            elif col == "transaction_nature":
                df[col] = "Operating"
            elif col == "attachment_ref":
                df[col] = ""
            else:
                df[col] = None
    df = df[TRANSACTION_COLUMNS]
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["exchange_rate"] = pd.to_numeric(df["exchange_rate"], errors="coerce").fillna(1.0)
        df["base_amount"] = pd.to_numeric(df["base_amount"], errors="coerce").fillna(df["amount"] * df["exchange_rate"])
        df["tax_related"] = df["tax_related"].fillna(False).astype(str).str.lower().isin(["true", "1", "yes", "是"])
    df.to_csv(TRANSACTION_FILE, index=False, encoding="utf-8-sig")
    return df


def save_transactions(df: pd.DataFrame) -> None:
    output = df.copy()
    for col in TRANSACTION_COLUMNS:
        if col not in output.columns:
            output[col] = None
    output = output[TRANSACTION_COLUMNS]
    if not output.empty:
        output["date"] = pd.to_datetime(output["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    if google_sheets_enabled():
        write_google_sheet(GSHEET_TRANSACTIONS_TAB, TRANSACTION_COLUMNS, output)
    output.to_csv(TRANSACTION_FILE, index=False, encoding="utf-8-sig")


def parse_date_text(value: str) -> Optional[date]:
    try:
        return pd.to_datetime(value, errors="raise").date()
    except Exception:
        return None


def format_money(value: float, currency: str = "USD") -> str:
    symbols = {"USD": "$", "TWD": "NT$", "CNY": "¥", "EUR": "€", "JPY": "¥", "GBP": "£", "CAD": "C$", "AUD": "A$"}
    symbol = symbols.get(currency, f"{currency} ")
    return f"{symbol}{value:,.2f}"


def get_active_user(users: pd.DataFrame) -> pd.Series:
    if users.empty:
        ensure_files()
        users = read_users()
    if st.session_state.selected_user_id not in users["user_id"].tolist():
        st.session_state.selected_user_id = str(users.iloc[0]["user_id"])
    return users[users["user_id"] == st.session_state.selected_user_id].iloc[0]


def metrics(df: pd.DataFrame, opening_balance: float = 0.0) -> Dict[str, float | str | int]:
    if df.empty:
        return {"income": 0.0, "expense": 0.0, "net": 0.0, "cash": opening_balance, "expense_ratio": 0.0, "count": 0, "top_expense": "-", "review_needed": 0, "profit_margin": 0.0}
    income = float(df.loc[df["type"] == "Income", "base_amount"].sum())
    expense = float(df.loc[df["type"] == "Expense", "base_amount"].sum())
    net = income - expense
    cash = opening_balance + net
    expense_ratio = expense / income if income else 0.0
    review_needed = int((df["status"] == "Needs Review").sum())
    exp_df = df[df["type"] == "Expense"]
    top_expense = "-" if exp_df.empty else exp_df.groupby("category")["base_amount"].sum().sort_values(ascending=False).index[0]
    profit_margin = net / income if income else 0.0
    return {"income": income, "expense": expense, "net": net, "cash": cash, "expense_ratio": expense_ratio, "count": len(df), "top_expense": top_expense, "review_needed": review_needed, "profit_margin": profit_margin}


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "Income", "Expense", "Net"])
    temp = df.copy()
    temp["month"] = pd.to_datetime(temp["date"], errors="coerce").dt.to_period("M").astype(str)
    pivot = temp.pivot_table(index="month", columns="type", values="base_amount", aggfunc="sum", fill_value=0).reset_index()
    for col in ["Income", "Expense"]:
        if col not in pivot.columns:
            pivot[col] = 0.0
    pivot["Net"] = pivot["Income"] - pivot["Expense"]
    return pivot.sort_values("month")


def display_dataframe(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    display = df.copy()
    display["date"] = pd.to_datetime(display["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    for text_col in ["payee", "description", "notes"]:
        if text_col in display.columns:
            display[text_col] = display[text_col].apply(lambda x: localize_dynamic_text(x, lang))
    display["type"] = display["type"].apply(lambda x: label(str(x), TYPE_LABELS, lang))
    display["account"] = display["account"].apply(lambda x: label(str(x), ACCOUNT_LABELS, lang))
    display["category"] = display["category"].apply(lambda x: label(str(x), CATEGORY_LABELS, lang))
    display["transaction_nature"] = display["transaction_nature"].apply(lambda x: label(str(x), TRANSACTION_NATURE_LABELS, lang))
    display["payment_method"] = display["payment_method"].apply(lambda x: label(str(x), PAYMENT_METHOD_LABELS, lang))
    display["status"] = display["status"].apply(lambda x: label(str(x), STATUS_LABELS, lang))
    display["tax_related"] = display["tax_related"].apply(lambda x: t("tax_yes", lang) if bool(x) else t("tax_no", lang))
    column_map = {
        "transaction_id": t("transaction_id", lang),
        "user_id": t("user_id", lang),
        "user_name": t("user_name", lang),
        "date": t("transaction_date", lang),
        "type": t("type", lang),
        "account": t("account", lang),
        "category": t("category", lang),
        "payee": t("payee", lang),
        "description": t("description", lang),
        "amount": t("amount", lang),
        "currency": t("transaction_currency", lang),
        "exchange_rate": t("exchange_rate", lang),
        "base_amount": t("base_amount", lang),
        "transaction_nature": t("transaction_nature", lang),
        "payment_method": t("payment_method", lang),
        "status": t("status", lang),
        "tax_related": t("tax_related", lang),
        "attachment_ref": t("attachment_ref", lang),
        "notes": t("notes", lang),
        "created_at": t("created_at", lang),
        "updated_at": t("updated_at", lang),
    }
    return display.rename(columns=column_map)


def build_pnl(df: pd.DataFrame, lang: str, currency: str) -> pd.DataFrame:
    m = metrics(df)
    return pd.DataFrame([
        {t("account", lang): t("gross_income", lang), t("amount", lang): format_money(float(m["income"]), currency)},
        {t("account", lang): t("operating_expense", lang), t("amount", lang): format_money(float(m["expense"]), currency)},
        {t("account", lang): t("net_income", lang), t("amount", lang): format_money(float(m["net"]), currency)},
    ])


def make_excel_report(df: pd.DataFrame, lang: str, currency: str, users: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        display_dataframe(df, lang).to_excel(writer, index=False, sheet_name="Transactions")
        monthly_summary(df).rename(columns={"month": t("month", lang), "Income": t("cash_inflow", lang), "Expense": t("cash_outflow", lang), "Net": t("net_cash_flow", lang)}).to_excel(writer, index=False, sheet_name="Cash Flow")
        build_pnl(df, lang, currency).to_excel(writer, index=False, sheet_name="Profit and Loss")
        users.to_excel(writer, index=False, sheet_name="User Accounts")
    return output.getvalue()


def validate_duplicate(df: pd.DataFrame, row: Dict[str, object]) -> bool:
    if df.empty:
        return False
    desc = str(row["description"]).strip().lower()
    matches = df[
        (df["user_id"] == row["user_id"])
        & (df["date"] == row["date"])
        & (df["type"] == row["type"])
        & (df["amount"].round(2) == round(float(row["amount"]), 2))
        & (df["currency"] == row["currency"])
        & (df["description"].astype(str).str.strip().str.lower() == desc)
    ]
    return not matches.empty


def append_transaction(row: Dict[str, object]) -> None:
    df = read_transactions()
    save_transactions(pd.concat([df, pd.DataFrame([row], columns=TRANSACTION_COLUMNS)], ignore_index=True))
    log_audit("CREATE_TRANSACTION", str(row["transaction_id"]), str(row["user_id"]), str(row["user_name"]), str(row["description"]))


def update_transaction(transaction_id: str, updates: Dict[str, object], user_id: str, user_name: str) -> None:
    df = read_transactions()
    if df.empty or transaction_id not in df["transaction_id"].astype(str).tolist():
        return
    idx = df.index[df["transaction_id"].astype(str) == str(transaction_id)][0]
    for key, value in updates.items():
        if key in TRANSACTION_COLUMNS:
            df.at[idx, key] = value
    df.at[idx, "updated_at"] = now_str()
    save_transactions(df)
    log_audit("UPDATE_TRANSACTION", str(transaction_id), user_id, user_name, f"Updated transaction {transaction_id}")


def delete_transaction(transaction_id: str, user_id: str, user_name: str) -> bool:
    """Delete a transaction permanently and return True when a row was removed."""
    df = read_transactions()
    before = len(df)
    tx_id = str(transaction_id).strip()
    if not df.empty:
        df = df[df["transaction_id"].astype(str).str.strip() != tx_id].copy()
    save_transactions(df)
    deleted = len(df) < before
    if deleted:
        # Mark migration complete so legacy/demo rows cannot be recreated when
        # the table becomes empty after cleanup.
        mark_legacy_migration_complete("transaction deleted")
        log_audit("DELETE_TRANSACTION", tx_id, user_id, user_name, "Deleted selected transaction")
    return deleted


DEMO_TEXT_TRANSLATIONS = {
    "Acme 客戶": {"zh-TW": "Acme 客戶", "zh-CN": "Acme 客户", "en": "Acme Client"},
    "Acme 客户": {"zh-TW": "Acme 客戶", "zh-CN": "Acme 客户", "en": "Acme Client"},
    "Acme Client": {"zh-TW": "Acme 客戶", "zh-CN": "Acme 客户", "en": "Acme Client"},
    "雲端工具": {"zh-TW": "雲端工具", "zh-CN": "云端工具", "en": "Cloud Tools"},
    "云端工具": {"zh-TW": "雲端工具", "zh-CN": "云端工具", "en": "Cloud Tools"},
    "Cloud Tools": {"zh-TW": "雲端工具", "zh-CN": "云端工具", "en": "Cloud Tools"},
    "客戶午餐": {"zh-TW": "客戶午餐", "zh-CN": "客户午餐", "en": "Client Lunch"},
    "客户午餐": {"zh-TW": "客戶午餐", "zh-CN": "客户午餐", "en": "Client Lunch"},
    "Client Lunch": {"zh-TW": "客戶午餐", "zh-CN": "客户午餐", "en": "Client Lunch"},
    "辦公室租約": {"zh-TW": "辦公室租約", "zh-CN": "办公室租约", "en": "Office Lease"},
    "办公室租约": {"zh-TW": "辦公室租約", "zh-CN": "办公室租约", "en": "Office Lease"},
    "Office Lease": {"zh-TW": "辦公室租約", "zh-CN": "办公室租约", "en": "Office Lease"},
    "Beta 客戶": {"zh-TW": "Beta 客戶", "zh-CN": "Beta 客户", "en": "Beta Client"},
    "Beta 客户": {"zh-TW": "Beta 客戶", "zh-CN": "Beta 客户", "en": "Beta Client"},
    "Beta Client": {"zh-TW": "Beta 客戶", "zh-CN": "Beta 客户", "en": "Beta Client"},
    "會計師事務所": {"zh-TW": "會計師事務所", "zh-CN": "会计师事务所", "en": "CPA Firm"},
    "会计师事务所": {"zh-TW": "會計師事務所", "zh-CN": "会计师事务所", "en": "CPA Firm"},
    "CPA Firm": {"zh-TW": "會計師事務所", "zh-CN": "会计师事务所", "en": "CPA Firm"},
    "每月顧問服務收入": {"zh-TW": "每月顧問服務收入", "zh-CN": "每月顾问服务收入", "en": "Monthly consulting invoice"},
    "每月顾问服务收入": {"zh-TW": "每月顧問服務收入", "zh-CN": "每月顾问服务收入", "en": "Monthly consulting invoice"},
    "Monthly consulting invoice": {"zh-TW": "每月顧問服務收入", "zh-CN": "每月顾问服务收入", "en": "Monthly consulting invoice"},
    "分析軟體訂閱": {"zh-TW": "分析軟體訂閱", "zh-CN": "分析软件订阅", "en": "Analytics software subscription"},
    "分析软件订阅": {"zh-TW": "分析軟體訂閱", "zh-CN": "分析软件订阅", "en": "Analytics software subscription"},
    "Analytics software subscription": {"zh-TW": "分析軟體訂閱", "zh-CN": "分析软件订阅", "en": "Analytics software subscription"},
    "商務午餐": {"zh-TW": "商務午餐", "zh-CN": "商务午餐", "en": "Business lunch"},
    "商务午餐": {"zh-TW": "商務午餐", "zh-CN": "商务午餐", "en": "Business lunch"},
    "Business lunch": {"zh-TW": "商務午餐", "zh-CN": "商务午餐", "en": "Business lunch"},
    "每月辦公室租金": {"zh-TW": "每月辦公室租金", "zh-CN": "每月办公室租金", "en": "Monthly office rent"},
    "每月办公室租金": {"zh-TW": "每月辦公室租金", "zh-CN": "每月办公室租金", "en": "Monthly office rent"},
    "Monthly office rent": {"zh-TW": "每月辦公室租金", "zh-CN": "每月办公室租金", "en": "Monthly office rent"},
    "專案階段收款": {"zh-TW": "專案階段收款", "zh-CN": "项目阶段收款", "en": "Project milestone payment"},
    "项目阶段收款": {"zh-TW": "專案階段收款", "zh-CN": "项目阶段收款", "en": "Project milestone payment"},
    "Project milestone payment": {"zh-TW": "專案階段收款", "zh-CN": "项目阶段收款", "en": "Project milestone payment"},
    "帳務覆核服務": {"zh-TW": "帳務覆核服務", "zh-CN": "账务复核服务", "en": "Bookkeeping review service"},
    "账务复核服务": {"zh-TW": "帳務覆核服務", "zh-CN": "账务复核服务", "en": "Bookkeeping review service"},
    "Bookkeeping review service": {"zh-TW": "帳務覆核服務", "zh-CN": "账务复核服务", "en": "Bookkeeping review service"},
    "示範資料": {"zh-TW": "示範資料", "zh-CN": "示范数据", "en": "Demo data"},
    "示范数据": {"zh-TW": "示範資料", "zh-CN": "示范数据", "en": "Demo data"},
    "Demo data": {"zh-TW": "示範資料", "zh-CN": "示范数据", "en": "Demo data"},
}


def localize_dynamic_text(value: object, lang: str) -> str:
    text = str(value) if value is not None else ""
    return DEMO_TEXT_TRANSLATIONS.get(text, {}).get(lang, text)


def find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    lowered = {str(c).strip().lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    return None


def import_pasted_csv(text: str, active_user: pd.Series) -> int:
    imported = pd.read_csv(StringIO(text.strip()))
    date_col = find_column(imported, ["Date", "date", "日期", "交易日期"])
    type_col = find_column(imported, ["Type", "type", "類型", "类型"])
    category_col = find_column(imported, ["Category", "category", "分類", "分类", "管理分類", "管理分类"])
    description_col = find_column(imported, ["Description", "description", "Item", "item", "說明", "说明", "交易說明", "交易说明"])
    amount_col = find_column(imported, ["Amount", "amount", "金額", "金额"])
    payee_col = find_column(imported, ["Payee", "payee", "交易對象", "交易对象"])
    payment_col = find_column(imported, ["Payment Method", "payment_method", "付款方式"])
    currency_col = find_column(imported, ["Currency", "currency", "幣別", "币别", "交易幣別", "交易币别"])
    rate_col = find_column(imported, ["Exchange Rate", "exchange_rate", "匯率", "汇率"])
    nature_col = find_column(imported, ["Transaction Nature", "transaction_nature", "交易性質", "交易性质"])
    if not all([date_col, type_col, category_col, description_col, amount_col]):
        raise ValueError("missing required columns")
    rows = []
    for _, row in imported.iterrows():
        tx_type = normalize_type(row.get(type_col, "Expense"))
        category = normalize_category(row.get(category_col, "Other"))
        amount = abs(float(row.get(amount_col, 0) or 0))
        tx_date = pd.to_datetime(row.get(date_col, date.today()), errors="coerce").date()
        currency = str(row.get(currency_col, active_user["base_currency"]) if currency_col else active_user["base_currency"]).upper()
        exchange_rate = float(row.get(rate_col, 1) if rate_col else 1)
        rows.append({
            "transaction_id": str(uuid.uuid4())[:8].upper(),
            "user_id": active_user["user_id"],
            "user_name": active_user["display_name"],
            "date": tx_date,
            "type": tx_type,
            "account": "Service Revenue" if tx_type == "Income" else account_from_category(category),
            "category": category,
            "payee": str(row.get(payee_col, "Imported") if payee_col else "Imported"),
            "description": str(row.get(description_col, "Imported transaction")),
            "amount": amount,
            "currency": currency if currency in CURRENCIES else active_user["base_currency"],
            "exchange_rate": exchange_rate,
            "base_amount": amount * exchange_rate,
            "transaction_nature": normalize_nature(row.get(nature_col, "Operating") if nature_col else "Operating"),
            "payment_method": normalize_payment(row.get(payment_col, "Other") if payment_col else "Other"),
            "status": "Needs Review",
            "tax_related": False,
            "attachment_ref": "",
            "notes": "Pasted import",
            "created_at": now_str(),
            "updated_at": now_str(),
        })
    if rows:
        save_transactions(pd.concat([read_transactions(), pd.DataFrame(rows, columns=TRANSACTION_COLUMNS)], ignore_index=True))
        log_audit("IMPORT_TRANSACTIONS", "MULTIPLE", str(active_user["user_id"]), str(active_user["display_name"]), f"Imported {len(rows)} rows")
    return len(rows)


def sample_rows(active_user: pd.Series, lang: str) -> pd.DataFrame:
    today = date.today()
    if lang == "zh-TW":
        payees = ["Acme 客戶", "雲端工具", "客戶午餐", "辦公室租約", "Beta 客戶", "會計師事務所"]
        descs = ["每月顧問服務收入", "分析軟體訂閱", "商務午餐", "每月辦公室租金", "專案階段收款", "帳務覆核服務"]
    elif lang == "zh-CN":
        payees = ["Acme 客户", "云端工具", "客户午餐", "办公室租约", "Beta 客户", "会计师事务所"]
        descs = ["每月顾问服务收入", "分析软件订阅", "商务午餐", "每月办公室租金", "项目阶段收款", "账务复核服务"]
    else:
        payees = ["Acme Client", "Cloud Tools", "Client Lunch", "Office Lease", "Beta Client", "CPA Firm"]
        descs = ["Monthly consulting invoice", "Analytics software subscription", "Business lunch", "Monthly office rent", "Project milestone payment", "Bookkeeping review service"]
    base = active_user["base_currency"]
    base_rows = [
        (today.replace(day=1), "Income", "Service Revenue", "Client Payment", payees[0], descs[0], 5200.00, base, 1.0, "ACH", True, "Operating"),
        (today.replace(day=min(3, today.day)), "Expense", "Software & Subscriptions", "Software", payees[1], descs[1], 89.00, base, 1.0, "Credit Card", True, "Operating"),
        (today.replace(day=min(5, today.day)), "Expense", "Meals & Entertainment", "Food", payees[2], descs[2], 74.60, base, 1.0, "Credit Card", True, "Operating"),
        (today.replace(day=min(7, today.day)), "Expense", "Rent Expense", "Rent", payees[3], descs[3], 1800.00, base, 1.0, "Bank Transfer", True, "Operating"),
        (today - timedelta(days=35), "Income", "Sales Revenue", "Client Payment", payees[4], descs[4], 3700.00, base, 1.0, "ACH", True, "Operating"),
        (today - timedelta(days=42), "Expense", "Professional Fees", "Professional Services", payees[5], descs[5], 350.00, base, 1.0, "Bank Transfer", True, "Operating"),
    ]
    return pd.DataFrame([
        {
            "transaction_id": str(uuid.uuid4())[:8].upper(),
            "user_id": active_user["user_id"],
            "user_name": active_user["display_name"],
            "date": r[0],
            "type": r[1],
            "account": r[2],
            "category": r[3],
            "payee": r[4],
            "description": r[5],
            "amount": r[6],
            "currency": r[7],
            "exchange_rate": r[8],
            "base_amount": r[6] * r[8],
            "transaction_nature": r[11],
            "payment_method": r[9],
            "status": "Reviewed",
            "tax_related": r[10],
            "attachment_ref": "",
            "notes": "Demo data" if lang == "en" else ("示範資料" if lang == "zh-TW" else "示范数据"),
            "created_at": now_str(),
            "updated_at": now_str(),
        }
        for r in base_rows
    ], columns=TRANSACTION_COLUMNS)


def filter_by_period(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    if df.empty:
        return df
    c1, c2, c3 = st.columns([1.1, 1, 1])
    options = ["all_time", "current_month", "last_90_days", "year_to_date", "custom_period"]
    with c1:
        selected = st.selectbox(t("period_filter", lang), options, format_func=lambda x: t(x, lang))
    default_start = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
    default_end = date.today().strftime("%Y-%m-%d")
    with c2:
        start_text = st.text_input(t("start_date", lang), value=default_start, help=t("date_hint", lang))
    with c3:
        end_text = st.text_input(t("end_date", lang), value=default_end, help=t("date_hint", lang))
    today = date.today()
    if selected == "all_time":
        return df
    if selected == "current_month":
        start, end = today.replace(day=1), today
    elif selected == "last_90_days":
        start, end = today - timedelta(days=90), today
    elif selected == "year_to_date":
        start, end = today.replace(month=1, day=1), today
    else:
        start = parse_date_text(start_text)
        end = parse_date_text(end_text)
        if not start or not end:
            st.warning(t("validation_date", lang))
            return df
    return df[(df["date"] >= start) & (df["date"] <= end)]




def clear_ai_capture_state(remove_temp: bool = True) -> None:
    """Clear transient image and Gemini extraction state after a transaction is saved or discarded."""
    if remove_temp:
        path = st.session_state.get("ai_temp_image_path")
        if path:
            try:
                Path(path).unlink(missing_ok=True)
            except Exception:
                pass
    st.session_state.ai_capture_suggestion = None
    st.session_state.ai_capture_source = None
    st.session_state.ai_temp_image_path = None
    st.session_state.capture_widget_nonce = str(uuid.uuid4())[:8]


def save_uploaded_image_to_temp(uploaded_file, active_user: pd.Series, source_kind: str) -> Optional[Path]:
    if uploaded_file is None:
        return None
    suffix = Path(getattr(uploaded_file, "name", "capture.jpg")).suffix or ".jpg"
    safe_user_id = re.sub(r"[^A-Za-z0-9_-]", "_", str(active_user.get("user_id", "user")))
    file_path = TEMP_DIR / f"{safe_user_id}_{source_kind}_{str(uuid.uuid4())[:10]}{suffix}"
    file_path.write_bytes(uploaded_file.getvalue())
    st.session_state.ai_temp_image_path = str(file_path)
    return file_path


def extract_json_object(text_value: str) -> Dict[str, object]:
    if not text_value:
        return {}
    cleaned = text_value.strip()
    cleaned = cleaned.replace("```json", "```").replace("```JSON", "```")
    if "```" in cleaned:
        parts = [p.strip() for p in cleaned.split("```") if p.strip()]
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                cleaned = part
                break
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        return json.loads(cleaned)
    except Exception:
        return {}


def sanitize_option(value: object, allowed: List[str], default: str) -> str:
    raw = str(value or "").strip()
    for item in allowed:
        if raw == item or raw.lower() == item.lower():
            return item
    # Try labels across languages.
    for mapping in [TYPE_LABELS, CATEGORY_LABELS, ACCOUNT_LABELS, TRANSACTION_NATURE_LABELS, PAYMENT_METHOD_LABELS, STATUS_LABELS]:
        for key, labels in mapping.items():
            if key in allowed and raw in labels.values():
                return key
    return default


def make_candidate_list(raw_values: object, allowed: List[str], default: str) -> List[str]:
    values: List[object]
    if isinstance(raw_values, list):
        values = raw_values
    elif raw_values is None or raw_values == "":
        values = []
    else:
        values = [raw_values]
    cleaned: List[str] = []
    for value in values:
        candidate = sanitize_option(value, allowed, default)
        if candidate not in cleaned:
            cleaned.append(candidate)
    if default not in cleaned:
        cleaned.insert(0, default)
    return cleaned[:4]


def normalize_ai_suggestion(raw: Dict[str, object], active_user: pd.Series, source_kind: str) -> Dict[str, object]:
    default_type = normalize_type(str(raw.get("type", "Expense")))
    type_candidates = make_candidate_list(raw.get("type_candidates", raw.get("type_options", [default_type])), ["Income", "Expense"], default_type)
    tx_type = type_candidates[0]
    allowed_categories = TYPE_TO_CATEGORIES.get(tx_type, TYPE_TO_CATEGORIES["Expense"])
    default_category = normalize_category(str(raw.get("category", "Other")))
    if default_category not in allowed_categories:
        default_category = "Client Payment" if tx_type == "Income" else "Other"
    category_candidates = make_candidate_list(raw.get("category_candidates", raw.get("category_options", [default_category])), allowed_categories, default_category)
    allowed_accounts = TYPE_TO_ACCOUNTS.get(tx_type, TYPE_TO_ACCOUNTS["Expense"])
    default_account = sanitize_option(raw.get("account", "Service Revenue" if tx_type == "Income" else account_from_category(default_category)), allowed_accounts, allowed_accounts[0])
    account_candidates = make_candidate_list(raw.get("account_candidates", raw.get("account_options", [default_account])), allowed_accounts, default_account)
    default_nature = normalize_nature(str(raw.get("transaction_nature", "Operating")))
    nature_candidates = make_candidate_list(raw.get("transaction_nature_candidates", raw.get("nature_options", [default_nature])), TRANSACTION_NATURES, default_nature)
    default_payment = normalize_payment(str(raw.get("payment_method", "Other")))
    payment_candidates = make_candidate_list(raw.get("payment_method_candidates", raw.get("payment_options", [default_payment])), PAYMENT_METHODS, default_payment)
    raw_date = parse_date_text(str(raw.get("date", ""))) or date.today()
    amount = pd.to_numeric(raw.get("amount", 0), errors="coerce")
    amount = float(amount) if pd.notna(amount) else 0.0
    currency = sanitize_option(raw.get("currency", active_user.get("base_currency", "USD")), CURRENCIES, str(active_user.get("base_currency", "USD")))
    confidence = raw.get("confidence", raw.get("overall_confidence", "medium"))
    return {
        "source_kind": source_kind,
        "date": raw_date.strftime("%Y-%m-%d"),
        "type_candidates": type_candidates,
        "category_candidates": category_candidates,
        "account_candidates": account_candidates,
        "transaction_nature_candidates": nature_candidates,
        "payment_method_candidates": payment_candidates,
        "payee": str(raw.get("payee", raw.get("merchant", raw.get("payer", ""))) or "").strip(),
        "description": str(raw.get("description", raw.get("memo", raw.get("summary", ""))) or "").strip(),
        "amount": abs(amount),
        "currency": currency,
        "exchange_rate": float(pd.to_numeric(raw.get("exchange_rate", 1), errors="coerce") or 1),
        "tax_related": bool(str(raw.get("tax_related", False)).lower() in ["true", "1", "yes", "是"]),
        "attachment_ref": str(raw.get("receipt_number", raw.get("reference", "")) or "").strip(),
        "notes": str(raw.get("notes", raw.get("reasoning", "")) or "").strip(),
        "confidence": str(confidence),
        "raw": raw,
    }


def gemini_extract_transaction(image_path: Path, api_key: str, active_user: pd.Series, source_kind: str, lang: str) -> Dict[str, object]:
    if not api_key:
        raise ValueError("missing api key")
    try:
        import google.generativeai as genai
        from PIL import Image
    except Exception as exc:
        raise RuntimeError("Missing google-generativeai or Pillow dependency") from exc
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    allowed = {
        "types": ["Income", "Expense"],
        "income_accounts": TYPE_TO_ACCOUNTS["Income"],
        "expense_accounts": TYPE_TO_ACCOUNTS["Expense"],
        "income_categories": TYPE_TO_CATEGORIES["Income"],
        "expense_categories": TYPE_TO_CATEGORIES["Expense"],
        "transaction_natures": TRANSACTION_NATURES,
        "payment_methods": PAYMENT_METHODS,
        "currencies": CURRENCIES,
    }
    lang_instruction = {
        "zh-TW": "Use Traditional Chinese only in notes or reasoning fields.",
        "zh-CN": "Use Simplified Chinese only in notes or reasoning fields.",
        "en": "Use English only in notes or reasoning fields.",
    }.get(lang, "Use English only in notes or reasoning fields.")
    prompt = f"""
You are an accounting extraction engine for a QuickBooks/Xero-style bookkeeping app.
Analyze this {source_kind} image and return ONLY one valid JSON object. No markdown.

{lang_instruction}

Allowed values:
{json.dumps(allowed, ensure_ascii=False)}

Rules:
1. Decide whether the image is Income or Expense. If uncertain, include multiple values in type_candidates ordered by confidence.
2. Extract date, merchant/payee/payer, amount, currency, payment method, receipt/reference number, and a short description.
3. Select account, category, and transaction_nature using ONLY allowed values.
4. If there are multiple plausible accounting treatments, include candidate arrays: type_candidates, account_candidates, category_candidates, transaction_nature_candidates, payment_method_candidates.
5. If the image is unclear, still return best estimates with confidence = low.

JSON schema:
{{
  "date": "YYYY-MM-DD",
  "type": "Income or Expense",
  "type_candidates": ["Expense", "Income"],
  "account": "allowed account",
  "account_candidates": ["allowed account"],
  "category": "allowed category",
  "category_candidates": ["allowed category"],
  "payee": "merchant, vendor, customer, or payer",
  "description": "short transaction description",
  "amount": 0.00,
  "currency": "USD",
  "exchange_rate": 1,
  "transaction_nature": "Operating",
  "transaction_nature_candidates": ["Operating"],
  "payment_method": "Credit Card",
  "payment_method_candidates": ["Credit Card", "Other"],
  "tax_related": false,
  "receipt_number": "",
  "confidence": "high, medium, or low",
  "notes": "brief extraction reason"
}}
"""
    image = Image.open(image_path)
    response = model.generate_content([prompt, image])
    raw = extract_json_object(getattr(response, "text", ""))
    if not raw:
        raise ValueError("No valid JSON returned by Gemini")
    return normalize_ai_suggestion(raw, active_user, source_kind)


def render_ai_capture_review(active_user: pd.Series, lang: str, source_kind: str) -> None:
    suggestion = st.session_state.get("ai_capture_suggestion")
    if not suggestion:
        return
    st.success(t("ai_suggestion_ready", lang))
    if any(len(suggestion.get(key, [])) > 1 for key in ["type_candidates", "account_candidates", "category_candidates", "transaction_nature_candidates", "payment_method_candidates"]):
        st.info(t("ai_multiple_options", lang))
    with st.expander(t("raw_ai_json", lang), expanded=False):
        st.json(suggestion.get("raw", {}))
    with st.form(f"ai_confirm_form_{source_kind}"):
        c1, c2, c3 = st.columns(3)
        with c1:
            date_text = st.text_input(t("transaction_date", lang), value=suggestion.get("date", date.today().strftime("%Y-%m-%d")), help=t("date_hint", lang), key=f"ai_date_{source_kind}")
            type_options_raw = make_candidate_list(suggestion.get("type_candidates"), ["Income", "Expense"], suggestion.get("type_candidates", ["Expense"])[0])
            type_display = st.selectbox(t("type", lang), [label(x, TYPE_LABELS, lang) for x in type_options_raw], key=f"ai_type_{source_kind}")
            tx_type = reverse_label(type_display, TYPE_LABELS, lang)
            nature_options_raw = make_candidate_list(suggestion.get("transaction_nature_candidates"), TRANSACTION_NATURES, "Operating")
            nature_display = st.selectbox(t("transaction_nature", lang), [label(x, TRANSACTION_NATURE_LABELS, lang) for x in nature_options_raw], key=f"ai_nature_{source_kind}")
            transaction_nature = reverse_label(nature_display, TRANSACTION_NATURE_LABELS, lang)
        with c2:
            allowed_accounts = TYPE_TO_ACCOUNTS[tx_type]
            default_account = suggestion.get("account_candidates", allowed_accounts)[0]
            account_options_raw = [x for x in make_candidate_list(suggestion.get("account_candidates"), allowed_accounts, default_account if default_account in allowed_accounts else allowed_accounts[0]) if x in allowed_accounts]
            account_display = st.selectbox(t("account", lang), [label(x, ACCOUNT_LABELS, lang) for x in account_options_raw], key=f"ai_account_{source_kind}")
            account = reverse_label(account_display, ACCOUNT_LABELS, lang)
            allowed_categories = TYPE_TO_CATEGORIES[tx_type]
            default_category = suggestion.get("category_candidates", allowed_categories)[0]
            category_options_raw = [x for x in make_candidate_list(suggestion.get("category_candidates"), allowed_categories, default_category if default_category in allowed_categories else allowed_categories[-1]) if x in allowed_categories]
            category_display = st.selectbox(t("category", lang), [label(x, CATEGORY_LABELS, lang) for x in category_options_raw], key=f"ai_category_{source_kind}")
            category = reverse_label(category_display, CATEGORY_LABELS, lang)
            payment_options_raw = make_candidate_list(suggestion.get("payment_method_candidates"), PAYMENT_METHODS, "Other")
            payment_display = st.selectbox(t("payment_method", lang), [label(x, PAYMENT_METHOD_LABELS, lang) for x in payment_options_raw], key=f"ai_payment_{source_kind}")
            payment_method = reverse_label(payment_display, PAYMENT_METHOD_LABELS, lang)
        with c3:
            amount = st.number_input(t("amount", lang), min_value=0.0, value=float(suggestion.get("amount", 0.0) or 0.0), step=0.01, format="%.2f", key=f"ai_amount_{source_kind}")
            currency = st.selectbox(t("transaction_currency", lang), CURRENCIES, index=CURRENCIES.index(suggestion.get("currency", active_user["base_currency"])) if suggestion.get("currency", active_user["base_currency"]) in CURRENCIES else 0, key=f"ai_currency_{source_kind}")
            exchange_rate = st.number_input(t("exchange_rate", lang), min_value=0.000001, value=float(suggestion.get("exchange_rate", 1.0) or 1.0), step=0.01, format="%.6f", key=f"ai_rate_{source_kind}")
            st.text_input(t("base_amount", lang), value=format_money(amount * exchange_rate, str(active_user["base_currency"])), disabled=True, key=f"ai_base_amount_{source_kind}")
        c4, c5 = st.columns(2)
        with c4:
            payee = st.text_input(t("payee", lang), value=suggestion.get("payee", ""), key=f"ai_payee_{source_kind}")
            description = st.text_input(t("description", lang), value=suggestion.get("description", ""), key=f"ai_description_{source_kind}")
            attachment_ref = st.text_input(t("attachment_ref", lang), value=suggestion.get("attachment_ref", ""), key=f"ai_attachment_{source_kind}")
        with c5:
            status = "Needs Review"
            tax_related = st.checkbox(t("tax_related", lang), value=bool(suggestion.get("tax_related", False)), key=f"ai_tax_{source_kind}")
            notes_default = f"{t('capture_source', lang)}: {t(source_kind, lang)} | {t('ai_confidence', lang)}: {suggestion.get('confidence', '-')}. {suggestion.get('notes', '')}".strip()
            notes = st.text_area(t("notes", lang), value=notes_default, height=82, key=f"ai_notes_{source_kind}")
        c6, c7 = st.columns(2)
        with c6:
            confirm = st.form_submit_button(t("confirm_and_save", lang), type="primary", use_container_width=True)
        with c7:
            discard = st.form_submit_button(t("discard_capture", lang), use_container_width=True)
        if discard:
            clear_ai_capture_state(remove_temp=True)
            st.success(t("temp_image_cleared", lang))
            st.rerun()
        if confirm:
            tx_date = parse_date_text(date_text)
            if not tx_date:
                st.warning(t("validation_date", lang))
            elif not description.strip():
                st.warning(t("validation_description", lang))
            elif amount <= 0:
                st.warning(t("validation_amount", lang))
            else:
                row = {
                    "transaction_id": str(uuid.uuid4())[:8].upper(),
                    "user_id": active_user["user_id"],
                    "user_name": active_user["display_name"],
                    "date": tx_date,
                    "type": tx_type,
                    "account": account,
                    "category": category,
                    "payee": payee.strip() or "-",
                    "description": description.strip(),
                    "amount": float(amount),
                    "currency": currency,
                    "exchange_rate": float(exchange_rate),
                    "base_amount": float(amount) * float(exchange_rate),
                    "transaction_nature": transaction_nature,
                    "payment_method": payment_method,
                    "status": status,
                    "tax_related": bool(tax_related),
                    "attachment_ref": attachment_ref.strip(),
                    "notes": notes.strip(),
                    "created_at": now_str(),
                    "updated_at": now_str(),
                }
                if validate_duplicate(read_transactions(), row):
                    st.warning(t("duplicate_warning", lang))
                    st.stop()
                append_transaction(row)
                log_audit("AI_CAPTURE_TRANSACTION", str(row["transaction_id"]), str(row["user_id"]), str(row["user_name"]), f"Saved from {source_kind}; temporary image cleared")
                clear_ai_capture_state(remove_temp=True)
                st.success(t("transaction_saved", lang))
                st.info(t("temp_image_cleared", lang))
                st.rerun()


def render_ai_capture_tab(active_user: pd.Series, lang: str, source_kind: str) -> None:
    st.caption(t(f"{source_kind}_help", lang))
    api_key = st.session_state.get("gemini_api_key", "")
    if not api_key:
        st.warning(t("gemini_api_missing", lang))
    uploaded = None
    if source_kind == "receipt_photo":
        camera_image = st.camera_input(t("take_receipt_photo", lang), key=f"camera_{st.session_state.capture_widget_nonce}")
        uploaded_receipt = st.file_uploader(t("or_upload_receipt", lang), type=["png", "jpg", "jpeg", "webp"], key=f"receipt_upload_{st.session_state.capture_widget_nonce}")
        uploaded = camera_image or uploaded_receipt
    else:
        uploaded = st.file_uploader(t("upload_screenshot", lang), type=["png", "jpg", "jpeg", "webp"], key=f"screenshot_upload_{st.session_state.capture_widget_nonce}")
    if uploaded is not None:
        st.image(uploaded, caption=t("image_preview", lang), use_container_width=True)
        if st.button(t("analyze_with_gemini", lang), type="primary", disabled=not bool(api_key), key=f"analyze_{source_kind}"):
            try:
                image_path = save_uploaded_image_to_temp(uploaded, active_user, source_kind)
                with st.spinner(t("ai_processing", lang)):
                    suggestion = gemini_extract_transaction(image_path, api_key, active_user, source_kind, lang)
                st.session_state.ai_capture_suggestion = suggestion
                st.session_state.ai_capture_source = source_kind
                st.rerun()
            except Exception as exc:
                st.error(f"{t('ai_extraction_failed', lang)}: {exc}")
    if st.session_state.get("ai_capture_source") == source_kind and st.session_state.get("ai_capture_suggestion"):
        render_ai_capture_review(active_user, lang, source_kind)

def render_hero(lang: str) -> None:
    st.markdown(f"""
    <div class="lp-hero">
        <h1>📘 {t('app_name', lang)}</h1>
        <p>{t('tagline', lang)}</p>
    </div>
    """, unsafe_allow_html=True)


def render_account_workspace(users: pd.DataFrame, lang: str) -> pd.Series:
    st.markdown(f"<div class='lp-profile-box'><h3>{t('account_workspace', lang)}</h3><p class='lp-note'>{t('commercial_logic_text', lang)}</p></div>", unsafe_allow_html=True)
    display_options = [f"{row.display_name} · {row.base_currency} · {label(row.entity_type, ENTITY_TYPE_LABELS, lang)}" for row in users.itertuples()]
    ids = users["user_id"].tolist()
    current_idx = ids.index(st.session_state.selected_user_id) if st.session_state.selected_user_id in ids else 0
    c1, c2 = st.columns([1.1, 1])
    with c1:
        selected_display = st.selectbox(t("select_user_account", lang), display_options, index=current_idx)
        new_selected_user_id = ids[display_options.index(selected_display)]
        if st.session_state.selected_user_id != new_selected_user_id:
            st.session_state.selected_user_id = new_selected_user_id
            # Defer clearing the Gemini API key until the next rerun, before
            # the sidebar password input widget with key="gemini_api_key" is
            # instantiated.  This avoids StreamlitAPIException.
            st.session_state.pending_clear_gemini_api_key = True
            st.session_state.api_reset_notice = True
            clear_ai_capture_state(remove_temp=True)
            st.rerun()
    active_user = get_active_user(users)
    with c2:
        st.text_input(t("active_account", lang), value=f"{active_user['display_name']} · {active_user['base_currency']}", disabled=True)

    with st.expander(t("account_profile", lang), expanded=False):
        with st.form("update_account_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input(t("display_name", lang), value=str(active_user["display_name"]))
                entity_display = st.selectbox(t("entity_type", lang), [label(x, ENTITY_TYPE_LABELS, lang) for x in ENTITY_TYPES], index=ENTITY_TYPES.index(str(active_user["entity_type"])) if str(active_user["entity_type"]) in ENTITY_TYPES else 0)
                entity_type = reverse_label(entity_display, ENTITY_TYPE_LABELS, lang)
                email = st.text_input(t("email", lang), value=str(active_user["email"]) if pd.notna(active_user["email"]) else "")
            with c2:
                country = st.text_input(t("country_region", lang), value=str(active_user["country_region"]) if pd.notna(active_user["country_region"]) else "")
                tax_id = st.text_input(t("tax_id", lang), value=str(active_user["tax_id"]) if pd.notna(active_user["tax_id"]) else "")
                industry = st.text_input(t("industry", lang), value=str(active_user["industry"]) if pd.notna(active_user["industry"]) else "")
            with c3:
                base_currency = st.selectbox(t("base_currency", lang), CURRENCIES, index=CURRENCIES.index(str(active_user["base_currency"])) if str(active_user["base_currency"]) in CURRENCIES else 0)
                opening_balance = st.number_input(t("opening_balance", lang), value=float(active_user["opening_balance"]), step=100.0, format="%.2f")
                account_notes = st.text_area(t("account_notes", lang), value=str(active_user["notes"]) if pd.notna(active_user["notes"]) else "", height=68)
            if st.form_submit_button(t("update_account", lang), type="primary", use_container_width=True):
                cleaned_name = name.strip()
                if not cleaned_name:
                    st.warning(t("validation_user", lang))
                elif user_name_exists(users, cleaned_name, exclude_user_id=str(active_user["user_id"])):
                    st.warning(t("duplicate_user_warning", lang))
                else:
                    users.loc[users["user_id"] == active_user["user_id"], ["display_name", "entity_type", "email", "country_region", "tax_id", "industry", "base_currency", "opening_balance", "notes", "updated_at"]] = [cleaned_name, entity_type, email, country, tax_id, industry, base_currency, opening_balance, account_notes, now_str()]
                    save_users(users)
                    tx = read_transactions()
                    tx.loc[tx["user_id"] == active_user["user_id"], "user_name"] = cleaned_name
                    save_transactions(tx)
                    log_audit("UPDATE_USER", "N/A", str(active_user["user_id"]), cleaned_name, "Updated user account profile")
                    st.success(t("account_saved", lang))
                    st.rerun()

    with st.expander(t("create_new_account", lang), expanded=False):
        with st.form("create_user_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                new_name = st.text_input(t("display_name", lang), placeholder=("Client A" if lang == "en" else ("客戶 A" if lang == "zh-TW" else "客户 A")))
                new_entity_display = st.selectbox(t("entity_type", lang), [label(x, ENTITY_TYPE_LABELS, lang) for x in ENTITY_TYPES], key="new_entity_type")
                new_entity_type = reverse_label(new_entity_display, ENTITY_TYPE_LABELS, lang)
                new_email = st.text_input(t("email", lang), key="new_email")
            with c2:
                new_country = st.text_input(t("country_region", lang), value="United States", key="new_country")
                new_tax_id = st.text_input(t("tax_id", lang), key="new_tax_id")
                new_industry = st.text_input(t("industry", lang), value="Small Business", key="new_industry")
            with c3:
                new_base = st.selectbox(t("base_currency", lang), CURRENCIES, key="new_base")
                new_opening = st.number_input(t("opening_balance", lang), value=0.0, step=100.0, format="%.2f", key="new_opening")
                new_notes = st.text_area(t("account_notes", lang), height=68, key="new_notes")
            if st.form_submit_button(t("save_new_account", lang), type="primary", use_container_width=True):
                cleaned_new_name = new_name.strip()
                if not cleaned_new_name:
                    st.warning(t("validation_user", lang))
                elif user_name_exists(users, cleaned_new_name):
                    st.warning(t("duplicate_user_warning", lang))
                else:
                    new_id = f"USER-{str(uuid.uuid4())[:8].upper()}"
                    row = pd.DataFrame([{
                        "user_id": new_id,
                        "display_name": cleaned_new_name,
                        "entity_type": new_entity_type,
                        "email": new_email.strip(),
                        "country_region": new_country.strip(),
                        "tax_id": new_tax_id.strip(),
                        "industry": new_industry.strip(),
                        "base_currency": new_base,
                        "opening_balance": new_opening,
                        "notes": new_notes.strip(),
                        "created_at": now_str(),
                        "updated_at": now_str(),
                    }])
                    save_users(pd.concat([users, row], ignore_index=True))
                    st.session_state.selected_user_id = new_id
                    log_audit("CREATE_USER", "N/A", new_id, cleaned_new_name, "Created new user account")
                    st.success(t("account_created", lang))
                    st.rerun()
    return get_active_user(read_users())


def render_kpis(df: pd.DataFrame, lang: str, currency: str, opening_balance: float) -> None:
    m = metrics(df, opening_balance)
    top_expense = label(str(m["top_expense"]), CATEGORY_LABELS, lang) if m["top_expense"] != "-" else "-"
    cards = [
        (t("total_income", lang), format_money(float(m["income"]), currency)),
        (t("total_expense", lang), format_money(float(m["expense"]), currency)),
        (t("net_profit", lang), format_money(float(m["net"]), currency)),
        (t("cash_position", lang), format_money(float(m["cash"]), currency)),
        (t("review_needed", lang), f"{int(m['review_needed']):,}"),
        (t("top_expense", lang), top_expense),
    ]
    cols = st.columns(3)
    for idx, (title, value) in enumerate(cards):
        with cols[idx % 3]:
            st.markdown(f"<div class='lp-card'><div class='lp-mini-title'>{title}</div><div class='lp-value'>{value}</div></div>", unsafe_allow_html=True)


def render_dashboard(df: pd.DataFrame, lang: str, active_user: pd.Series) -> None:
    currency = str(active_user["base_currency"])
    opening_balance = float(active_user["opening_balance"])
    if df.empty:
        st.info(t("no_data", lang))
        return
    render_kpis(df, lang, currency, opening_balance)
    st.divider()
    monthly = monthly_summary(df)
    c1, c2 = st.columns([1.35, 1])
    with c1:
        chart = monthly.rename(columns={"month": t("month", lang), "Income": t("income", lang), "Expense": t("expense", lang), "Net": t("net_cash_flow", lang)})
        fig = px.bar(chart, x=t("month", lang), y=[t("income", lang), t("expense", lang)], barmode="group", title=t("income_vs_expense", lang))
        fig.update_layout(legend_title_text="", height=420)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        exp_df = df[df["type"] == "Expense"].groupby("category", as_index=False)["base_amount"].sum()
        if not exp_df.empty:
            exp_df["category_label"] = exp_df["category"].apply(lambda x: label(x, CATEGORY_LABELS, lang))
            fig = px.pie(exp_df, values="base_amount", names="category_label", title=t("expense_distribution", lang), hole=0.42)
            fig.update_layout(height=420)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.subheader(t("management_insight", lang))
    m = metrics(df, opening_balance)
    if int(m["count"]) == 0:
        st.info(t("insight_no_data", lang))
    elif float(m["net"]) >= 0:
        st.success(t("insight_positive", lang))
    else:
        st.warning(t("insight_negative", lang))
    st.subheader(t("recent_transactions", lang))
    st.dataframe(display_dataframe(df.sort_values("date", ascending=False).head(10), lang), use_container_width=True, hide_index=True)


def render_manual_entry_form(lang: str, active_user: pd.Series) -> None:
    st.caption(t("manual_tab_help", lang))
    with st.form("transaction_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            date_text = st.text_input(t("transaction_date", lang), value=date.today().strftime("%Y-%m-%d"), help=t("date_hint", lang))
            type_display = st.radio(t("type", lang), [label("Expense", TYPE_LABELS, lang), label("Income", TYPE_LABELS, lang)], horizontal=True)
            tx_type = reverse_label(type_display, TYPE_LABELS, lang)
            nature_display = st.selectbox(t("transaction_nature", lang), [label(x, TRANSACTION_NATURE_LABELS, lang) for x in TRANSACTION_NATURES])
            transaction_nature = reverse_label(nature_display, TRANSACTION_NATURE_LABELS, lang)
        with c2:
            account_options_raw = TYPE_TO_ACCOUNTS[tx_type]
            account_display = st.selectbox(t("account", lang), [label(x, ACCOUNT_LABELS, lang) for x in account_options_raw])
            account = reverse_label(account_display, ACCOUNT_LABELS, lang)
            category_options_raw = TYPE_TO_CATEGORIES[tx_type]
            category_display = st.selectbox(t("category", lang), [label(x, CATEGORY_LABELS, lang) for x in category_options_raw])
            category = reverse_label(category_display, CATEGORY_LABELS, lang)
            payment_display = st.selectbox(t("payment_method", lang), [label(x, PAYMENT_METHOD_LABELS, lang) for x in PAYMENT_METHODS])
            payment_method = reverse_label(payment_display, PAYMENT_METHOD_LABELS, lang)
        with c3:
            amount = st.number_input(t("amount", lang), min_value=0.0, value=0.0, step=0.01, format="%.2f")
            base_currency = str(active_user["base_currency"])
            currency = st.selectbox(t("transaction_currency", lang), CURRENCIES, index=CURRENCIES.index(base_currency) if base_currency in CURRENCIES else 0)
            exchange_rate = st.number_input(t("exchange_rate", lang), min_value=0.000001, value=1.0, step=0.01, format="%.6f")
            st.text_input(t("base_amount", lang), value=format_money(amount * exchange_rate, base_currency), disabled=True)
        c4, c5 = st.columns([1, 1])
        with c4:
            payee = st.text_input(t("payee", lang), placeholder=t("payee_placeholder", lang))
            description = st.text_input(t("description", lang), placeholder=t("description_placeholder", lang))
            attachment_ref = st.text_input(t("attachment_ref", lang))
        with c5:
            status_display = st.selectbox(t("status", lang), [label(x, STATUS_LABELS, lang) for x in STATUSES])
            status = reverse_label(status_display, STATUS_LABELS, lang)
            tax_related = st.checkbox(t("tax_related", lang), value=False)
            notes = st.text_area(t("notes", lang), placeholder=t("notes_placeholder", lang), height=70)
        submitted = st.form_submit_button(t("save_transaction", lang), type="primary", use_container_width=True)
        if submitted:
            tx_date = parse_date_text(date_text)
            if not tx_date:
                st.warning(t("validation_date", lang))
            elif not description.strip():
                st.warning(t("validation_description", lang))
            elif amount <= 0:
                st.warning(t("validation_amount", lang))
            else:
                row = {
                    "transaction_id": str(uuid.uuid4())[:8].upper(),
                    "user_id": active_user["user_id"],
                    "user_name": active_user["display_name"],
                    "date": tx_date,
                    "type": tx_type,
                    "account": account,
                    "category": category,
                    "payee": payee.strip() or "-",
                    "description": description.strip(),
                    "amount": float(amount),
                    "currency": currency,
                    "exchange_rate": float(exchange_rate),
                    "base_amount": float(amount) * float(exchange_rate),
                    "transaction_nature": transaction_nature,
                    "payment_method": payment_method,
                    "status": status,
                    "tax_related": bool(tax_related),
                    "attachment_ref": attachment_ref.strip(),
                    "notes": notes.strip(),
                    "created_at": now_str(),
                    "updated_at": now_str(),
                }
                if validate_duplicate(read_transactions(), row):
                    st.warning(t("duplicate_warning", lang))
                    st.stop()
                append_transaction(row)
                st.success(t("transaction_saved", lang))
                st.rerun()


def render_transaction_ledger(df: pd.DataFrame, lang: str, active_user: pd.Series) -> None:
    st.subheader(t("transaction_ledger", lang))
    c1, c2, c3 = st.columns([1.6, 1, 1])
    with c1:
        search = st.text_input(t("search", lang), placeholder=t("search_placeholder", lang))
    with c2:
        selected_type = st.selectbox(t("filter_type", lang), [t("all", lang), label("Income", TYPE_LABELS, lang), label("Expense", TYPE_LABELS, lang)], key="ledger_type_filter")
    with c3:
        currency_filter = st.selectbox(t("filter_currency", lang), [t("all", lang)] + CURRENCIES, key="ledger_currency_filter")
    ledger = df.copy()
    if selected_type != t("all", lang):
        ledger = ledger[ledger["type"] == reverse_label(selected_type, TYPE_LABELS, lang)]
    if currency_filter != t("all", lang):
        ledger = ledger[ledger["currency"] == currency_filter]
    if search and not ledger.empty:
        mask = ledger[["payee", "description", "category", "account", "currency", "transaction_nature"]].astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
        ledger = ledger[mask]
    st.dataframe(display_dataframe(ledger.sort_values("date", ascending=False), lang), use_container_width=True, hide_index=True)
    if not ledger.empty:
        with st.expander(t("delete_transaction", lang), expanded=False):
            tx_id = st.selectbox(t("select_transaction", lang), ledger["transaction_id"].tolist(), key="ledger_delete_id")
            if st.button(t("delete_selected", lang), type="secondary"):
                deleted = delete_transaction(tx_id, str(active_user["user_id"]), str(active_user["display_name"]))
                if deleted:
                    st.success(t("deleted", lang))
                else:
                    st.warning(t("transaction_not_found", lang))
                st.rerun()


def render_transactions(df: pd.DataFrame, lang: str, active_user: pd.Series) -> None:
    st.subheader(t("capture_center", lang))
    st.caption(t("capture_center_text", lang))
    manual_tab, receipt_tab, screenshot_tab, ledger_tab = st.tabs([
        t("manual_entry", lang),
        t("receipt_photo", lang),
        t("income_expense_screenshot", lang),
        t("transaction_ledger", lang),
    ])
    with manual_tab:
        render_manual_entry_form(lang, active_user)
    with receipt_tab:
        render_ai_capture_tab(active_user, lang, "receipt_photo")
    with screenshot_tab:
        render_ai_capture_tab(active_user, lang, "income_expense_screenshot")
    with ledger_tab:
        render_transaction_ledger(df, lang, active_user)


def render_data_cleaning(df: pd.DataFrame, lang: str, active_user: pd.Series) -> None:
    st.subheader(t("data_cleaning", lang))
    st.caption(t("data_cleaning_text", lang))
    if df.empty:
        st.info(t("no_data", lang))
        return

    ledger = df.sort_values("date", ascending=False).copy()
    st.dataframe(display_dataframe(ledger, lang), use_container_width=True, hide_index=True)

    option_map = {}
    for row in ledger.itertuples():
        raw_date = pd.to_datetime(row.date, errors="coerce")
        date_label = raw_date.strftime("%Y-%m-%d") if pd.notna(raw_date) else "-"
        option = f"{row.transaction_id} · {date_label} · {row.description} · {row.currency} {float(row.amount):,.2f}"
        option_map[option] = str(row.transaction_id)

    selected_option = st.selectbox(t("select_transaction_to_clean", lang), list(option_map.keys()))
    selected_tx_id = option_map[selected_option]
    selected = ledger[ledger["transaction_id"].astype(str) == selected_tx_id].iloc[0]

    edit_tab, delete_tab = st.tabs([t("edit_transaction", lang), t("delete_transaction", lang)])
    with edit_tab:
        with st.form(f"edit_transaction_form_{selected_tx_id}"):
            current_type = str(selected.get("type", "Expense")) if str(selected.get("type", "Expense")) in ["Income", "Expense"] else "Expense"
            c1, c2, c3 = st.columns(3)
            with c1:
                selected_date = pd.to_datetime(selected.get("date", date.today()), errors="coerce")
                date_text = st.text_input(t("transaction_date", lang), value=(selected_date.strftime("%Y-%m-%d") if pd.notna(selected_date) else date.today().strftime("%Y-%m-%d")), help=t("date_hint", lang), key=f"edit_date_{selected_tx_id}")
                type_options = [label("Expense", TYPE_LABELS, lang), label("Income", TYPE_LABELS, lang)]
                type_display = st.radio(t("type", lang), type_options, index=type_options.index(label(current_type, TYPE_LABELS, lang)), horizontal=True, key=f"edit_type_{selected_tx_id}")
                tx_type = reverse_label(type_display, TYPE_LABELS, lang)
                nature_options = [label(x, TRANSACTION_NATURE_LABELS, lang) for x in TRANSACTION_NATURES]
                current_nature = str(selected.get("transaction_nature", "Operating")) if str(selected.get("transaction_nature", "Operating")) in TRANSACTION_NATURES else "Operating"
                nature_display = st.selectbox(t("transaction_nature", lang), nature_options, index=TRANSACTION_NATURES.index(current_nature), key=f"edit_nature_{selected_tx_id}")
                transaction_nature = reverse_label(nature_display, TRANSACTION_NATURE_LABELS, lang)
            with c2:
                account_options_raw = TYPE_TO_ACCOUNTS[tx_type]
                account_options = [label(x, ACCOUNT_LABELS, lang) for x in account_options_raw]
                current_account = str(selected.get("account", account_options_raw[0])) if str(selected.get("account", account_options_raw[0])) in account_options_raw else account_options_raw[0]
                account_display = st.selectbox(t("account", lang), account_options, index=account_options_raw.index(current_account), key=f"edit_account_{selected_tx_id}")
                account = reverse_label(account_display, ACCOUNT_LABELS, lang)
                category_options_raw = TYPE_TO_CATEGORIES[tx_type]
                category_options = [label(x, CATEGORY_LABELS, lang) for x in category_options_raw]
                current_category = str(selected.get("category", category_options_raw[-1])) if str(selected.get("category", category_options_raw[-1])) in category_options_raw else category_options_raw[-1]
                category_display = st.selectbox(t("category", lang), category_options, index=category_options_raw.index(current_category), key=f"edit_category_{selected_tx_id}")
                category = reverse_label(category_display, CATEGORY_LABELS, lang)
                payment_options = [label(x, PAYMENT_METHOD_LABELS, lang) for x in PAYMENT_METHODS]
                current_payment = str(selected.get("payment_method", "Other")) if str(selected.get("payment_method", "Other")) in PAYMENT_METHODS else "Other"
                payment_display = st.selectbox(t("payment_method", lang), payment_options, index=PAYMENT_METHODS.index(current_payment), key=f"edit_payment_{selected_tx_id}")
                payment_method = reverse_label(payment_display, PAYMENT_METHOD_LABELS, lang)
            with c3:
                amount = st.number_input(t("amount", lang), min_value=0.0, value=float(selected.get("amount", 0.0) or 0.0), step=0.01, format="%.2f", key=f"edit_amount_{selected_tx_id}")
                current_currency = str(selected.get("currency", active_user["base_currency"])) if str(selected.get("currency", active_user["base_currency"])) in CURRENCIES else str(active_user["base_currency"])
                currency = st.selectbox(t("transaction_currency", lang), CURRENCIES, index=CURRENCIES.index(current_currency) if current_currency in CURRENCIES else 0, key=f"edit_currency_{selected_tx_id}")
                exchange_rate = st.number_input(t("exchange_rate", lang), min_value=0.000001, value=float(selected.get("exchange_rate", 1.0) or 1.0), step=0.01, format="%.6f", key=f"edit_rate_{selected_tx_id}")
                st.text_input(t("base_amount", lang), value=format_money(amount * exchange_rate, str(active_user["base_currency"])), disabled=True, key=f"edit_base_amount_{selected_tx_id}")
            c4, c5 = st.columns([1, 1])
            with c4:
                payee = st.text_input(t("payee", lang), value=str(selected.get("payee", "") if pd.notna(selected.get("payee", "")) else ""), key=f"edit_payee_{selected_tx_id}")
                description = st.text_input(t("description", lang), value=str(selected.get("description", "") if pd.notna(selected.get("description", "")) else ""), key=f"edit_description_{selected_tx_id}")
                attachment_ref = st.text_input(t("attachment_ref", lang), value=str(selected.get("attachment_ref", "") if pd.notna(selected.get("attachment_ref", "")) else ""), key=f"edit_attachment_{selected_tx_id}")
            with c5:
                status_options = [label(x, STATUS_LABELS, lang) for x in STATUSES]
                current_status = str(selected.get("status", "Needs Review")) if str(selected.get("status", "Needs Review")) in STATUSES else "Needs Review"
                status_display = st.selectbox(t("status", lang), status_options, index=STATUSES.index(current_status), key=f"edit_status_{selected_tx_id}")
                status = reverse_label(status_display, STATUS_LABELS, lang)
                tax_related = st.checkbox(t("tax_related", lang), value=bool(selected.get("tax_related", False)), key=f"edit_tax_{selected_tx_id}")
                notes = st.text_area(t("notes", lang), value=str(selected.get("notes", "") if pd.notna(selected.get("notes", "")) else ""), height=70, key=f"edit_notes_{selected_tx_id}")

            if st.form_submit_button(t("save_transaction_changes", lang), type="primary", use_container_width=True):
                tx_date = parse_date_text(date_text)
                if not tx_date:
                    st.warning(t("validation_date", lang))
                elif not description.strip():
                    st.warning(t("validation_description", lang))
                elif amount <= 0:
                    st.warning(t("validation_amount", lang))
                else:
                    update_transaction(
                        selected_tx_id,
                        {
                            "date": tx_date,
                            "type": tx_type,
                            "account": account,
                            "category": category,
                            "payee": payee.strip() or "-",
                            "description": description.strip(),
                            "amount": float(amount),
                            "currency": currency,
                            "exchange_rate": float(exchange_rate),
                            "base_amount": float(amount) * float(exchange_rate),
                            "transaction_nature": transaction_nature,
                            "payment_method": payment_method,
                            "status": status,
                            "tax_related": bool(tax_related),
                            "attachment_ref": attachment_ref.strip(),
                            "notes": notes.strip(),
                        },
                        str(active_user["user_id"]),
                        str(active_user["display_name"]),
                    )
                    st.success(t("transaction_updated", lang))
                    st.rerun()

    with delete_tab:
        st.warning(t("delete_permanent_warning", lang))
        confirm_delete = st.checkbox(t("confirm_delete_transaction", lang), key=f"confirm_delete_{selected_tx_id}")
        if st.button(t("delete_selected", lang), disabled=not confirm_delete, use_container_width=True, key=f"clean_delete_{selected_tx_id}"):
            deleted = delete_transaction(selected_tx_id, str(active_user["user_id"]), str(active_user["display_name"]))
            if deleted:
                st.success(t("deleted", lang))
            else:
                st.warning(t("transaction_not_found", lang))
            st.rerun()

def render_reports(df: pd.DataFrame, lang: str, active_user: pd.Series, users: pd.DataFrame) -> None:
    currency = str(active_user["base_currency"])
    if df.empty:
        st.info(t("no_data", lang))
        return
    m = metrics(df, float(active_user["opening_balance"]))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(t("gross_income", lang), format_money(float(m["income"]), currency))
    with c2:
        st.metric(t("operating_expense", lang), format_money(float(m["expense"]), currency))
    with c3:
        st.metric(t("net_income", lang), format_money(float(m["net"]), currency), f"{float(m['profit_margin']):.1%}")
    st.subheader(t("pnl_report", lang))
    st.table(build_pnl(df, lang, currency))
    st.subheader(t("cash_flow_report", lang))
    cash_flow = monthly_summary(df).rename(columns={"month": t("month", lang), "Income": t("cash_inflow", lang), "Expense": t("cash_outflow", lang), "Net": t("net_cash_flow", lang)})
    st.dataframe(cash_flow, use_container_width=True, hide_index=True)
    st.subheader(t("category_breakdown", lang))
    category_df = df.groupby(["type", "category"], as_index=False)["base_amount"].sum()
    if not category_df.empty:
        category_df["type"] = category_df["type"].apply(lambda x: label(x, TYPE_LABELS, lang))
        category_df["category"] = category_df["category"].apply(lambda x: label(x, CATEGORY_LABELS, lang))
    st.dataframe(category_df.rename(columns={"type": t("type", lang), "category": t("category", lang), "base_amount": t("base_amount", lang)}), use_container_width=True, hide_index=True)
    st.subheader(t("close_readiness", lang))
    st.markdown(f"- {t('close_item_1', lang)}\n- {t('close_item_2', lang)}\n- {t('close_item_3', lang)}\n- {t('close_item_4', lang)}")
    c4, c5 = st.columns(2)
    safe_name = str(active_user["display_name"]).replace(" ", "_")
    with c4:
        csv_data = display_dataframe(df, lang).to_csv(index=False).encode("utf-8-sig")
        st.download_button(t("export_transactions", lang), csv_data, file_name=f"{safe_name}_transactions.csv", mime="text/csv", use_container_width=True)
    with c5:
        st.download_button(t("export_workbook", lang), make_excel_report(df, lang, currency, users), file_name=f"{safe_name}_financial_workbook.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)


def render_settings(df: pd.DataFrame, lang: str, active_user: pd.Series) -> None:
    st.subheader(t("commercial_logic", lang))
    st.info(t("commercial_logic_text", lang))
    st.divider()
    render_data_cleaning(df, lang, active_user)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(t("import_data", lang))
        st.caption(t("paste_help", lang))
        template = "Date,Type,Category,Description,Amount,Currency,Exchange Rate,Transaction Nature\n2026-01-01,Expense,Food,Lunch,12.50,USD,1,Operating\n"
        st.download_button(t("download_template", lang), template.encode("utf-8-sig"), file_name="import_template.csv", mime="text/csv")
        pasted = st.text_area(t("paste_csv", lang), placeholder=t("paste_placeholder", lang), height=170)
        if st.button(t("import_button", lang), type="primary", use_container_width=True):
            try:
                count = import_pasted_csv(pasted, active_user)
                st.success(f"{t('import_success', lang)}: {count}")
                st.rerun()
            except Exception:
                st.error(t("import_error", lang))
    with c2:
        st.subheader(t("data_location", lang))
        if google_sheets_enabled():
            st.success(t("cloud_connected", lang))
            st.code(f"Google Sheets: {google_spreadsheet_id()}")
        else:
            st.warning(t("cloud_not_connected", lang))
            st.code(str(DATA_DIR))
        if st.button(t("load_demo", lang), use_container_width=True):
            all_tx = read_transactions()
            all_tx = all_tx[all_tx["user_id"] != active_user["user_id"]]
            save_transactions(pd.concat([all_tx, sample_rows(active_user, lang)], ignore_index=True))
            log_audit("LOAD_DEMO", "MULTIPLE", str(active_user["user_id"]), str(active_user["display_name"]), "Loaded demo data")
            st.rerun()
        confirm = st.checkbox(t("confirm_clear", lang))
        if st.button(t("clear_active", lang), disabled=not confirm, use_container_width=True):
            all_tx = read_transactions()
            save_transactions(all_tx[all_tx["user_id"] != active_user["user_id"]])
            log_audit("CLEAR_ACTIVE", "MULTIPLE", str(active_user["user_id"]), str(active_user["display_name"]), "Cleared active account transactions")
            st.success(t("data_cleared", lang))
            st.rerun()
    st.divider()
    st.subheader(t("audit_log", lang))
    audit = read_audit_log()
    if not audit.empty:
        audit_display = audit.copy()
        audit_display = audit_display[audit_display.get("user_id", "") == active_user["user_id"]]
        if audit_display.empty:
            st.info(t("no_data", lang))
        else:
            audit_display["action"] = audit_display["action"].apply(lambda x: label(str(x), ACTION_LABELS, lang))
            audit_display = audit_display.rename(columns={"timestamp": t("created_at", lang), "action": t("type", lang), "transaction_id": t("transaction_id", lang), "user_id": t("user_id", lang), "user_name": t("user_name", lang), "details": t("notes", lang)})
            st.dataframe(audit_display.sort_values(t("created_at", lang), ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info(t("no_data", lang))


def main() -> None:
    init_session_state()
    lang = render_language_sidebar()
    ensure_files()
    users = read_users()
    render_hero(lang)
    active_user = render_account_workspace(users, lang)
    df = read_transactions()
    user_df = df[df["user_id"] == active_user["user_id"]] if not df.empty else df
    filtered_df = filter_by_period(user_df, lang)
    tab1, tab2, tab3, tab4 = st.tabs([t("dashboard", lang), t("transactions", lang), t("reports", lang), t("settings", lang)])
    with tab1:
        render_dashboard(filtered_df, lang, active_user)
    with tab2:
        render_transactions(user_df, lang, active_user)
    with tab3:
        render_reports(filtered_df, lang, active_user, users)
    with tab4:
        render_settings(user_df, lang, active_user)


if __name__ == "__main__":
    main()
