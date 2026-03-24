// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Details", {
	setup(frm) {
		frm.set_query("reporting_manager", function () {
			return {
				filters: {
					role: "Reporting Manager",
				},
			};
		});
	},
});
