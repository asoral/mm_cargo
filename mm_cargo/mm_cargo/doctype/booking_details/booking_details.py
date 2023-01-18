# Copyright (c) 2022, dexciss and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt

class BookingDetails(Document):
	@frappe.whitelist()
	def make_quotation(self):
		location=[]
		quo=frappe.get_value("Quotation",{"booking_details":self.name},["name"])
		if not quo:
			transport=frappe.get_doc("Transport Setting")
			if self.shipment_type=="Dedicated":
				price=[]
				local_rate=[]
				# location.append(self.origin_point)
				# location.append(self.destination)
				if self.port_of_exit:
					location.append(self.port_of_exit)
				if self.port_of_entry:
					location.append(self.port_of_entry)
				doc=frappe.new_doc("Quotation")

				for i in self.mmcs_transport:
					doc.append("mmcs_transport",{
						"origin_point":i.origin_point,
						"destination_point":i.destination_point,
						"vehicle_type":i.vehicle_type
					})
					location.append(i.origin_point)
					location.append(i.destination_point)
					doc1=frappe.get_value("Pricing Matrix",{"source":i.origin_point,"dest":i.destination_point,"vehicle_type":i.vehicle_type},["price"])
					price.append(flt(doc1))
					if self.need_pickup:
						local_rate1=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["local_rate"])
						local_rate.append(local_rate1)
				doc.booking_details=self.name
				doc.quotation_to=self.party
				doc.party_name=self.party_name
				doc.order_type="Sales"
			
				doc.append("items",{
					"item_code":transport.mmcs,
					"qty":1,
					"rate":sum(price)
				})
				if self.need_pickup:
					doc.append("items",{
						"item_code":transport.lt,
						"qty":1,
						"rate":sum(local_rate)*flt(self.kms)
					})
				
				if self.custom_clearing_required:
					cc=[]
					for j in self.custom_region:
						location.append(j.location)
						cc.append(j.amount)
						doc.append("custom_region",{
							"location":j.location,
							"agent_inhouse":j.agent_inhouse,
							"agent_name":loc.name,
							"amount":j.amount
						})
					doc.append("items",{
						"item_code":transport.cc,
						"qty":1,
						"rate":sum(cc)
					})
					
				if self.special_packaging:
					doc.append("items",{
						"item_code":transport.sp,
						"qty":1,
						"rate":self.packaging_charges1
					})

				for k in self.booking_items:
					doc.append("booking_items",{
						"length":k.length,
						"width":k.width,
						"height":k.height,
						"weight":k.weight,
						"numbers":k.numbers,
						"vw":k.vw,
						"aw":k.aw
					})
				if self.permits_required:
					pp=[]
					for i in self.permits_details:
						pp.append(i.charges)
						doc.append("permits_details",{
							"permit_type":i.permit_type,
							"desription":i.desription,
							"charges":i.charges
						})
					doc.append("items",{
						"item_code":transport.pc,
						"qty":1,
						"rate":sum(pp)
					})
				for lo in location:
					doc.append("milestone_list",{
						"milestone":lo
					})
				doc.save(ignore_permissions=True)
				frappe.msgprint("Quotation Created")
			if self.shipment_type=="Consolidated":
				price=[]
				local_rate=[]
				volume=[]
				actual=[]
				capacity=[]
				# location.append(self.origin_point)
				# location.append(self.destination)
				if self.port_of_exit:
					location.append(self.port_of_exit)
				if self.port_of_entry:
					location.append(self.port_of_entry)
				for i in self.mmcs_transport:
					location.append(i.origin_point)
					location.append(i.destination_point)
					doc1=frappe.get_value("Pricing Matrix",{"source":i.origin_point,"dest":i.destination_point,"vehicle_type":i.vehicle_type},["price"])
					price.append(doc1)
					print("YYYYYYYYYYYYYYYYYYY",price)
					if self.need_pickup:
						local_rate1=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["local_rate"])
						local_rate.append(local_rate1)
						capacity1=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["capacity"])
						capacity.append(capacity1)
				doc=frappe.new_doc("Quotation")
				doc.booking_details=self.name
				doc.quotation_to=self.party
				doc.party_name=self.party_name
				doc.order_type="Sales"
				for i in self.booking_items:
					vw=i.length* i.width * i.height * i.numbers*333.33/1000000
					volume.append(vw)
					aw=i.weight *i.numbers
					actual.append(aw)
					i.vw=vw
					i.aw=aw
				high=0
				if sum(volume) and sum(actual):
					high=max(sum(volume),sum(actual))
				print("TTTTTTTTTTTT",price,capacity)
				doc.append("items",{
					"item_code":transport.mmcs,
					"qty":high,
					"rate":(sum(price))/(sum(capacity))
				})
				
				if self.need_pickup:
					doc.append("items",{
						"item_code":transport.lt,
						"qty":1,
						"rate":sum(local_rate)*flt(self.kms)
					})
				
				if self.custom_clearing_required:
					cc=[]
					for j in self.custom_region:
						location.append(j.location)
						cc.append(j.amount)
					doc.append("items",{
						"item_code":transport.cc,
						"qty":1,
						"rate":sum(cc)
					})
				# for kl in self.booking_details:
				# 	doc.append({
				# 		"":"",
				# 		"":""
				# 	})
				if self.special_packaging:
					doc.append("items",{
						"item_code":transport.sp,
						"qty":1,
						"rate":self.packaging_charges1
					})

				if self.permits_required:
					pp=[]
					for i in self.permits_details:
						pp.append(i.charges)
					doc.append("items",{

						"item_code":transport.pc,
						"qty":1,
						"rate":sum(pp)
					})
				for lo in location:
					doc.append("milestone_list",{
						"milestone":lo
					})
				doc.save(ignore_permissions=True)
				frappe.msgprint("Quotation Created")
		else:
			frappe.msgprint("Quotation Already Created For This Document")

	def before_save(self):
		for i in self.mmcs_transport:
			vh = frappe.get_doc("Vehicle Type",{'name':i.vehicle_type})
			for j in self.booking_items:
				if j.cargo_properties == "Non-Stackable":
					j.height=vh.height
				value_vw =((j.length * j.height * j.width)/5000)
				j.vw=value_vw	
				j.aw = j.numbers * j.weight	

	@frappe.whitelist()
	def address_(self):
		list_add=[]
		pick_add = frappe.db.get_all("Address")
		for a in pick_add:
			add_c = frappe.get_doc("Address",{'name':a.name})
			for add_l in add_c.links:
				if add_l.link_name == self.party_name:
					list_add.append(add_c.name)
		return list_add
	
		
			