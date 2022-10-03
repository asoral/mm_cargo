// Copyright (c) 2022, dexciss and contributors
// For license information, please see license.txt

frappe.ui.form.on('Booking Details', {
	setup: function(frm) {
		frm.set_query("party", function() {
			return{
				"filters": {
					"name": ["in", ["Customer", "Lead"]],
				}
			}
		});
	},
	refresh: function(frm) {
		if(frm.doc.docstatus==1){
			frm.add_custom_button(__('Create Quotation'), function() {
				frappe.call({
					method :'make_quotation',
					doc:frm.doc,
					
					callback: function(r)
					{
					}
				});
			})
		}
	}

});
