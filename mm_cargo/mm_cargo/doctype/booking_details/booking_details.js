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
		frm.fields_dict.custom_region.grid.get_field('agent_name').get_query = function(frm,cdt,cdn) {
			let child =locals[cdt][cdn]
			return {
				filters:{
					"partner_type":["=",child.agent_inhouse]
				}
			}
		}
		
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
	},
	imp_ex:function(frm){
		// frm.set_query("location",function(doc){
			if(frm.doc.imp_ex=="Import"){
				console.log("%%%%%%%%%%%%%%%%%%%%%%%%%55")
				frm.set_query("port_of_entry",function(doc){
					return{
						filters:{
							'import':1
						}
					}
				})
			}
			else{
				frm.set_query("port_of_exit",function(doc){
					return{
						filters:{
							'export':1
						}
					}
				})
			}
		// })
	}

});

frappe.ui.form.on('Booking Details Items', {
	length: function(frm,cdt,cdn){
		let child = locals[cdt][cdn];
		if(child.length < 0){
			frappe.msgprint("Could not accept negative values.");
			child.length = 0
		}
	},
	width: function(frm,cdt,cdn){
		let child = locals[cdt][cdn];
		if(child.width < 0){
			frappe.msgprint("Could not accept negative values.");
			child.width = 0
		}
	},
	height: function(frm,cdt,cdn){
		let child = locals[cdt][cdn];
		if(child.height < 0){
			frappe.msgprint("Could not accept negative values.");
			child.height = 0
		}
	},
	weight: function(frm,cdt,cdn){
		let child = locals[cdt][cdn];
		if(child.weight < 0){
			frappe.msgprint("Could not accept negative values.");
			child.weight = 0 
		}
	},
	numbers: function(frm,cdt,cdn){
		let child = locals[cdt][cdn];
		if(child.numbers < 0){
			frappe.msgprint("Could not accept negative values.");
			child.numbers = 0 
		}
	}
	
})