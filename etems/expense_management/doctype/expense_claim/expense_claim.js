// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Claim", {
	setup(frm) {
        frm.set_query("category","expense_details", function(){
            return{
                filters: {
                    is_group:0,
                }
            }
        })
	},
    refresh(frm){
        if (
			frm.doc.status === "Pending Manager Approval" &&
			frappe.user.has_role("Reporting Manager") &&
			frm.doc.docstatus !== 1
		) {
			frm.add_custom_button("Approve", () => {
				frappe.call({
					method: "etems.expense_management.doctype.expense_claim.expense_claim.manager_approval",
					args: {
						name: frm.doc.name,
					},
					callback: function () {
						frm.reload_doc();
					},
				});
			});

			frm.add_custom_button("Reject", () => {
				frappe.call({
					method: "etems.expense_management.doctype.travel_request.travel_request.manager_reject",
					args: {
						name: frm.doc.name,
					},
					callback: function () {
						frm.reload_doc();
					},
				});
			});
		}
    }
});

frappe.ui.form.on("Expense Details",{
    amount(frm,cdt,cdn){
        calculate_amount(frm,cdt,cdn)
    },
});

function calculate_amount(frm,cdt,cdn){
    let sum=0;
    let row=locals[cdt][cdn]
    frm.doc.expense_details.forEach(row => {
        sum+=row.amount;
    });
    frm.set_value("total_claimed_amount",sum);
}
