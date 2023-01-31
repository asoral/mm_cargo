// Copyright (c) 2022, dexciss and contributors
// For license information, please see license.txt

frappe.ui.form.on('MM Delivery Trip', {
	// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
	// refresh:function(frm){
	// 	if(frm.doc.docstatus==1){
	// 		frm.set_df_property("status_milestones","hidden",0);
	// 	}

	// },

	setup: function (frm) {
		frm.set_indicator_formatter('customer', (stop) => (stop.visited) ? "green" : "orange");

		frm.set_query("driver", function () {
			return {
				filters: {
					"status": "Active"
				}
			};
		});

		frm.set_query("address", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: 'frappe.contacts.doctype.address.address.address_query',
					filters: {
						link_doctype: "Customer",
						link_name: row.customer
					}
				};
			}
		})

		frm.set_query("contact", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: 'frappe.contacts.doctype.contact.contact.contact_query',
					filters: {
						link_doctype: "Customer",
						link_name: row.customer
					}
				};
			}
		})

			
		frm.fields_dict.delivery_stops.grid.get_field('waybill').get_query = function(frm,cdt,cdn) {
			let child =locals[cdt][cdn]
			return {
				filters:{
					"docstatus":["=",1]
				}
			}
		}



		frm.set_query("template", function () {
			return {
				filters: {
					"docstatus":["=",1]
				}
			};
		});

		// if(!frm.doc.__islocal){
		// 	frappe.call({
		// 		method:"list_m",
		// 		doc:frm.doc,
		// 		callback:function(r){
		// 			frm.set_df_property("milestone", "options", r.message);
		// 		}
		// 	})
	
		// }

		// frappe.call({
		// 	method:"list_m",
		// 	doc:frm.doc,
		// 	callback:function(r){
		// 		frm.set_df_property("milestone", "options", r.message);
		// 	}
		// })

	},
	// milestone:function(frm){
	// 	if(!frm.doc.__islocal){
	// 		frappe.call({
	// 			method:"list_m",
	// 			doc:frm.doc,
	// 			callback:function(r){
	// 				frm.set_df_property("milestone", "options", r.message);
	// 			}
	// 		})
	
	// 	}
	// },
	
	refresh: function (frm) {

		// frm.set_query("milestone", function () {
		// 	return {
		// 		filters: {
		// 			"name": ["in",r.message]
		// 		}
		// 	};
		// });



		// $.each(frm.doc.delivery_stops,function(i,v){
		// 	console.log("YYYYYYYYYYYYYYYYYYYYyy",v.waybill)
		
			
		// 	// $.each(mil_list.milestone_list,function(j,k){
		// 	// 	console.log("UUUUUUUUUUUUUUUUUUUUUUUUUu",k.milestone)
		// 	// })
		// })
		
		if(!frm.doc.__islocal){
			frappe.call({
				method:"list_m",
				doc:frm.doc,
				callback:function(r){
					frm.set_df_property("milestone", "options", r.message);
				}
			})
	
		}
		

		if (frm.doc.docstatus == 1 && frm.doc.employee) {
			frm.add_custom_button(__('Expense Claim'), function() {
				frappe.model.open_mapped_doc({
					method: 'erpnext.stock.doctype.delivery_trip.delivery_trip.make_expense_claim',
					frm: cur_frm,
				});
			}, __("Create"));
		}

		if (frm.doc.docstatus == 1 && frm.doc.delivery_stops.length > 0) {
			frm.add_custom_button(__("Notify Customers via Email"), function () {
				frm.trigger('notify_customers');
			});
		}

		if(frm.doc.inspection_required == 1) {
			  frm.add_custom_button(__('Create Inspection'), function(){
				frappe.db.get_doc('Inspection Template',frm.doc.template).then(tmp => {
					console.log("**************************",)
					if(tmp.item_inspection_parameter){
						console.log('AAAAAAAAAAAAAA')
						frappe.new_doc('Inspection', {"driver": frm.doc.driver,"vehicle":frm.doc.vehicle}).then(function(r){
						$.each(tmp.item_inspection_parameter,function(i,v){
							cur_frm.add_child("parameter",
							{
								"parameter":v.parameter,
								
							})
							cur_frm.refresh_field("parameter")
                
							console.log('vvvvvvvvvvvvvvvvvvvv',v.parameter)
						})
					}, __("Create"));
				}
				
				})
			})
				
		  }

		// if (frm.doc.docstatus === 0) {
		// 	frm.add_custom_button(__('Waybill'), () => {
		// 		erpnext.utils.map_current_doc({
		// 			method: "mm_cargo.mm_cargo.doctype.waybill.waybill.make_waybill",
		// 			source_doctype: "Waybill",
		// 			target: frm,
		// 			date_field: "posting_date",
		// 			setters: {
		// 				company: frm.doc.company,
		// 			},
		// 			get_query_filters: {
		// 				docstatus: 1,
		// 				company: frm.doc.company,
		// 			}
		// 		})
		// 	}, __("Get customers from"));
		// }
	},

	calculate_arrival_time: function (frm) {
		if (!frm.doc.driver_address) {
			frappe.throw(__("Cannot Calculate Arrival Time as Driver Address is Missing."));
		}
		frappe.show_alert({
			message: "Calculating Arrival Times",
			indicator: 'orange'
		});
		frm.call("process_route", {
			optimize: false,
		}, () => {
			frm.reload_doc();
		});
	},

	driver: function (frm) {
		if (frm.doc.driver) {
			frappe.call({
				method: "erpnext.stock.doctype.delivery_trip.delivery_trip.get_driver_email",
				args: {
					driver: frm.doc.driver
				},
				callback: (data) => {
					frm.set_value("driver_email", data.message.email);
				}
			});
		};
	},

	optimize_route: function (frm) {
		if (!frm.doc.driver_address) {
			frappe.throw(__("Cannot Optimize Route as Driver Address is Missing."));
		}
		frappe.show_alert({
			message: "Optimizing Route",
			indicator: 'orange'
		});
		frm.call("process_route", {
			optimize: true,
		}, () => {
			frm.reload_doc();
		});
	},

	notify_customers: function (frm) {
		$.each(frm.doc.delivery_stops || [], function (i, delivery_stop) {
			if (!delivery_stop.delivery_note) {
				frappe.msgprint({
					"message": __("No Delivery Note selected for Customer {}", [delivery_stop.customer]),
					"title": __("Warning"),
					"indicator": "orange",
					"alert": 1
				});
			}
		});

		frappe.db.get_value("Delivery Settings", { name: "Delivery Settings" }, "dispatch_template", (r) => {
			if (!r.dispatch_template) {
				frappe.throw(__("Missing email template for dispatch. Please set one in Delivery Settings."));
			} else {
				frappe.confirm(__("Do you want to notify all the customers by email?"), function () {
					frappe.call({
						method: "erpnext.stock.doctype.delivery_trip.delivery_trip.notify_customers",
						args: {
							"delivery_trip": frm.doc.name
						},
						callback: function (r) {
							if (!r.exc) {
								frm.doc.email_notification_sent = true;
								frm.refresh_field('email_notification_sent');
							}
						}
					});
				});
			}
		});
	}
});

