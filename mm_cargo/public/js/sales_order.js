frappe.ui.form.on("Sales Order", {
    refresh:function(frm){
        frm.add_custom_button(__('Waybill'), function() {
                

            frappe.new_doc('Waybill', {"delivery_customer": frm.doc.customer,"sales_order":frm.doc.name,"delivery_address_name":frm.doc.shipping_address_name});

        }, __('Create'));
    }

});