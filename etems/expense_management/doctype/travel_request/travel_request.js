// // Copyright (c) 2026, ajish and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Travel Request", {
	setup(frm) {
		if(frappe.session.user!=="Administrator"){
		frm.set_query("employee_id", function () {
			return {
				filters: {
					user_id:frappe.session.user,
				},
			};
		});
	}
	},
});
