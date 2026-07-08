from __future__ import annotations

LANG_OPTIONS = ["zh-TW", "zh-CN", "en"]
LANG_NAMES = {
    "zh-TW": {"zh-TW": "繁體", "zh-CN": "簡體", "en": "英文"},
    "zh-CN": {"zh-TW": "繁体", "zh-CN": "简体", "en": "英文"},
    "en": {"zh-TW": "Traditional", "zh-CN": "Simplified", "en": "English"},
}

TEXT = {
    "page_title": {"zh-TW": "LedgerPro AI 商業帳務系統", "zh-CN": "LedgerPro AI 商业账务系统", "en": "LedgerPro AI Commercial Bookkeeping"},
    "app_name": {"zh-TW": "LedgerPro AI 商業帳務系統", "zh-CN": "LedgerPro AI 商业账务系统", "en": "LedgerPro AI Commercial Bookkeeping"},
    "tagline": {
        "zh-TW": "以 QuickBooks / Xero 類型的工作流重新設計：使用者帳戶、交易中心、多幣別、科目分類、審核狀態、報表與稽核紀錄。",
        "zh-CN": "以 QuickBooks / Xero 类型的工作流重新设计：用户账户、交易中心、多币别、科目分类、审核状态、报表与稽核记录。",
        "en": "A QuickBooks/Xero-style workflow for user accounts, transaction entry, multi-currency tracking, account mapping, review status, reports, and audit trails.",
    },
    "account_workspace": {"zh-TW": "使用者帳戶工作區", "zh-CN": "用户账户工作区", "en": "User Account Workspace"},
    "select_user_account": {"zh-TW": "選擇使用者帳戶", "zh-CN": "选择用户账户", "en": "Select User Account"},
    "active_account": {"zh-TW": "目前帳戶", "zh-CN": "当前账户", "en": "Active Account"},
    "account_profile": {"zh-TW": "帳戶基本資料", "zh-CN": "账户基本资料", "en": "Account Profile"},
    "create_new_account": {"zh-TW": "建立新使用者帳戶", "zh-CN": "建立新用户账户", "en": "Create New User Account"},
    "update_account": {"zh-TW": "更新帳戶資料", "zh-CN": "更新账户资料", "en": "Update Account Profile"},
    "save_new_account": {"zh-TW": "儲存新帳戶", "zh-CN": "保存新账户", "en": "Save New Account"},
    "account_saved": {"zh-TW": "帳戶資料已儲存。", "zh-CN": "账户资料已保存。", "en": "Account profile saved."},
    "account_created": {"zh-TW": "新使用者帳戶已建立。", "zh-CN": "新用户账户已建立。", "en": "New user account created."},
    "display_name": {"zh-TW": "顯示名稱", "zh-CN": "显示名称", "en": "Display Name"},
    "entity_type": {"zh-TW": "帳戶類型", "zh-CN": "账户类型", "en": "Account Type"},
    "email": {"zh-TW": "電子郵件", "zh-CN": "电子邮件", "en": "Email"},
    "country_region": {"zh-TW": "國家或地區", "zh-CN": "国家或地区", "en": "Country or Region"},
    "tax_id": {"zh-TW": "稅務編號", "zh-CN": "税务编号", "en": "Tax ID"},
    "industry": {"zh-TW": "產業或用途", "zh-CN": "产业或用途", "en": "Industry or Use Case"},
    "base_currency": {"zh-TW": "基準幣別", "zh-CN": "基准币别", "en": "Base Currency"},
    "opening_balance": {"zh-TW": "期初餘額", "zh-CN": "期初余额", "en": "Opening Balance"},
    "account_notes": {"zh-TW": "帳戶備註", "zh-CN": "账户备注", "en": "Account Notes"},
    "dashboard": {"zh-TW": "總覽", "zh-CN": "总览", "en": "Dashboard"},
    "transactions": {"zh-TW": "交易中心", "zh-CN": "交易中心", "en": "Transaction Center"},
    "reports": {"zh-TW": "財務報表", "zh-CN": "财务报表", "en": "Financial Reports"},
    "settings": {"zh-TW": "帳戶與資料管理", "zh-CN": "账户与数据管理", "en": "Account and Data Management"},
    "commercial_logic": {"zh-TW": "商業化會計系統邏輯", "zh-CN": "商业化会计系统逻辑", "en": "Commercial Accounting System Logic"},
    "commercial_logic_text": {
        "zh-TW": "每一筆交易會綁定到特定使用者帳戶，並保留幣別、交易性質、科目、分類、付款方式、審核狀態與稅務標記，方便後續擴充成正式總帳、應收應付與月結流程。",
        "zh-CN": "每一笔交易会绑定到特定用户账户，并保留币别、交易性质、科目、分类、付款方式、审核状态与税务标记，方便后续扩充成正式总账、应收应付与月结流程。",
        "en": "Each transaction is assigned to a specific user account and stores currency, transaction nature, account, category, payment method, review status, and tax flags so the app can expand toward a formal general ledger, receivables/payables, and month-end close workflow.",
    },
    "period_filter": {"zh-TW": "期間", "zh-CN": "期间", "en": "Period"},
    "all_time": {"zh-TW": "全部期間", "zh-CN": "全部期间", "en": "All Time"},
    "current_month": {"zh-TW": "本月", "zh-CN": "本月", "en": "Current Month"},
    "last_90_days": {"zh-TW": "近九十天", "zh-CN": "近九十天", "en": "Last 90 Days"},
    "year_to_date": {"zh-TW": "今年至今", "zh-CN": "今年至今", "en": "Year to Date"},
    "custom_period": {"zh-TW": "自訂期間", "zh-CN": "自定义期间", "en": "Custom Period"},
    "start_date": {"zh-TW": "開始日期", "zh-CN": "开始日期", "en": "Start Date"},
    "end_date": {"zh-TW": "結束日期", "zh-CN": "结束日期", "en": "End Date"},
    "date_hint": {"zh-TW": "格式：YYYY-MM-DD", "zh-CN": "格式：YYYY-MM-DD", "en": "Format: YYYY-MM-DD"},
    "total_income": {"zh-TW": "總收入", "zh-CN": "总收入", "en": "Total Income"},
    "total_expense": {"zh-TW": "總費用", "zh-CN": "总费用", "en": "Total Expenses"},
    "net_profit": {"zh-TW": "淨利", "zh-CN": "净利", "en": "Net Profit"},
    "cash_position": {"zh-TW": "現金餘額", "zh-CN": "现金余额", "en": "Cash Position"},
    "expense_ratio": {"zh-TW": "費用率", "zh-CN": "费用率", "en": "Expense Ratio"},
    "transactions_count": {"zh-TW": "交易筆數", "zh-CN": "交易笔数", "en": "Transaction Count"},
    "top_expense": {"zh-TW": "最大費用類別", "zh-CN": "最大费用类别", "en": "Top Expense Category"},
    "review_needed": {"zh-TW": "待審核交易", "zh-CN": "待审核交易", "en": "Transactions Needing Review"},
    "income_vs_expense": {"zh-TW": "收入與費用趨勢", "zh-CN": "收入与费用趋势", "en": "Income vs. Expense Trend"},
    "expense_distribution": {"zh-TW": "費用分類分布", "zh-CN": "费用分类分布", "en": "Expense Category Distribution"},
    "management_insight": {"zh-TW": "管理洞察", "zh-CN": "管理洞察", "en": "Management Insight"},
    "insight_no_data": {"zh-TW": "尚無足夠資料產生管理洞察。", "zh-CN": "尚无足够数据产生管理洞察。", "en": "Not enough data to generate management insight."},
    "insight_positive": {"zh-TW": "目前帳戶在選定期間為正向淨利，建議持續追蹤費用率與待審核交易。", "zh-CN": "当前账户在选定期间为正向净利，建议持续追踪费用率与待审核交易。", "en": "The active account shows positive net profit in the selected period. Continue monitoring expense ratio and pending reviews."},
    "insight_negative": {"zh-TW": "目前帳戶在選定期間為負向淨利，建議檢查主要費用類別、付款方式與非經常性支出。", "zh-CN": "当前账户在选定期间为负向净利，建议检查主要费用类别、付款方式与非经常性支出。", "en": "The active account shows negative net profit in the selected period. Review major expense categories, payment methods, and non-recurring spending."},
    "recent_transactions": {"zh-TW": "近期交易", "zh-CN": "近期交易", "en": "Recent Transactions"},
    "quick_entry": {"zh-TW": "新增交易", "zh-CN": "新增交易", "en": "Add Transaction"},
    "assigned_user": {"zh-TW": "對應使用者帳戶", "zh-CN": "对应用户账户", "en": "Assigned User Account"},
    "transaction_date": {"zh-TW": "交易日期", "zh-CN": "交易日期", "en": "Transaction Date"},
    "type": {"zh-TW": "交易類型", "zh-CN": "交易类型", "en": "Transaction Type"},
    "account": {"zh-TW": "會計科目", "zh-CN": "会计科目", "en": "Account"},
    "category": {"zh-TW": "管理分類", "zh-CN": "管理分类", "en": "Category"},
    "payee": {"zh-TW": "交易對象", "zh-CN": "交易对象", "en": "Payee"},
    "payee_placeholder": {"zh-TW": "例如：客戶、供應商、店家", "zh-CN": "例如：客户、供应商、店家", "en": "For example: customer, vendor, merchant"},
    "description": {"zh-TW": "交易說明", "zh-CN": "交易说明", "en": "Description"},
    "description_placeholder": {"zh-TW": "輸入這筆交易的商業目的或說明", "zh-CN": "输入这笔交易的商业目的或说明", "en": "Enter the business purpose or transaction description"},
    "amount": {"zh-TW": "交易金額", "zh-CN": "交易金额", "en": "Transaction Amount"},
    "transaction_currency": {"zh-TW": "交易幣別", "zh-CN": "交易币别", "en": "Transaction Currency"},
    "exchange_rate": {"zh-TW": "匯率至基準幣別", "zh-CN": "汇率至基准币别", "en": "Exchange Rate to Base Currency"},
    "base_amount": {"zh-TW": "基準幣別金額", "zh-CN": "基准币别金额", "en": "Base Currency Amount"},
    "transaction_nature": {"zh-TW": "交易性質", "zh-CN": "交易性质", "en": "Transaction Nature"},
    "payment_method": {"zh-TW": "付款方式", "zh-CN": "付款方式", "en": "Payment Method"},
    "status": {"zh-TW": "審核狀態", "zh-CN": "审核状态", "en": "Review Status"},
    "tax_related": {"zh-TW": "稅務相關", "zh-CN": "税务相关", "en": "Tax Related"},
    "attachment_ref": {"zh-TW": "憑證或附件編號", "zh-CN": "凭证或附件编号", "en": "Receipt or Attachment Reference"},
    "notes": {"zh-TW": "備註", "zh-CN": "备注", "en": "Notes"},
    "notes_placeholder": {"zh-TW": "可填寫憑證狀態、補充資訊或審核意見", "zh-CN": "可填写凭证状态、补充信息或审核意见", "en": "Enter receipt status, additional context, or review comments"},
    "save_transaction": {"zh-TW": "儲存交易", "zh-CN": "保存交易", "en": "Save Transaction"},
    "transaction_saved": {"zh-TW": "交易已儲存到目前選取的使用者帳戶。", "zh-CN": "交易已保存到当前选择的用户账户。", "en": "Transaction saved to the selected user account."},
    "validation_description": {"zh-TW": "請輸入交易說明。", "zh-CN": "请输入交易说明。", "en": "Please enter a transaction description."},
    "validation_amount": {"zh-TW": "金額必須大於零。", "zh-CN": "金额必须大于零。", "en": "Amount must be greater than zero."},
    "validation_date": {"zh-TW": "請使用正確日期格式。", "zh-CN": "请使用正确日期格式。", "en": "Please use the correct date format."},
    "validation_user": {"zh-TW": "請先建立或選擇使用者帳戶。", "zh-CN": "请先建立或选择用户账户。", "en": "Please create or select a user account first."},
    "duplicate_warning": {"zh-TW": "系統偵測到可能重複的交易，為避免重複入帳，這筆交易尚未儲存。", "zh-CN": "系统检测到可能重复的交易，为避免重复入账，这笔交易尚未保存。", "en": "A possible duplicate was detected. To prevent duplicate posting, this transaction was not saved."},
    "transaction_not_found": {"zh-TW": "找不到這筆交易，可能已經被刪除或交易清單已更新。", "zh-CN": "找不到这笔交易，可能已经被删除或交易清单已更新。", "en": "Transaction not found. It may have already been deleted or the ledger has been refreshed."},
    "duplicate_user_warning": {"zh-TW": "使用者名稱不可重複。請使用不同的顯示名稱。", "zh-CN": "用户名称不可重复。请使用不同的显示名称。", "en": "User names cannot be duplicated. Please use a different display name."},
    "data_cleaning": {"zh-TW": "資料清理中心", "zh-CN": "数据清理中心", "en": "Data Cleaning Center"},
    "data_cleaning_text": {"zh-TW": "在這裡可以檢視、編輯或刪除目前使用者帳戶的交易明細。所有修改都會寫入稽核紀錄。", "zh-CN": "在这里可以查看、编辑或删除当前用户账户的交易明细。所有修改都会写入稽核记录。", "en": "Review, edit, or delete transactions for the active user account. Every change is recorded in the audit log."},
    "select_transaction_to_clean": {"zh-TW": "選擇要清理的交易", "zh-CN": "选择要清理的交易", "en": "Select Transaction to Clean"},
    "edit_transaction": {"zh-TW": "編輯交易明細", "zh-CN": "编辑交易明细", "en": "Edit Transaction Details"},
    "save_transaction_changes": {"zh-TW": "儲存交易修改", "zh-CN": "保存交易修改", "en": "Save Transaction Changes"},
    "transaction_updated": {"zh-TW": "交易明細已更新。", "zh-CN": "交易明细已更新。", "en": "Transaction details updated."},
    "delete_permanent_warning": {"zh-TW": "刪除後將從目前帳戶交易明細移除。建議先確認交易編號與內容。", "zh-CN": "删除后将从当前账户交易明细移除。建议先确认交易编号与内容。", "en": "Deleting will remove this transaction from the active account ledger. Confirm the transaction ID and details before deleting."},
    "confirm_delete_transaction": {"zh-TW": "我確認要刪除這筆交易", "zh-CN": "我确认要删除这笔交易", "en": "I confirm that I want to delete this transaction"},
    "transaction_ledger": {"zh-TW": "交易明細", "zh-CN": "交易明细", "en": "Transaction Ledger"},
    "search": {"zh-TW": "搜尋交易", "zh-CN": "搜索交易", "en": "Search Transactions"},
    "search_placeholder": {"zh-TW": "搜尋交易對象、說明、分類、科目或幣別", "zh-CN": "搜索交易对象、说明、分类、科目或币别", "en": "Search payee, description, category, account, or currency"},
    "filter_type": {"zh-TW": "類型篩選", "zh-CN": "类型筛选", "en": "Type Filter"},
    "filter_currency": {"zh-TW": "幣別篩選", "zh-CN": "币别筛选", "en": "Currency Filter"},
    "all": {"zh-TW": "全部", "zh-CN": "全部", "en": "All"},
    "income": {"zh-TW": "收入", "zh-CN": "收入", "en": "Income"},
    "expense": {"zh-TW": "費用", "zh-CN": "费用", "en": "Expense"},
    "delete_transaction": {"zh-TW": "刪除交易", "zh-CN": "删除交易", "en": "Delete Transaction"},
    "select_transaction": {"zh-TW": "選擇交易編號", "zh-CN": "选择交易编号", "en": "Select Transaction ID"},
    "delete_selected": {"zh-TW": "刪除選取交易", "zh-CN": "删除选取交易", "en": "Delete Selected Transaction"},
    "deleted": {"zh-TW": "交易已刪除。", "zh-CN": "交易已删除。", "en": "Transaction deleted."},
    "gross_income": {"zh-TW": "營業收入", "zh-CN": "营业收入", "en": "Gross Income"},
    "operating_expense": {"zh-TW": "營業費用", "zh-CN": "营业费用", "en": "Operating Expenses"},
    "net_income": {"zh-TW": "本期淨利", "zh-CN": "本期净利", "en": "Net Income"},
    "profit_margin": {"zh-TW": "淨利率", "zh-CN": "净利率", "en": "Profit Margin"},
    "pnl_report": {"zh-TW": "損益表", "zh-CN": "损益表", "en": "Profit and Loss Statement"},
    "cash_flow_report": {"zh-TW": "現金流量表", "zh-CN": "现金流量表", "en": "Cash Flow Statement"},
    "category_breakdown": {"zh-TW": "分類明細", "zh-CN": "分类明细", "en": "Category Breakdown"},
    "month": {"zh-TW": "月份", "zh-CN": "月份", "en": "Month"},
    "cash_inflow": {"zh-TW": "現金流入", "zh-CN": "现金流入", "en": "Cash Inflow"},
    "cash_outflow": {"zh-TW": "現金流出", "zh-CN": "现金流出", "en": "Cash Outflow"},
    "net_cash_flow": {"zh-TW": "淨現金流", "zh-CN": "净现金流", "en": "Net Cash Flow"},
    "export_transactions": {"zh-TW": "匯出目前帳戶交易明細", "zh-CN": "导出当前账户交易明细", "en": "Export Active Account Transactions"},
    "export_workbook": {"zh-TW": "匯出目前帳戶財務工作簿", "zh-CN": "导出当前账户财务工作簿", "en": "Export Active Account Financial Workbook"},
    "close_readiness": {"zh-TW": "關帳準備度", "zh-CN": "关账准备度", "en": "Close Readiness"},
    "close_item_1": {"zh-TW": "確認所有交易均已綁定到正確使用者帳戶。", "zh-CN": "确认所有交易均已绑定到正确用户账户。", "en": "Confirm every transaction is assigned to the correct user account."},
    "close_item_2": {"zh-TW": "確認每筆交易已填入幣別、匯率、交易性質與會計科目。", "zh-CN": "确认每笔交易已填入币别、汇率、交易性质与会计科目。", "en": "Confirm every transaction includes currency, exchange rate, transaction nature, and account mapping."},
    "close_item_3": {"zh-TW": "審核待審核交易並檢查稅務相關交易與憑證。", "zh-CN": "审核待审核交易并检查税务相关交易与凭证。", "en": "Review pending transactions and check tax-related transactions and receipts."},
    "close_item_4": {"zh-TW": "匯出報表並保存稽核紀錄。", "zh-CN": "导出报表并保存稽核记录。", "en": "Export reports and retain audit records."},
    "import_data": {"zh-TW": "匯入資料", "zh-CN": "导入数据", "en": "Import Data"},
    "paste_csv": {"zh-TW": "貼上交易資料", "zh-CN": "粘贴交易数据", "en": "Paste Transaction Data"},
    "paste_help": {"zh-TW": "第一列需包含欄位名稱。系統會讀取日期、類型、分類、說明、金額、幣別、匯率與交易性質。", "zh-CN": "第一列需包含字段名称。系统会读取日期、类型、分类、说明、金额、币别、汇率与交易性质。", "en": "The first row must contain headers. The system reads date, type, category, description, amount, currency, exchange rate, and transaction nature."},
    "paste_placeholder": {"zh-TW": "日期,類型,分類,說明,金額,幣別,匯率,交易性質\n2026-01-01,費用,餐飲,午餐,12.5,USD,1,營運", "zh-CN": "日期,类型,分类,说明,金额,币别,汇率,交易性质\n2026-01-01,费用,餐饮,午餐,12.5,USD,1,营运", "en": "Date,Type,Category,Description,Amount,Currency,Exchange Rate,Transaction Nature\n2026-01-01,Expense,Food,Lunch,12.5,USD,1,Operating"},
    "import_button": {"zh-TW": "匯入到目前使用者帳戶", "zh-CN": "导入到当前用户账户", "en": "Import to Active User Account"},
    "import_success": {"zh-TW": "匯入完成", "zh-CN": "导入完成", "en": "Import completed"},
    "import_error": {"zh-TW": "匯入失敗，請檢查欄位與資料格式。", "zh-CN": "导入失败，请检查字段与数据格式。", "en": "Import failed. Please check the fields and data format."},
    "download_template": {"zh-TW": "下載匯入範本", "zh-CN": "下载导入模板", "en": "Download Import Template"},
    "data_location": {"zh-TW": "資料儲存位置", "zh-CN": "数据储存位置", "en": "Data Storage Location"},
    "load_demo": {"zh-TW": "載入目前帳戶示範資料", "zh-CN": "载入当前账户示范数据", "en": "Load Demo Data for Active Account"},
    "confirm_clear": {"zh-TW": "我確認要清除目前帳戶的所有交易", "zh-CN": "我确认要清除当前账户的所有交易", "en": "I confirm that I want to clear all transactions for the active account"},
    "clear_active": {"zh-TW": "清除目前帳戶交易", "zh-CN": "清除当前账户交易", "en": "Clear Active Account Transactions"},
    "data_cleared": {"zh-TW": "目前帳戶交易已清除。", "zh-CN": "当前账户交易已清除。", "en": "Active account transactions cleared."},
    "audit_log": {"zh-TW": "稽核紀錄", "zh-CN": "稽核记录", "en": "Audit Log"},
    "no_data": {"zh-TW": "尚無資料。請新增交易或載入示範資料。", "zh-CN": "尚无数据。请新增交易或载入示范数据。", "en": "No data yet. Add a transaction or load demo data."},
    "transaction_id": {"zh-TW": "交易編號", "zh-CN": "交易编号", "en": "Transaction ID"},
    "user_id": {"zh-TW": "使用者編號", "zh-CN": "用户编号", "en": "User ID"},
    "user_name": {"zh-TW": "使用者名稱", "zh-CN": "用户名称", "en": "User Name"},
    "created_at": {"zh-TW": "建立時間", "zh-CN": "建立时间", "en": "Created At"},
    "updated_at": {"zh-TW": "更新時間", "zh-CN": "更新时间", "en": "Updated At"},
    "tax_yes": {"zh-TW": "是", "zh-CN": "是", "en": "Yes"},
    "tax_no": {"zh-TW": "否", "zh-CN": "否", "en": "No"},
    "choose": {"zh-TW": "請選擇", "zh-CN": "请选择", "en": "Choose"},
}

