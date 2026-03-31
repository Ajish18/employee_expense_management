# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters:None):
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
            "label":"Branch",
            "fieldname": "branch",
            "fieldtype": "Data",
        },
        {
            "label":"No. of Travel Request",
            "fieldname": "travel_count",
            "fieldtype": "Int",
        },
        {
            "label":"No. of Expense Claims",
            "fieldname": "expense_count",
            "fieldtype": "Int",
        },
        {
            "label":"Total Estimated Amount",
            "fieldname": "estimated_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Total Approved Amount",
            "fieldname": "approved_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Advance Amount",
            "fieldname": "advance_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Total Payable Amount",
            "fieldname": "payable_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Total Receivable Amount",
            "fieldname": "receivable_amount",
            "fieldtype": "Currency",
        },
        {
            "label":"Pending Count",
            "fieldname": "pending",
            "fieldtype": "Int",
        },
        
    ]


def get_data(filters):
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    pass