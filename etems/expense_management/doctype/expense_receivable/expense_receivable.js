// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Receivable", {
    setup(frm) {
        frm.set_query("expense_claim", function(){
            return{
                filters: {
                    balance_receivable:["!=",0],
                    status: ['!=', 'Settled']
                }
            }
        })
    },
    expense_claim(frm){
        frm.doc.balance=frm.doc.total_receivable_amount-frm.doc.settled_amount
        frm.refresh_field("balance")
    },
    amount_received(frm){
        if(frm.doc.amount_received>frm.doc.balance){
            frappe.msgprint("Amount Receivable cannot be greater than balance amount")
            frm.set_value("amount_received",0)
        }
    }
});
