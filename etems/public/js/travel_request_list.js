// frappe.listview_settings["Travel Request"] = {
//     add_fields: ["status"],
//     has_indicator_for_draft: true,
//     get_indicator: function (doc) {
//         let colour_map = {
//             "Pending Manager Approval": ["Pending Manager Approval", "Orange"],
//             // "Pending Finance Verification": ["Pending Finance Verification", "Pink"],
//             "Draft": ["Draft", "Yellow"],
//         };
//         return colour_map[doc.status];
//     }
// }