frappe.ui.form.on("Sales Order", {
    refresh:function(frm){

        frm.add_custom_button(__('Waybill'), function() {

                frappe.new_doc('Waybill', {"delivery_customer": frm.doc.customer,"sales_order":frm.doc.name,"pickup_address_name":frm.doc.company_address,"delivery_address_name":frm.doc.customer_address,"delivery_contact_name":frm.doc.contact_person,"booking_details":frm.doc.booking_details}).then(function(r){
                    // let k = frappe.get_doc("")
                    $.each(frm.doc.milestone_list,function(i,v){
                    cur_frm.add_child("milestone_list",
                    {
                        "milestone":v.milestone,
                        "timestamp":v.timestamp
                    })
                })
                $.each(frm.doc.booking_items,function(i,v){
                    cur_frm.add_child("booking_items",
                    {
                        "length":v.length,
                        "width":v.width,
                        "height":v.height,
                        "weight":v.weight,
                        "numbers":v.numbers,
                        "vw":v.vw,
                        "aw":v.aw,
                        "cargo":v.cargo,
                        "cargo_properties":v.cargo_properties,
                        "state_of_cargo":v.state_of_cargo
                    })
                    cur_frm.refresh_field("booking_items")
                    cur_frm.refresh_field("milestone_list")
                    cur_frm.refresh_field("delivery_address_name")
                })
            })
        }, __('Create'));
    }

});