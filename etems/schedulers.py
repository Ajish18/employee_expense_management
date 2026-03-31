import frappe
from frappe.utils import getdate, add_days
def settlement_remainders():
    remainder_days=frappe.db.get_single_value("Policy Settings", "settlement_due_days")
    expense_claims=frappe.db.get_all(
        "Expense Claim",
        filters={"settlement_status": "payable","status": "Approved"},
        fields=["name", "employee_id","email","final_approval_date","balance_receivable"])
    
    for claim in expense_claims:
        remainder=add_days(claim.final_approval_date, remainder_days)
        if(getdate()>=getdate(remainder)):
            employee=frappe.db.get_value("Employee Details", claim.employee_id, "employee_name")
            frappe.sendmail(
                recipients=claim.email,
                subject="Settlement Remainder",
                message=f"""
                Dear {employee},<br>
                This is a reminder that your expense claim {claim.name} with a balance receivable of {claim.balance_receivable} is due for settlement on {remainder}.<br>
                Please ensure that you complete the settlement process by the due date to avoid any delays in reimbursement.<br>"""
                )
            
def settlement_notifications():
    remainder_days=frappe.db.get_single_value("Policy Settings", "settlement_due_days")
    expense_claims=frappe.db.get_all(
        "Expense Claim",
        fields=["name", "employee_id","email","final_approval_date","balance_receivable","status","settlement_status"])
    
    pending=[]
    overdue=[]
    for claim in expense_claims:
        if(claim.status=="Approved"):
            remainder=add_days(claim.final_approval_date, remainder_days)
            if(getdate()>=getdate(remainder)):
                overdue.append(claim)
        if(claim.settlement_status=="Pending"):
            pending.append(claim)
    
    mail_notification(pending,overdue)

def mail_notification(pending,overdue):
        message = "<h3>Expense Claim Summary Report</h3>"
        message += f"<h4>Pending Claims (Total: {len(pending)})</h4>"
        if pending:
            message += "<ul>"
            for c in pending:
                message += f"<li>{c.name} - {c.employee_id}</li>"
            message += "</ul>"
        else:
            message += "<p>No pending claims</p>"

        message += f"<h4 style='color:red;'>Overdue Claims (Total: {len(overdue)})</h4>"
        if overdue:
            message += "<ul>"
            for c in overdue:
                message += f"<li>{c.name} - {c.employee_id}</li>"
            message += "</ul>"
        else:
            message += "<p>No overdue claims</p>"
        frappe.sendmail(
            recipients=frappe.db.get_single_value("Policy Settings", "manager_email"),
            subject="Expense Claim Summary Notification",
            message=message,
            now=True
        )