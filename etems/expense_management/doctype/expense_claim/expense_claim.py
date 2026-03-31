# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExpenseClaim(Document):
    def before_save(self):
        if self.status=="Pending Finance Verification":
            self.validate_advance_settlement()
        # if self.status=="Settled":
        #     if self.amount_settled==self.total_approved_amount:
        #         self.settlement_status="Settled"
        #         self.status="Settled"
        #         self.workflow_state="Approved"

    def on_update(self):
        self.update_mail_notification()
        
    def validate_advance_settlement(self):
        self.total_approved_expense=self.total_approved_amount
        if(self.advance_taken>self.total_approved_amount):
            balance=self.advance_taken-self.total_approved_amount
            self.balance_receivable=balance
            self.balance_payable=0
            self.settlement_status="Receivable"
        elif(self.advance_taken<self.total_approved_amount):
            balance=self.total_approved_amount-self.advance_taken
            self.balance_payable=balance
            self.balance_receivable=0
            self.settlement_status="Payable"
        else:
            self.settlement_status="Not Required"
    
    def update_mail_notification(self):
        if(self.workflow_state in ["Approved","Rejected","Pending Finance Verification","Verified"]):
            action=""
            user = frappe.session.user
            roles = frappe.get_roles(user)
            if "Administrator" in roles:
                action = "Administrator"
            elif "Reporting Manager" in roles:
                action = "Reporting Manager"
            elif "Finance Manager" in roles:
                action = "Finance Manager"
            elif "Finance User" in roles:
                action="Finance User"
            email_template = frappe.get_doc("Email Template", "Expense Claim Email")
            frappe.sendmail(
                recipients=[self.email],
                subject=frappe.render_template(email_template.subject, {"doc": self}),
                content=frappe.render_template(email_template.response, {
                    "doc": self,
                    "action_by": action
                }),
            )
