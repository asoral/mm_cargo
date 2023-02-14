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
                    cur_frm.refresh_field("milestone_list")
                    cur_frm.refresh_field("delivery_address_name")
                })
            })
        }, __('Create'));
    }

});