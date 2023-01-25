# Copyright (c) 2022, dexciss and contributors
# For license information, please see license.txt

import frappe
from frappe import _, utils
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import flt

class Waybill(Document):
	def before_save(self):
		location=[]
		doc=frappe.get_doc("Sales Order",self.sales_order)
		for i in doc.milestone_list:
			if i.milestone not in location:
				location.append(i.milestone)
		location=set(location)
		self.milestone_list=[]
		for i in list(location):
			self.append("milestone_list",{
				"milestone":i
			})

	def before_submit(self):
		self.send_email()

	@frappe.whitelist()	
	def send_email(self):
	# def before_submit(self):	
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
		"message_to": self.delivery_contact_email,
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
		new_comm.recipients = self.delivery_contact_email
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
		

	@frappe.whitelist()
	def address(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Customer","link_name":self.pickup_customer,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Customer","link_name":self.pickup_customer,"parenttype":"Contact"},["parent"])
		print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",c_doc)
		list_adr=[]
		list_con=[]
		for c_ads in doc:
			list_adr.append(c_ads.parent)
		for c_con in c_doc:
			list_con.append(c_con.parent)
		return list_adr,list_con

	@frappe.whitelist()
	def d_address(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Customer","link_name":self.delivery_customer,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Customer","link_name":self.delivery_customer,"parenttype":"Contact"},["parent"])
		list_adr1=[]
		list_con1=[]
		for c_ads in doc:
			list_adr1.append(c_ads.parent)
		for c_con in c_doc:
			list_con1.append(c_con.parent)
		return list_adr1,list_con1

	
	@frappe.whitelist()
	def company_n(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Company","link_name":self.pickup_company,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Company","link_name":self.pickup_company,"parenttype":"Contact"},["parent"])
		list_adr2=[]
		list_con2=[]
		for c_ads in doc:
			list_adr2.append(c_ads.parent)
		for c_con in c_doc:
			list_con2.append(c_con.parent)
		return list_adr2,list_con2
	
	@frappe.whitelist()
	def company_n1(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Company","link_name":self.delivery_company,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Company","link_name":self.delivery_company,"parenttype":"Contact"},["parent"])
		list_adr3=[]
		list_con3=[]
		for c_ads in doc:
			list_adr3.append(c_ads.parent)
		for c_con in c_doc:
			list_con3.append(c_con.parent)
		return list_adr3,list_con3

	@frappe.whitelist()
	def supplier_n(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Supplier","link_name":self.pickup_supplier,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Supplier","link_name":self.pickup_supplier,"parenttype":"Contact"},["parent"])
		list_adr4=[]
		list_con4=[]
		for c_ads in doc:
			list_adr4.append(c_ads.parent)
		for c_con in c_doc:
			list_con4.append(c_con.parent)
		return list_adr4,list_con4
	
	@frappe.whitelist()
	def supplier_d(self):
		doc = frappe.get_all("Dynamic Link",{"link_doctype":"Supplier","link_name":self.delivery_supplier,"parenttype":"Address"},["parent"])
		c_doc = frappe.get_all("Dynamic Link",{"link_doctype":"Supplier","link_name":self.delivery_supplier,"parenttype":"Contact"},["parent"])
		list_adr5=[]
		list_con5=[]
		for c_ads in doc:
			list_adr5.append(c_ads.parent)
		for c_con in c_doc:
			list_con5.append(c_con.parent)
		return list_adr5,list_con5

	def before_update_after_submit(self):
		if (self.otp == self.verification_code):
			frappe.db.set_value("Delivery Stops",{"waybill":self.name,"parenttype":"MM Delivery Trip"},{
								"delivered":1
						})
			# pass
		else:
			frappe.throw("Please enter valide OTP")

	def notify(self, args):
		args = frappe._dict(args)
		outgoing = frappe.db.get_value("Email Account", {'enable_outgoing': 1, 'default_outgoing':1}, ['email_id'])
		print(" outgoing", outgoing)

		if not outgoing:
			frappe.msgprint(" Please add Email account with Enable Outgoing and Default Outgoing")

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

