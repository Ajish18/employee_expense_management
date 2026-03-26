import frappe

def after_install():
    create_roles()
    create_workflow_state()
    create_workflow_action_master()
    create_travel_request_workflow()
    create_expense_claim_workflow()

def create_roles():
    roles = ["Employee", "Reporting Manager", "Finance Manager", "Finance User","Auditor"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role
            }).insert(ignore_permissions=True)

    frappe.db.commit()
def create_workflow_action_master():
    actions=["Settled","Verified","Submit","Send to Reporting Manager","Review","Reject","Approve"]
    for action in actions:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc({
                "doctype":"Workflow Action Master",
                "workflow_action_name":action
            }).insert(ignore_permissions=True)
    frappe.db.commit()

def create_workflow_state():
    states=["Settled","Verified","Draft","Pending Finance Verification","Pending Manager Approval","Rejected","Approved","Pending"]
    for state in states:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc({
                "doctype":"Workflow State",
                "workflow_state_name":state
            }).insert(ignore_permissions=True)
    frappe.db.commit()


def create_travel_request_workflow():
    workflow="Travel Request Workflow"
    if frappe.db.exists("Workflow", workflow):
        return
    
    frappe.get_doc({
        "doctype":"Workflow",
        "workflow_name":workflow,
        "document_type":"Travel Request",
        "is_active":1,
        "workflow_state_field":"workflow_state",
        "states":[
            {
                "state": "Draft",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Draft",
                "allow_edit": "Employee"
            },
            {
                "state": "Pending Manager Approval",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Pending Manager Approval",
                "allow_edit": "Reporting Manager"
            },
            {
                "state": "Pending Finance Verification",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Pending Finance Verification",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Approved",
                "doc_status": 1,
                "update_field": "status",
                "update_value": "Approved",
                "allow_edit": "Administrator"
            },
            {
                "state": "Rejected",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Rejected",
                "allow_edit": "Administrator"
            }
        ],
        "transitions":[
             {
                "state": "Draft",
                "action": "Submit",
                "next_state": "Pending Manager Approval",
                "allowed": "Employee"
            },
            {
                "state": "Pending Manager Approval",
                "action": "Approve",
                "next_state": "Pending Finance Verification",
                "allowed": "Reporting Manager"
            },
            {
                "state": "Pending Manager Approval",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Reporting Manager"
            },
            {
                "state": "Pending Finance Verification",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Finance Manager"
            },
            {
                "state": "Pending Finance Verification",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Finance Manager"
            }
        ]
    }).insert(ignore_permissions=True)
    frappe.db.commit()

def create_expense_claim_workflow():
    workflow="Expense Claim Workflow"
    if frappe.db.exists("Workflow", workflow):
        return
    frappe.get_doc({
        "doctype":"Workflow",
        "workflow_name":workflow,
        "document_type":"Expense Claim",
        "is_active":1,
        "workflow_state_field":"workflow_state",
        "states":[
            {
                "state": "Draft",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Draft",
                "allow_edit": "Employee"
            },
            {
                "state": "Pending Manager Approval",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Pending Manager Approval",
                "allow_edit": "Reporting Manager"
            },
            {
                "state": "Pending Finance Verification",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Pending Finance Verification",
                "allow_edit": "Finance User"
            },
            {
                "state": "Verified",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Verified",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Approved",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Approved",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Settled",
                "doc_status": 1,
                "update_field": "status",
                "update_value": "Settled",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Rejected",
                "doc_status": 1,
                "update_field": "status",
                "update_value": "Rejected",
                "allow_edit": "System Manager"
            }
        ],
        "transitions":[
            {
                "state": "Draft",
                "action": "Submit",
                "next_state": "Pending Manager Approval",
                "allowed": "Employee"
            },
            {
                "state": "Pending Manager Approval",
                "action": "Approve",
                "next_state": "Pending Finance Verification",
                "allowed": "Reporting Manager"
            },
            {
                "state": "Pending Manager Approval",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Reporting Manager"
            },
            {
                "state": "Pending Finance Verification",
                "action": "Verified",
                "next_state": "Verified",
                "allowed": "Finance User"
            },
            {
                "state": "Pending Finance Verification",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Finance User"
            },
            {
                "state": "Verified",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Finance Manager"
            },
            {
                "state": "Verified",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Finance Manager"
            },
            {
                "state": "Approved",
                "action": "Settled",
                "next_state": "Settled",
                "allowed": "Finance Manager"
            }
        ]
    }).insert(ignore_permissions=True)
    frappe.db.commit()