TYPE_LABELS = {
    "Income": {"zh-TW": "收入", "zh-CN": "收入", "en": "Income"},
    "Expense": {"zh-TW": "費用", "zh-CN": "费用", "en": "Expense"},
}

ENTITY_TYPE_LABELS = {
    "Individual": {"zh-TW": "個人", "zh-CN": "个人", "en": "Individual"},
    "Sole Proprietor": {"zh-TW": "獨資經營者", "zh-CN": "独资经营者", "en": "Sole Proprietor"},
    "LLC": {"zh-TW": "有限責任公司", "zh-CN": "有限责任公司", "en": "LLC"},
    "Corporation": {"zh-TW": "公司", "zh-CN": "公司", "en": "Corporation"},
    "Client Account": {"zh-TW": "客戶帳戶", "zh-CN": "客户账户", "en": "Client Account"},
}

TRANSACTION_NATURE_LABELS = {
    "Operating": {"zh-TW": "營運", "zh-CN": "营运", "en": "Operating"},
    "Owner Contribution": {"zh-TW": "業主投入", "zh-CN": "业主投入", "en": "Owner Contribution"},
    "Owner Draw": {"zh-TW": "業主提領", "zh-CN": "业主提领", "en": "Owner Draw"},
    "Reimbursable": {"zh-TW": "可報銷", "zh-CN": "可报销", "en": "Reimbursable"},
    "Refund": {"zh-TW": "退款", "zh-CN": "退款", "en": "Refund"},
    "Transfer": {"zh-TW": "轉帳", "zh-CN": "转账", "en": "Transfer"},
    "Tax Payment": {"zh-TW": "稅款支付", "zh-CN": "税款支付", "en": "Tax Payment"},
    "Non-operating": {"zh-TW": "非營運", "zh-CN": "非营运", "en": "Non-operating"},
}

