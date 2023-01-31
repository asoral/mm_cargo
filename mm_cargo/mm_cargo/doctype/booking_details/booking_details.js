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
		
		frappe.call({
			method:"c_charge",
			doc:frm.doc,
			callback:function(r){
				console.log("YYYYYYYYYYYYYYYYYYYYYYYy",r.message)
				frm.set_value("charges_type",r.message)
				frm.refresh_fields("charges_type")
			}
		})
		
		// cur_frm.fields_dict['charges_type'].grid.get_field('exchange_rate').get_query = function(doc, cdt, cdn) {
		// 	return {
				
		// 	}
		// }

	},


	conversion_currency:function(frm){
		console.log("HHHHHHHHHHHHHHHHHHHHHhh0",frm.doc.conversion_currency)
		let base_currency = frappe.defaults.get_global_default('currency');
		if (base_currency != frm.doc.conversion_currency) {
			frappe.call({
				method: "erpnext.setup.utils.get_exchange_rate",
				args: {
					  from_currency: frm.doc.conversion_currency,
					  to_currency: base_currency
				},
				callback: function(r) {
					frm.doc.exchange_rate = r.message
				}
		  });
		}
		else{
			frappe.call({
				method: "erpnext.setup.utils.get_exchange_rate",
				args: {
					  from_currency: frm.doc.conversion_currency,
					  to_currency: base_currency
				},
				callback: function(r) {
					frm.doc.exchange_rate = r.message
				}
		  });
		}
	   
	},
	
	// before_save:function(frm){
		// frappe.call({
		// 	method:"c_charge",
		// 	doc:frm.doc,
		// 	callback:function(r){
		// 		console.log("YYYYYYYYYYYYYYYYYYYYYYYYYYYYY",r.message)
		// 	}
		// })
	// },
	party_name:function(frm){
				frappe.call({
				method:"address_",
				doc:frm.doc,
				callback:function(r){
					console.log("%%%%%%%%%%%%%%%%%%%%%%%%%%%%",r.message)
					// frm.doc.pickup_address = r.message
					frm.set_query("pickup_address", function() {
						return{
							"filters": {
								"name": ["in", r.message],
							}
						}
					});
				}
	
			})
		
	},
	refresh: function(frm) {
		
		// frm.fields_dict.custom_region.grid.get_field('agent_name').get_query = function(frm,cdt,cdn) {
		// 	let child =locals[cdt][cdn]
		// 	return {
		// 		filters:{
		// 			"partner_type":["=",child.agent_inhouse]
		// 		}
		// 	}
		// }


		
		// frappe.call({
		// 	method:"c_charge",
		// 	doc:frm.doc,
		// 	callback:function(r){
		// 		console.log("YYYYYYYYYYYYYYYYYYYYYYYy",r.message)
		// 		frm.set_value("charges_type",r.message)
		// 		frm.refresh_fields("charges_type")
		// 	}
		// })


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

		frm.fields_dict.custom_region.grid.get_field('agent_name').get_query = function(frm,cdt,cdn) {
			let child =locals[cdt][cdn]
			return {
				filters:{
					"partner_type":["=",child.agent_inhouse]
				}
			}
		}

		frm.fields_dict.mmcs_transport.grid.get_field("origin_point").get_query = function(frm,cdt,cdn){
			let child =locals[cdt][cdn]
			return {
				filters:{
					"import" : 0,
					"export" : 0
			}
			}
		}

		frm.fields_dict.mmcs_transport.grid.get_field("destination_point").get_query = function(frm,cdt,cdn){
			let child =locals[cdt][cdn]
			return {
				filters:{
					"import" : 0,
					"export" : 0
			}
			}
		}

		frm.fields_dict.custom_region.grid.get_field("location").get_query = function(frm,cdt,cdn){
			let child =locals[cdt][cdn]
			return {
				filters:{
					"import" : 0,
					"export" : 0
			}
			}
		}

		frappe.call({
			method:"item_list",
			doc:frm.doc,
			callback:function(r){
				frm.fields_dict.custom_region.grid.get_field('item').get_query = function(frm,cdt,cdn) {
					let child =locals[cdt][cdn]
					return {
						filters:{
							"name":["in",r.message]
						}
					}
				}
			}
		})
		
	},
	// pickup_address(frm){
	// 	// if(frm.doc.customer){
	// 		// frm.set_query("pickup_address", function() {
	// 		// 	return{
	// 		// 		"filters": {
	// 		// 			"": ["in", ["Customer", "Lead"]],
	// 		// 		}
	// 		// 	}
	// 		// });
	// 		frappe.call({
	// 			method:"address_",
	// 			doc:frm.doc,
	// 			callback:function(r){
	// 				console.log("%%%%%%%%%%%%%%%%%%%%%%%%%%%%",r.message)

	// 			}

	// 		})
	// 	// }
		
	// },
	imp_ex:function(frm){
		// frm.set_query("location",function(doc){
			if(frm.doc.imp_ex=="Import"){
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

// frappe.ui.form.on('Charges Type Table',{
	// conversion_currency:function(frm,cdt,cdn){
	// 	let child = locals[cdt][cdn]
	// 	let base_currency = frappe.defaults.get_global_default('currency');
	// 	if (base_currency != child.conversion_currency) {
	// 		frappe.call({
	// 			method: "erpnext.setup.utils.get_exchange_rate",
	// 			args: {
	// 				  from_currency: child.conversion_currency,
	// 				  to_currency: base_currency
	// 			},
	// 			callback: function(r) {
	// 				child.exchange_rate = r.message
	// 			}
	// 	  });
	// 	}
	// 	else{
	// 		frappe.call({
	// 			method: "erpnext.setup.utils.get_exchange_rate",
	// 			args: {
	// 				  from_currency: child.conversion_currency,
	// 				  to_currency: base_currency
	// 			},
	// 			callback: function(r) {
	// 				child.exchange_rate = r.message
	// 			}
	// 	  });
	// 	}
	   
	// }
// });


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
	},
	
});

// frappe.ui.form.on("Inhouse Transport Services",{
// 	refresh:function(frm,cdt,cdn){
// 		let child = locals[cdt][cdn];
// 		frm.set_query("origin_point", function() {
// 			return{
// 				"filters": {
// 					"name": ["not in", r.message],
// 				}
// 			}
// 		});
// 	}

// })