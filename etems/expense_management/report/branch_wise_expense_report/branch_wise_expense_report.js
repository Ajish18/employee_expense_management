// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.query_reports["Branch Wise Expense Report"] = {
	filters: [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": "to Date",
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options":"Employee Details"
		},
		{
			"fieldname": "branch",
			"label": "Branch",
			"fieldtype": "Link",
			"options":"Branch"
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Link",
			"options":"Department",
		},
		{
			"fieldname": "workflow_status",
			"label": "Status",
			"fieldtype": "Select",
			"options":"\nDraft\nPending Manager Approval\nPending Finance Verification\nVerified\nApproved\nSettled\nRejected"
		},
		{
			"fieldname": "reimbursement_status",
			"label": "Reimbursement Status",
			"fieldtype": "Select",
			"Options": "\nPending\nPayable\nReceivable\nNot Required",
		}
	],
};