ACCOUNT_LABELS = {
    "Sales Revenue": {"zh-TW": "銷貨收入", "zh-CN": "销货收入", "en": "Sales Revenue"},
    "Service Revenue": {"zh-TW": "服務收入", "zh-CN": "服务收入", "en": "Service Revenue"},
    "Other Income": {"zh-TW": "其他收入", "zh-CN": "其他收入", "en": "Other Income"},
    "Cost of Goods Sold": {"zh-TW": "銷貨成本", "zh-CN": "销货成本", "en": "Cost of Goods Sold"},
    "Rent Expense": {"zh-TW": "租金費用", "zh-CN": "租金费用", "en": "Rent Expense"},
    "Utilities Expense": {"zh-TW": "水電瓦斯費", "zh-CN": "水电瓦斯费", "en": "Utilities Expense"},
    "Meals & Entertainment": {"zh-TW": "餐飲交際費", "zh-CN": "餐饮交际费", "en": "Meals and Entertainment"},
    "Travel & Transportation": {"zh-TW": "差旅交通費", "zh-CN": "差旅交通费", "en": "Travel and Transportation"},
    "Software & Subscriptions": {"zh-TW": "軟體訂閱費", "zh-CN": "软件订阅费", "en": "Software and Subscriptions"},
    "Professional Fees": {"zh-TW": "專業服務費", "zh-CN": "专业服务费", "en": "Professional Fees"},
    "Office Expense": {"zh-TW": "辦公費用", "zh-CN": "办公费用", "en": "Office Expense"},
    "Other Expense": {"zh-TW": "其他費用", "zh-CN": "其他费用", "en": "Other Expense"},
}

