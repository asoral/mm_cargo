frappe.ui.form.on("Sales Order", {
    refresh:function(frm){
        frm.add_custom_button(__('Waybill'), function() {
            $.each(frm.doc.milestone_list,function(i,v){
                let list_w = []

                list_w.push(v.milestone)
                
                console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",list_w)
                frappe.new_doc('Waybill', {"delivery_customer": frm.doc.customer,"sales_order":frm.doc.name,"delivery_address_name":frm.doc.shipping_address_name}).then(function(r){
                    // console.log("%%%%%%%%%%%%%%%%%%%%%")
                    cur_frm.add_child("milestone_list",
                    {
                        "milestone":v.milestone,
                        "timestamp":v.timestamp
                    })

                    cur_frm.refresh_field("milestone_list")
                    // console.log("RRRRRRRRRRRRRRRRRRRRRRRR",)
                })
            })

            // r.refresh_fields()
            // console.log("%%%%%%%%%%%%%%%%%%%%%",cur_frm.doc.milestone_list)

        }, __('Create'));
    }

});