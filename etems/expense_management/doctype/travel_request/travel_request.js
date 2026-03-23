// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Travel Request", {
	refresh(frm) {
        if(frm.doc.status==="Pending Manager Approval"  && (frappe.user.has_role("Reporting Manager") ||frappe.user.has_role("Reporting Manager"))
        && frm.doc.docstatus!==1){
            frm.add_custom_button("Approve", ()=>{
                frappe.call({
                    method:"etems.expense_management.doctype.travel_request.travel_request.manager_approval",
                    args:{
                        name:frm.doc.name
                    },
                    callback:function(){
                        frm.reload_doc();
                    }
                })
            });

            frm.add_custom_button("Reject",()=>{
                frappe.call({
                    method:"etems.expense_management.doctype.travel_request.travel_request.manager_reject",
                    args:{
                        name:frm.doc.name
                    },
                    callback:function(){
                        frm.reload_doc();
                    }
                })
            });
        }

	},
});