CATEGORY_LABELS = {
    "Salary": {"zh-TW": "薪資", "zh-CN": "薪资", "en": "Salary"},
    "Client Payment": {"zh-TW": "客戶收款", "zh-CN": "客户收款", "en": "Client Payment"},
    "Investment": {"zh-TW": "投資收入", "zh-CN": "投资收入", "en": "Investment"},
    "Bonus": {"zh-TW": "獎金", "zh-CN": "奖金", "en": "Bonus"},
    "Freelance": {"zh-TW": "自由接案", "zh-CN": "自由接案", "en": "Freelance"},
    "Food": {"zh-TW": "餐飲", "zh-CN": "餐饮", "en": "Food"},
    "Transport": {"zh-TW": "交通", "zh-CN": "交通", "en": "Transport"},
    "Rent": {"zh-TW": "租金", "zh-CN": "租金", "en": "Rent"},
    "Utilities": {"zh-TW": "水電瓦斯", "zh-CN": "水电瓦斯", "en": "Utilities"},
    "Entertainment": {"zh-TW": "娛樂交際", "zh-CN": "娱乐交际", "en": "Entertainment"},
    "Software": {"zh-TW": "軟體", "zh-CN": "软件", "en": "Software"},
    "Professional Services": {"zh-TW": "專業服務", "zh-CN": "专业服务", "en": "Professional Services"},
    "Office Supplies": {"zh-TW": "辦公用品", "zh-CN": "办公用品", "en": "Office Supplies"},
    "Other": {"zh-TW": "其他", "zh-CN": "其他", "en": "Other"},
}

