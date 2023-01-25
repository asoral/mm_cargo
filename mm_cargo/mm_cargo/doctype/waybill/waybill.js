// Copyright (c) 2022, dexciss and contributors
// For license information, please see license.txt

frappe.ui.form.on('Waybill', {
	refresh: function(frm) {
		// frappe.call({
		// 	method: "get_locations",
		// 	doc:frm.doc,
		// 	callback: (data) => {
		// 		// console.log("&&&&&&&&&&&&&&&&&&&777",data.message)
		// 		// frm.set_df_property('delivery_milestone', 'options', data.message);
		// 		// frm.refresh_field("delivery_milestone")
		// 	}
		// });
		console.log("uuuuuuuuuuuuuuuuuuuuuuuuuuu",frm.doc.docstatus)
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__('Sent Mail'), function() {
				frappe.call({
					method:"send_email",
					doc:frm.doc
				})
			},);
		}
	
	},
	pickup_customer: function(frm) {
		frappe.call({
			method:"address",
			doc:frm.doc,
			callback:function(r){
				console.log("*******************************",r.message[1])
					frm.set_query("pickup_address_name", function() {
						return {
							filters: [
								["name" , "in" , r.message[0]]
							]
						}
					});		
					frm.set_query("pickup_contact_name", function() {
						return {
							filters: [
								["name" , "in" , r.message[1]]
							]
						}
					});				
			}
		})
	},
	delivery_customer:function(frm){
		frappe.call({
			method:"d_address",
			doc:frm.doc,
			callback:function(r){
				frm.set_query("delivery_address_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[0]]
						]
					}
				});
				frm.set_query("delivery_contact_name", function() {
					console.log("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPp",r.message[1])
					return {
						filters: [
							["name" , "in" , r.message[1]]
						]
					}
				});	
			}
		})
	},
	pickup_company:function(frm){
		frappe.call({
			method:"company_n",
			doc:frm.doc,
			callback:function(r){
				frm.set_query("pickup_address_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[0]]
						]
					}
				});	
				frm.set_query("pickup_contact_person", function() {
					return {
						filters: [
							["name" , "in" , r.message[1]]
						]
					}
				});	
			}
		})
	},
	delivery_company:function(frm){
		frappe.call({
			method:"company_n1",
			doc:frm.doc,
			callback:function(r){
				frm.set_query("delivery_address_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[0]]
						]
					}
				});	
				frm.set_query("delivery_contact_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[1]]
						]
					}
				});	
			}
		})
	},
	pickup_supplier:function(frm){
		frappe.call({
			method:"supplier_n",
			doc:frm.doc,
			callback:function(r){
				frm.set_query("pickup_address_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[0]]
						]
					}
				});	
				frm.set_query("pickup_contact_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[1]]
						]
					}
				});
			}
		})
	},
	delivery_supplier:function(frm){
		frappe.call({
			method:"supplier_d",
			doc:frm.doc,
			callback:function(r){
				frm.set_query("delivery_address_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[0]]
						]
					}
				});	
				frm.set_query("delivery_contact_name", function() {
					return {
						filters: [
							["name" , "in" , r.message[1]]
						]
					}
				});	
			}
		})
	},
});