frappe.ui.form.on('Delivery Stops', {
	waybill:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		frappe.call({
			method:"wb_list",
			doc:frm.doc,
			callback:function(r){
				
				
				// console.log("@@@@@@@@@@@@@@@@@@@@@@2",r.message)
			}
		})
	},
	customer: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.customer) {
			frappe.call({
				method: "erpnext.stock.doctype.delivery_trip.delivery_trip.get_contact_and_address",
				args: { "name": row.customer },
				callback: function (r) {
					if (r.message) {
						if (r.message["shipping_address"]) {
							frappe.model.set_value(cdt, cdn, "address", r.message["shipping_address"].parent);
						}
						else {
							frappe.model.set_value(cdt, cdn, "address", '');
						}
						if (r.message["contact_person"]) {
							frappe.model.set_value(cdt, cdn, "contact", r.message["contact_person"].parent);
						}
						else {
							frappe.model.set_value(cdt, cdn, "contact", '');
						}
					}
					else {
						frappe.model.set_value(cdt, cdn, "address", '');
						frappe.model.set_value(cdt, cdn, "contact", '');
					}
				}
			});
		}
	},

	address: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.address) {
			frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: { "address_dict": row.address },
				callback: function (r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, "customer_address", r.message);
					}
				}
			});
		} else {
			frappe.model.set_value(cdt, cdn, "customer_address", "");
		}
	},

	contact: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.contact) {
			frappe.call({
				method: "erpnext.stock.doctype.delivery_trip.delivery_trip.get_contact_display",
				args: { "contact": row.contact },
				callback: function (r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, "customer_contact", r.message);
					}
				}
			});
		} else {
			frappe.model.set_value(cdt, cdn, "customer_contact", "");
		}
	},


});

