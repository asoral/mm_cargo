frappe.ui.form.on("Sales Order", {
    refresh:function(frm){
        frm.add_custom_button(__('Waybill'), function() {
            $.each(frm.doc.milestone_list,function(i,v){
                console.log("vvvvvvvvvvvvvvvvvv",v.milestone)
                frappe.new_doc('Waybill', {"delivery_customer": frm.doc.customer,"sales_order":frm.doc.name,"delivery_address_name":frm.doc.shipping_address_name}).then(function(r){
                    cur_frm.add_child("milestone_list",
                    {
                        "milestone":v.milestone,
                        "timestamp":v.timestamp
                    })
                    cur_frm.refresh_field("milestone_list")
                })
            })

            // r.refresh_fields()
            console.log("%%%%%%%%%%%%%%%%%%%%%",cur_frm.doc.milestone_list)

        }, __('Create'));
    }

});