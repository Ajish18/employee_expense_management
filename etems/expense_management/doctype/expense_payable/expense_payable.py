# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExpensePayable(Document):
	def on_submit(self):
		amount_settled=frappe.db.get_value("Expense Claim", self.expense_claim, "amount_settled")
		amount=amount_settled+self.amount_paid
		frappe.db.set_value("Expense Claim", self.expense_claim, "amount_settled", amount)
		if amount==self.total_payable_amount:
			frappe.db.set_value("Expense Claim", self.expense_claim, "settlement_status", "Settled")
			frappe.db.set_value("Expense Claim", self.expense_claim, "status", "Settled")
			frappe.db.set_value("Expense Claim", self.expense_claim, "workflow_state", "Settled")
			travel_request=frappe.db.get_value("Expense Claim", self.expense_claim, "travel_request")
			frappe.db.set_value("Travel Request",travel_request,"expense_claimed",1)