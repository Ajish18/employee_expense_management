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
            <p>Dear {doc.employee_name},</p>
            <p>
            Your Travel Request <b>{doc.name}</b> has been sent for 
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
            <p>Dear {doc.employee_name},</p>
            <p>
            Your Travel Request <b>{doc.name}</b> has been Rejected by your Reporting Manager.
            </p>
            <p>
            Please contact your manager for more details.
            </p>
            <p>
            Regards,<br>
            Reporting Manager,<br>
            <b>{doc.reporting_manager_name}</b>
            </p>
            """
        )

@frappe.whitelist()
def finance_manager_reject(name,reason):
    frappe.db.set_value("Travel Request", name, "status", "Cancelled")
    doc=frappe.get_doc("Travel Request", name)
    doc.cancel_reason=reason
    doc.save()
    doc.submit()
    doc.cancel()
    frappe.sendmail(
            recipients=[doc.email],
            subject="Travel Request Rejected",
            message=f"""
            Dear {doc.employee_name},
            Your Travel Request <b>{doc.name}</b> has been rejected/cancelled by the Finance Manager.
            <b>Reason:</b> {reason}
            Please contact the Finance team for more details.
            Regards,<br>
            Finance Team
            """
        )

@frappe.whitelist()
def finance_manager_approval(name):
    frappe.db.set_value("Travel Request", name, "status", "Approved")
    doc=frappe.get_doc("Travel Request", name)
    doc.submit()
    if doc.email:
        frappe.sendmail(
            recipients=[doc.email],
            subject="Travel Request Rejected",
            message=f"""
            <p>Dear {doc.employee_name},</p>
            <p>
            Your Travel Request <b>{doc.name}</b> has been approved by the Finance Manager. 
            </p>
            <p>
            Please contact your manager for more details.
            </p>
            <p>
            Regards,<br>
            Finace Team,<br>
            </p>
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
        `tabTravel Request`.status IN ('Pending Finance Verification', 'Cancelled') """
    return ""