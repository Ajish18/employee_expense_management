import frappe

@frappe.whitelist()
def ask_ai(message):

    message = message.lower().strip()

    if message == "open customer":
        return {
            "action": "open_list",
            "doctype": "Customer",
            "response": "Opening Customer List..."
        }

    return {
        "action": "message",
        "response": f"You said: {message}"
    }