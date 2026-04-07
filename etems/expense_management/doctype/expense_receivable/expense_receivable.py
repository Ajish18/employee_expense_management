# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExpenseReceivable(Document):
	def on_submit(self):
		amount_received=frappe.db.get_value("Expense Claim", self.expense_claim, "amount_settled")
		amount=amount_received+self.amount_received
		frappe.db.set_value("Expense Claim", self.expense_claim, "amount_settled", amount)
		if amount==self.total_receivable_amount:
			frappe.db.set_value("Expense Claim", self.expense_claim, "settlement_status", "Settled")
			frappe.db.set_value("Expense Claim", self.expense_claim, "status", "Settled")
			frappe.db.set_value("Expense Claim", self.expense_claim, "workflow_state", "Settled")
			frappe.db.set_value("Travel Request",self.expense_claimed,"expense_claimed",1)
