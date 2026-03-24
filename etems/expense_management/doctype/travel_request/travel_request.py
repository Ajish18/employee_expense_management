# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TravelRequest(Document):
    
    def before_save(self):
        if self.is_new():
            self.status="Pending Manager Approval"

    def on_cancel(self):
        self.status="Rejected"


@frappe.whitelist()
def manager_approval(name):
    frappe.db.set_value("Travel Request", name, "status", "Pending Finance Verification")
    doc=frappe.get_doc("Travel Request", name)
    if doc.email:
        frappe.sendmail(
            recipients=[doc.email],
            subject="Travel Request Rejected",
            message=f"""
            Dear {doc.employee_name},
            Your travel request {doc.name} has been sent for finace verification by your reporting manager.
            Please contact your manager for more details.

            Regards,
            Reporting Manager,
            {doc.reporting_manager_name}
            """
        )

@frappe.whitelist()
def manager_reject(name):
    frappe.db.set_value("Travel Request", name, "status", "Rejected")
    doc=frappe.get_doc("Travel Request", name)
    frappe.sendmail(
            recipients=[doc.email],
            subject="Travel Request Rejected",
            message=f"""
            Dear {doc.employee_name},
            Your travel request {doc.name} has been rejected by your reporting manager.
            Please contact your manager for more details.
            Regards,
            Reporting Manager,
            {doc.reporting_manager_name}
            """
        )


def travel_request_query(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or user == "Administrator":
        return
    if "Reporting Manager" in roles:
        return f"""
        `tabTravel Request`.reporting_manager='{user}'
        """
    if "Finance Manager" in roles:
        return f"""
        `tabTravel Request`.status='Pending Finance Verification' """
    return ""