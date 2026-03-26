# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label":"Expense Claim ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options":"Expense Claim"
        },
        {
            "label":"Claim Date",
            "fieldname": "creation",
            "fieldtype": "Datetime",
        },
        {
            "label":"Employee ID",
            "fieldname": "employee_id",
            "fieldtype": "Link",
            "options":"Employee Details"
        },
        {
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Link",
            "options":"Branch"
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options":"Department",
        },
        {
            "label": "Travel Request",
            "fieldname": "travel_request",
            "fieldtype": "Link",
            "options":"Travel Request",
        },
        {
            "label": "Total Claimed Amount",
            "fieldname": "total_claimed_amount",
            "fieldtype": "Currency",
        },
        {
            "label": "Total Approved Amount",
            "fieldname": "total_approved_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Advance",
            "fieldname":"advance_taken",
            "fieldtype":"Currency"
        },
        {
            "fieldname": "balance_payable",
            "fieldtype": "Currency",
            "label": "Balance Payable",
        },
        {
            "fieldname": "balance_receivable",
            "fieldtype": "Currency",
            "label": "Balance Receivable",
        },
        {
            "fieldname": "settlement_status",
            "fieldtype": "Select",
            "label": "Settlement Status",
            "options": "Pending\nPayable\nReceivable\nSettled\nNot Required",
        },
        {
            "label": "Workflow Status",
            "fieldname": "status",
            "fieldtype": "Data"
        }
    ]


def get_data(filters):
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    conditions = ""

    if filters.get("from_date"):
        conditions += f" AND ec.creation >= '{filters.get('from_date')}'"

    if filters.get("to_date"):
        conditions += f" AND ec.creation <= '{filters.get('to_date')}'"

    if filters.get("employee"):
        conditions += f" AND ec.employee_id = '{filters.get('employee')}'"

    if filters.get("branch"):
        conditions += f" AND ec.branch = '{filters.get('branch')}'"

    if filters.get("department"):
        conditions += f" AND ec.department = '{filters.get('department')}'"

    if filters.get("workflow_status"):
        conditions += f" AND ec.status = '{filters.get('workflow_status')}'"

    if filters.get("reimbursement_status"):
        conditions += f" AND ec.settlement_status = '{filters.get('reimbursement_status')}'"

    data = frappe.db.sql(f"""
        SELECT
            ec.name,
            ec.creation,
            ec.employee_id,
            ec.branch,
            ec.department,
            ec.travel_request,
            ec.total_claimed_amount,
            ec.total_approved_amount,
            ec.advance_taken,
            ec.balance_payable,
            ec.balance_receivable,
            ec.settlement_status,
            ec.status
        FROM `tabExpense Claim` ec
        WHERE 1=1 {conditions}
        ORDER BY ec.creation DESC
    """, as_dict=True)

    return data


