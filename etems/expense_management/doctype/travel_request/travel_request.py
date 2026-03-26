# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TravelRequest(Document):
    def on_update(self):
        if(self.workflow_state in ["Approved","Rejected","Pending Finance Verification"]):
            action=""
            user = frappe.session.user
            roles = frappe.get_roles(user)
            if "Administrator" in roles:
                action = "Administrator"
            elif "Reporting Manager" in roles:
                action = "Reporting Manager"
            elif "Finance Manager" in roles:
                action = "Finance Manager"
            email_template = frappe.get_doc("Email Template", "Travel Request Email")
            frappe.sendmail(
                recipients=[self.email],
                subject=frappe.render_template(email_template.subject, {"doc": self}),
                content=frappe.render_template(email_template.response, {
                    "doc": self,
                    "action_by": action
                }),
            )

        # if self.workflow_state=="Rejected":
        #     self.send_rejection_mail()

    # def send_rejection_mail(self):
    #     user=frappe.session.user
    #     rejected_by=""
    #     if "Reporting Manager" in frappe.get_roles(user):
    #         rejected_by="Reporting Manager"
    #     else:
    #         rejected_by="Finance Manager"

    #     frappe.sendmail(
    #     recipients=[self.email],
    #     subject="Travel Request Rejected",
    #     message=f"""
    #         Dear {self.employee_name},<br>
    #         Your Travel Request <b>{self.name}</b> has been <b>rejected</b> by {rejected_by}.<br><br>
    #         Please contact your manager for more details.<br>

    #         Regards,<br>
    #         ETEMS System
    #     """
    #     )
            



def travel_request_query(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or user == "Administrator":
        return
    if "Reporting Manager" in roles:
        return f"""
        `tabTravel Request`.reporting_manager='{user}'
        """
    if "Finance Manager" in roles:
        return """
        `tabTravel Request`.status IN ('Pending Finance Verification', 'Cancelled') """
    return ""
