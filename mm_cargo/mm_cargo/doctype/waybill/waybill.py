# Copyright (c) 2022, dexciss and contributors
# For license information, please see license.txt

import frappe
from frappe import _, utils
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import flt

class Waybill(Document):
	@frappe.whitelist()
	def get_locations(self):
		location=[]
		if self.sales_order:
			doc=frappe.get_doc("Sales Order",self.sales_order)
			for i in doc.milestone_list:
				location.append(i.milestone)
			return location
                
	def before_submit(self):
		doc=frappe.get_doc("Address",self.delivery_address_name)
		d=frappe.get_doc('User', frappe.session.user)
		# emails = []
		# for e in email_id:
		# 	emails.append(e.get('email_id'))
		msg="<div> Dear <b> {0}</b> <br>".format(d.first_name)
		import random

		a=random.randint(0,9999)
		msg+="""Here is a one-time verification code for your use. This code ensures that ewaybill {1} Generated against Sales Order {2} .<br><br>

			Your verification code is: {0}<br>

			This is a system-generated email, please do not reply.""".format(a,self.name,a)
		
		self.notify({
		# for post in messages
		# "message": message,
		"message": msg,
		"message_to": doc.email_id,
		# for email
		"subject":"Waybill OTP",
		
		})
		self.verification_code=flt(a)
		outgoing = frappe.db.get_value("Email Account", {'enable_outgoing': 1, 'default_outgoing':1}, ['email_id'])


		# message = frappe.render_template(email_template.response, args)
		new_comm = frappe.new_doc("Communication")
		
		new_comm.subject = "Waybill OTP"
		new_comm.communication_medium = "Email"
		new_comm.sender = outgoing
		new_comm.recipients = doc.email_id
		# new_comm.content = message
		new_comm.content = msg
		new_comm.communication_type	= "Communication"
		new_comm.status = "Linked"
		new_comm.sent_or_received = "Sent"      
		new_comm.communication_date	= str(utils.today())
		new_comm.sender_full_name = frappe.session.user_fullname
		new_comm.reference_doctype = "Waybill"
		new_comm.reference_name = self.name
		new_comm.reference_owner = self.name
		new_comm.save(ignore_permissions=True)	
	
 

	def notify(self, args):
		args = frappe._dict(args)
		outgoing = frappe.db.get_value("Email Account", {'enable_outgoing': 1, 'default_outgoing':1}, ['email_id'])
		print(" outgoing", outgoing)

		if not outgoing:
			frappe.throw(" Please add Email account with Eable Outgoing and Default Outgoing")

		sender      	    = dict()
		sender['email']     = outgoing 
		sender['full_name'] = "MM Cargo"
		try:
			frappe.sendmail(
				recipients = args.message_to,
				sender = sender['email'],
				subject = args.subject,
				message = args.message,
			)
			frappe.msgprint(_("Email sent to {0}").format(args.message_to))
		except frappe.OutgoingEmailError:
			pass	




@frappe.whitelist()
def make_waybill(source_name, target_doc="Delivery Stops"):
	def update_stop_details(source_doc, target_doc,source_parent):
		print("888888888888888888",target_doc.doctype)
		target_doc.customer = source_parent.delivery_customer
		target_doc.address = source_parent.delivery_address_name
		if source_parent.sales_order:
			doc=frappe.get_doc("Sales Order",source_parent.sales_order)
			target_doc.customer_address = doc.shipping_address
			target_doc.contact = doc.contact_person
			target_doc.customer_contact = doc.contact_display
			target_doc.grand_total = doc.grand_total

		# Append unique Delivery Notes in Delivery Trip
		waybills.append(source_doc.name)

	waybills = []

	doclist = get_mapped_doc(
		"Waybill",
		source_name,
		{
			"Waybill": {"doctype": "MM Delivery Trip", "validation": {"docstatus": ["=", 1]}},
			"Box Details": {
				"doctype": "Delivery Stops",
				"field_map": {"parent": "waybill"},
				"condition": lambda item: item.name not in waybills,
				"postprocess": update_stop_details
			},
		},
		target_doc,
	)
	return doclist