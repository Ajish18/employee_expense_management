frappe.listview_settings["Travel Request"] = {
    add_fields: ["status"],
    has_indicator_for_draft: false,
    get_indicator: function (doc) {
        if (doc.status === "Approved") {
            return ["Approved", "green", "status,=,Approved"];
        }
        if (doc.status === "Rejected") {
            return ["Rejected", "red", "status,=,Rejected"];
        }
        if (doc.status === "Pending Manager Approval") {
            return ["Pending Manager Approval", "orange", "status,=,Pending Manager Approval"];
        }

        return ["Draft", "gray"];
    },
};