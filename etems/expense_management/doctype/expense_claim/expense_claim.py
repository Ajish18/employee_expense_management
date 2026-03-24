# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExpenseClaim(Document):
	def before_save(self):
		self.validate_advance_settlement()
		if self.is_new():
			self.status = "Pending Manager Approval"

	def validate_advance_settlement(self):
		self.total_approved_expense=self.total_approved_amount
		if(self.advance_taken>self.total_approved_amount):
			balance=self.advance_taken-self.total_approved_amount
			self.balance_receivable=balance
			self.balance_payable=0
			self.settlement_status="Receivable"
		else:
			balance=self.total_approved_amount-self.advance_taken
			self.balance_payable=balance
			self.balance_receivable=0
			self.settlement_status="Payable"

@frappe.whitelist()
def manager_approval(name):
	frappe.db.set_value("Expense Claim", name, "status", "Pending Finance Verification")
	doc = frappe.get_doc("Expense Claim", name)
	doc.verified=1
	doc.save()
	if doc.email:
		frappe.sendmail(
			recipients=[doc.email],
			subject="Expense Claim Manager Approved",
			message=f"""
            <p>Dear {doc.employee_id},</p>
            <p>
            Your Expense Claim Request <b>{doc.name}</b> has been sent for
            <b>Finance Verification</b> by your Reporting Manager.
            </p>
            <p>
            Please contact your manager for more details.
            </p>
            <p>
            Regards,<br>
            Reporting Manager,<br>
            <b>{doc.reporting_manager_name}</b>
            </p>
            """,
		)