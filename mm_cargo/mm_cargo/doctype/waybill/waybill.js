// Copyright (c) 2022, dexciss and contributors
// For license information, please see license.txt

frappe.ui.form.on('Waybill', {
	refresh: function(frm) {
		frappe.call({
			method: "get_locations",
			doc:frm.doc,
			callback: (data) => {
				console.log("&&&&&&&&&&&&&&&&&&&777",data.message)
				frm.set_df_property('delivery_milestone', 'options', data.message);
				frm.refresh_field("delivery_milestone")
			}
		});
	}
});