PAYMENT_METHOD_LABELS = {
    "Cash": {"zh-TW": "現金", "zh-CN": "现金", "en": "Cash"},
    "Credit Card": {"zh-TW": "信用卡", "zh-CN": "信用卡", "en": "Credit Card"},
    "Debit Card": {"zh-TW": "金融卡", "zh-CN": "借记卡", "en": "Debit Card"},
    "Bank Transfer": {"zh-TW": "銀行轉帳", "zh-CN": "银行转账", "en": "Bank Transfer"},
    "ACH": {"zh-TW": "自動清算轉帳", "zh-CN": "自动清算转账", "en": "ACH"},
    "Other": {"zh-TW": "其他", "zh-CN": "其他", "en": "Other"},
}

STATUS_LABELS = {
    "Reviewed": {"zh-TW": "已審核", "zh-CN": "已审核", "en": "Reviewed"},
    "Needs Review": {"zh-TW": "待審核", "zh-CN": "待审核", "en": "Needs Review"},
}

ACTION_LABELS = {
    "CREATE_TRANSACTION": {"zh-TW": "新增交易", "zh-CN": "新增交易", "en": "Create Transaction"},
    "DELETE_TRANSACTION": {"zh-TW": "刪除交易", "zh-CN": "删除交易", "en": "Delete Transaction"},
    "UPDATE_TRANSACTION": {"zh-TW": "更新交易", "zh-CN": "更新交易", "en": "Update Transaction"},
    "IMPORT_TRANSACTIONS": {"zh-TW": "匯入交易", "zh-CN": "导入交易", "en": "Import Transactions"},
    "LOAD_DEMO": {"zh-TW": "載入示範資料", "zh-CN": "载入示范数据", "en": "Load Demo Data"},
    "CLEAR_ACTIVE": {"zh-TW": "清除目前帳戶交易", "zh-CN": "清除当前账户交易", "en": "Clear Active Account"},
    "CREATE_USER": {"zh-TW": "建立使用者", "zh-CN": "建立用户", "en": "Create User"},
    "UPDATE_USER": {"zh-TW": "更新使用者", "zh-CN": "更新用户", "en": "Update User"},
    "MIGRATE_LEGACY": {"zh-TW": "舊資料轉換", "zh-CN": "旧数据转换", "en": "Legacy Migration"},
}

