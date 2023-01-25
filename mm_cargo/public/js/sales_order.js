frappe.ui.form.on("Sales Order", {
    refresh:function(frm){

        frm.add_custom_button(__('Waybill'), function() {
                frappe.new_doc('Waybill', {"delivery_customer": frm.doc.customer,"sales_order":frm.doc.name}).then(function(r){
                    $.each(frm.doc.milestone_list,function(i,v){
                    cur_frm.add_child("milestone_list",
                    {
                        "milestone":v.milestone,
                        "timestamp":v.timestamp
                    })
                    cur_frm.refresh_field("milestone_list")
                })
            })
        }, __('Create'));
    }

});