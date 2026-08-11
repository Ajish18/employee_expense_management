// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Payable", {
    setup(frm) {
        frm.set_query("expense_claim", function(){
            return{
                filters: {
                    balance_payable:["!=",0],
                    status: ['!=', 'Settled'],
                }
            }
        })
    },
    expense_claim(frm){
        frm.doc.balance=frm.doc.total_payable_amount-frm.doc.settled_amount
        frm.refresh_field("balance")
    },
    amount_paid(frm){
        if(frm.doc.amount_paid>frm.doc.balance){
            frappe.msgprint("Amount paid cannot be greater than balance amount")
            frm.set_value("amount_paid",0)
        }
    }
});
