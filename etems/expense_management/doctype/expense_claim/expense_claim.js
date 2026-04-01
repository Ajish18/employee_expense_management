// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Claim", {
    setup(frm) {
        if(frappe.session.user!=="Administrator"){
            frm.set_query("employee_id", function(){
                return{
                    filters: {
                        user_id:frappe.session.user,
                    }
                }
            })
        };
        frm.set_query("category","expense_details", function(){
            return{
                filters: {
                    is_group:0,
                }
            }
        }),
        frm.set_query("travel_request", function(){
            return{
                filters: {
                    status:"Approved",
                }
            }
        });
        frm.set_query("travel_request",function(){
            return{
                filters: {
                    expense_claimed: 0,
                    status: "Approved",
                }
            }
        })
    },
    refresh(frm) {
        if (frm.doc.workflow_state === "Verified" && !frm.doc.verified_by) {
            frm.set_value("verified_byuser_id", frappe.session.user)
        }
        if (frappe.user.has_role("Employee")) {
            frm.set_df_property("total_approved_amount", "read_only", 1);
        }
        if (frm.doc.workflow_state === "Approved" && !frm.doc.approved_by) {
            frm.set_value("approved_byuser_id", frappe.session.user)
        }
    },
    after_workflow_action: function(frm) {
        frm.save();
    }
});

frappe.ui.form.on("Expense Details",{
    amount(frm,cdt,cdn){
        calculate_amount(frm,cdt,cdn)
    },
    approve_amount(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        if(row.approve_amount>row.amount){
            frappe.msgprint("Approved amount cannot be greater than claimed amount")
            frm.set_value("approve_amount",0)
        }
        else{
            calculate_approve_amount(frm,cdt,cdn)
        }
    }
});

function calculate_amount(frm,cdt,cdn){
    let sum=0;
    let row=locals[cdt][cdn]
    frm.doc.expense_details.forEach(row => {
        sum+=row.amount;
    });
    frm.set_value("total_claimed_amount",sum);
}

function calculate_approve_amount(frm,cdt,cdn){
    let sum=0;
    let row=locals[cdt][cdn]
    frm.doc.expense_details.forEach(row => {
        sum+=row.approve_amount;
    });
    frm.set_value("total_approved_amount",sum);
}