def t(key: str, lang: str = "en", **kwargs) -> str:
    value = TEXT.get(key, {}).get(lang)
    if value is None:
        value = TEXT.get(key, {}).get("en", key)
    return value.format(**kwargs) if kwargs else value


def label(value: str, mapping: dict, lang: str = "en") -> str:
    if value in mapping:
        return mapping[value].get(lang, mapping[value].get("en", value))
    return str(value)


def reverse_label(display: str, mapping: dict, lang: str = "en") -> str:
    for raw, labels in mapping.items():
        if display == labels.get(lang) or display == labels.get("en"):
            return raw
    return display


# Additional multilingual text for Gemini receipt/screenshot capture workflow.
TEXT.update({
    "gemini_sidebar_title": {"zh-TW": "Gemini 識別設定", "zh-CN": "Gemini 识别设置", "en": "Gemini Recognition Settings"},
    "gemini_api_key": {"zh-TW": "Gemini API 金鑰", "zh-CN": "Gemini API 密钥", "en": "Gemini API Key"},
    "gemini_api_placeholder": {"zh-TW": "貼上目前帳戶專用 API 金鑰", "zh-CN": "粘贴当前账户专用 API 密钥", "en": "Paste the API key for the active account"},
    "gemini_api_notice": {"zh-TW": "API 金鑰只保存在目前瀏覽器 session，不會寫入交易資料。", "zh-CN": "API 密钥只保存在当前浏览器 session，不会写入交易数据。", "en": "The API key stays in the current browser session and is not saved to the ledger."},
    "api_key_account_only": {"zh-TW": "切換使用者帳戶後，系統會清空此 API 金鑰，請重新輸入。", "zh-CN": "切换用户账户后，系统会清空此 API 密钥，请重新输入。", "en": "When you switch user accounts, this API key is cleared and must be re-entered."},
    "api_reset_notice": {"zh-TW": "你已切換使用者帳戶。請重新輸入 Gemini API 金鑰。", "zh-CN": "你已切换用户账户。请重新输入 Gemini API 密钥。", "en": "You switched user accounts. Please re-enter the Gemini API key."},
    "gemini_api_missing": {"zh-TW": "請先在左側 sidebar 輸入 Gemini API 金鑰。", "zh-CN": "请先在左侧 sidebar 输入 Gemini API 密钥。", "en": "Please enter the Gemini API key in the left sidebar first."},
    "capture_center": {"zh-TW": "帳務資料紀錄中心", "zh-CN": "账务数据记录中心", "en": "Bookkeeping Data Capture Center"},
    "capture_center_text": {"zh-TW": "支援手動輸入、手機拍攝收據、以及上傳收入或支出截圖。AI 會先提出判斷，你再做最後確認。", "zh-CN": "支持手动输入、手机拍摄收据、以及上传收入或支出截图。AI 会先提出判断，你再做最后确认。", "en": "Supports manual entry, mobile receipt capture, and income/expense screenshot upload. AI suggests the accounting treatment, and you make the final decision."},
    "manual_entry": {"zh-TW": "手動輸入", "zh-CN": "手动输入", "en": "Manual Entry"},
    "manual_tab_help": {"zh-TW": "適合直接手動 key in 收入、支出或調整分錄。", "zh-CN": "适合直接手动 key in 收入、支出或调整分录。", "en": "Use this for direct manual entry of income, expenses, or adjustments."},
    "receipt_photo": {"zh-TW": "收據拍照", "zh-CN": "收据拍照", "en": "Receipt Photo"},
    "receipt_photo_help": {"zh-TW": "用手機相機拍攝收據，或上傳已拍好的收據圖片。系統會用 Gemini 判斷收入或支出、金額、幣別、分類與交易性質。", "zh-CN": "用手机相机拍摄收据，或上传已拍好的收据图片。系统会用 Gemini 判断收入或支出、金额、币别、分类与交易性质。", "en": "Take a receipt photo on mobile or upload an existing receipt image. Gemini estimates income/expense type, amount, currency, category, and transaction nature."},
    "income_expense_screenshot": {"zh-TW": "收入／支出截圖", "zh-CN": "收入／支出截图", "en": "Income/Expense Screenshot"},
    "income_expense_screenshot_help": {"zh-TW": "上傳銀行、信用卡、付款平台、發票或收入截圖。AI 會萃取交易資訊並列出可能選項。", "zh-CN": "上传银行、信用卡、付款平台、发票或收入截图。AI 会萃取交易信息并列出可能选项。", "en": "Upload a bank, card, payment platform, invoice, income, or expense screenshot. AI extracts the transaction and lists possible options."},
    "take_receipt_photo": {"zh-TW": "用手機或相機拍攝收據", "zh-CN": "用手机或相机拍摄收据", "en": "Take a Receipt Photo"},
    "or_upload_receipt": {"zh-TW": "或上傳收據圖片", "zh-CN": "或上传收据图片", "en": "Or Upload Receipt Image"},
    "upload_screenshot": {"zh-TW": "上傳收入或支出截圖", "zh-CN": "上传收入或支出截图", "en": "Upload Income or Expense Screenshot"},
    "image_preview": {"zh-TW": "圖片預覽", "zh-CN": "图片预览", "en": "Image Preview"},
    "analyze_with_gemini": {"zh-TW": "使用 Gemini 識別並判斷", "zh-CN": "使用 Gemini 识别并判断", "en": "Analyze with Gemini"},
    "ai_processing": {"zh-TW": "Gemini 正在識別圖片並判斷交易性質...", "zh-CN": "Gemini 正在识别图片并判断交易性质...", "en": "Gemini is reading the image and estimating the accounting treatment..."},
    "ai_extraction_failed": {"zh-TW": "AI 識別失敗", "zh-CN": "AI 识别失败", "en": "AI extraction failed"},
    "ai_suggestion_ready": {"zh-TW": "AI 已產生建議。請檢查並做最後確認。", "zh-CN": "AI 已生成建议。请检查并做最后确认。", "en": "AI suggestions are ready. Please review and make the final decision."},
    "ai_review_and_confirm": {"zh-TW": "檢查 AI 建議並確認入帳", "zh-CN": "检查 AI 建议并确认入账", "en": "Review AI Suggestions and Confirm Posting"},
    "ai_multiple_options": {"zh-TW": "AI 偵測到多種可能性。請從下拉選單選擇最正確的結果。", "zh-CN": "AI 检测到多种可能性。请从下拉选单选择最正确的结果。", "en": "AI detected multiple possibilities. Select the final treatment from the dropdown options."},
    "detected_possibilities": {"zh-TW": "AI 判斷可能性", "zh-CN": "AI 判断可能性", "en": "Detected Possibilities"},
    "ai_confidence": {"zh-TW": "AI 信心水準", "zh-CN": "AI 信心水准", "en": "AI Confidence"},
    "capture_source": {"zh-TW": "資料來源", "zh-CN": "资料来源", "en": "Capture Source"},
    "confirm_and_save": {"zh-TW": "確認並記錄交易", "zh-CN": "确认并记录交易", "en": "Confirm and Save Transaction"},
    "discard_capture": {"zh-TW": "放棄本次識別", "zh-CN": "放弃本次识别", "en": "Discard This Capture"},
    "temp_image_cleared": {"zh-TW": "暫存圖片已清除。", "zh-CN": "暂存图片已清除。", "en": "Temporary image cleared."},
    "raw_ai_json": {"zh-TW": "AI 原始識別結果", "zh-CN": "AI 原始识别结果", "en": "Raw AI Extraction Result"},
})
ACTION_LABELS.update({
    "AI_CAPTURE_TRANSACTION": {"zh-TW": "AI 圖片入帳", "zh-CN": "AI 图片入账", "en": "AI Image Capture Transaction"},
})
