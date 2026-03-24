// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Travel Request", {
	refresh(frm) {
        if(frm.doc.status==="Pending Manager Approval"  && (frappe.user.has_role("Reporting Manager"))
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

        if(frm.doc.status==="Pending Finance Verification"  && (frappe.user.has_role("Finance Manager"))
        && frm.doc.docstatus!==1){
            frm.add_custom_button("Cancel", ()=>{
                let d=new frappe.ui.Dialog({
                    title:"Reason for Cancellation",
                    fields:[
                        {
                            label:"Cancel",
                            fieldname:"cancel",
                            fieldtype:"Small Text",
                            reqd: 1
                        }
                    ],
                    primary_action_label:"Submit",
                    primary_action(values){
                        frappe.call({
                        method:"etems.expense_management.doctype.travel_request.travel_request.finance_manager_reject",
                        args:{
                            name:frm.doc.name,
                            reason:values.cancel
                        },
                        callback:function(){
                            d.hide()
                            frm.reload_doc();
                        }
                    })
                    }
                })
                d.show();
            });

            frm.add_custom_button("Approve", ()=>{
                frappe.call({
                    method:"etems.expense_management.doctype.travel_request.travel_request.finance_manager_approval",
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
