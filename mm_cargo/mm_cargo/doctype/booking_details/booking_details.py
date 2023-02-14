# Copyright (c) 2022, dexciss and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt
from erpnext.setup.utils import get_exchange_rate

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
						"vehicle_type":i.vehicle_type,
						"additional_charge":i.additional_charge,
						"additional_trailer":i.additional_trailer
					})
					location.append(i.origin_point)
					location.append(i.destination_point)
					doc1=frappe.get_value("Pricing Matrix",{"source":i.origin_point,"dest":i.destination_point,"vehicle_type":i.vehicle_type},["price"])
					price.append(flt(doc1)*flt(self.multiplier_factor))
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
							"item":j.item,
							"agent_name":j.agent_name,
							"amount":j.amount
						})
						doc.append("items",{
							"item_code":j.item,
							"qty":1,
							"description":"Agent Name : {0}".format(j.agent_name),
							"rate":j.amount
						})
					
				if self.special_packaging:
					doc.append("items",{
						"item_code":transport.sp,
						"qty":1,
						"description":self.special_packaging_description,
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
						"aw":k.aw,
						"cargo":k.cargo,
						"cargo_properties":k.cargo_properties,
						"state_of_cargo":k.state_of_cargo
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
						"description":i.desription,
						"rate":sum(pp)
					})
				for lo in location:
					doc.append("milestone_list",{
						"milestone":lo
					})
				for i in self.mmcs_transport:
					if i.additional_charge:
						doc.append("items",{
							"item_code":transport.mmcs,
							"qty":1,
							"description":"Additional Trailer {0}".format(i.additional_trailer),
							"rate":i.additional_charge
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
				doc=frappe.new_doc("Quotation")	
				for i in self.mmcs_transport:
									# for i in self.mmcs_transport:
					doc.append("mmcs_transport",{
						"origin_point":i.origin_point,
						"destination_point":i.destination_point,
						"vehicle_type":i.vehicle_type,
						"additional_charge":i.additional_charge,
						"additional_trailer":i.additional_trailer
					})
					location.append(i.origin_point)
					location.append(i.destination_point)
					doc1=frappe.get_value("Pricing Matrix",{"source":i.origin_point,"dest":i.destination_point,"vehicle_type":i.vehicle_type},["price"])
					price.append(flt(doc1))
					# if self.need_pickup:
					local_rate1=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["local_rate"])
					local_rate.append(local_rate1)
					capacity1=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["capacity"])
					capacity.append(capacity1)
				# doc=frappe.new_doc("Quotation")
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
				for i in self.mmcs_transport:
					if i.additional_charge:
						doc.append("items",{
							"item_code":transport.mmcs,
							"qty":1,
							"description":"Additional Trailer {0}".format(i.additional_trailer),
							"rate":i.additional_charge
						})
				if self.need_pickup:
					doc.append("items",{
						"item_code":transport.lt,
						"qty":1,
						"rate":sum(local_rate)*flt(self.kms)
					})
				
				for k in self.booking_items:
					doc.append("booking_items",{
						"length":k.length,
						"width":k.width,
						"height":k.height,
						"weight":k.weight,
						"numbers":k.numbers,
						"vw":k.vw,
						"aw":k.aw,
						"cargo":k.cargo,
						"cargo_properties":k.cargo_properties,
						"state_of_cargo":k.state_of_cargo
					})
				
				if self.custom_clearing_required:
					cc=[]
					for j in self.custom_region:
						location.append(j.location)
						cc.append(j.amount)
						doc.append("custom_region",{
							"location":j.location,
							"agent_inhouse":j.agent_inhouse,
							"item":j.item,
							"agent_name":j.agent_name,
							"amount":j.amount
						})
						doc.append("items",{
							"item_code":j.item,
							"qty":1,
							"description":"Agent Name : {0}".format(j.agent_name),
							"rate":j.amount
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
						"description":self.special_packaging_description,
						"rate":self.packaging_charges1
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
						# pp.append(i.charges)
					doc.append("items",{

						"item_code":transport.pc,
						"qty":1,
						"description":i.desription,
						"rate":sum(pp)
					})
				for lo in location:
					doc.append("milestone_list",{
						"milestone":lo
					})

				# for add_c in self.mmcs_transport:
				

				doc.save(ignore_permissions=True)
				frappe.msgprint("Quotation Created")
		else:
			frappe.msgprint("Quotation Already Created For This Document")

	@frappe.whitelist()
	def c_charge(self):
		ch_ty = frappe.db.sql("""select name from `tabCharges Type` where docstatus=0 and active=1 order by id asc """,as_dict=1)
		print(ch_ty)
		# frappe.db.get_list("Charges Type",filters={"docstatus":0},fields=["*"],'index asc')
		for k in ch_ty:
			i = frappe.get_doc("Charges Type",{"name":k.name})
			self.append("charges_type",{
				"charges_type":k.name,
				"abbr":i.abbr,
				"percentage":i.percentage,
				"formula":i.formula
			})
		
		# return cvr 
	

	def before_save(self):
		
		for i in self.mmcs_transport:
			vh = frappe.get_doc("Vehicle Type",{'name':i.vehicle_type})
			for j in self.booking_items:
				if j.length==0 :
					frappe.throw("Zero is not allowd in booking item")
				if j.height == 0 :
					frappe.throw("Zero is not allowd in booking item")
				if j.weight == 0 :
					frappe.throw("Zero is not allowd in booking item")
				if j.width == 0:	
					frappe.throw("Zero is not allowd in booking item")	
				if j.cargo_properties == "Non-Stackable":
					j.height=vh.height
				value_vw =((j.length * j.height * j.width)/5000)
				j.vw=value_vw	
				j.aw = j.numbers * j.weight	


		self.whitelisted_globals = {
			"int": int,
			"float": float,
			"long": int,
			"round": round,
		}
		a=[]
		abbr_amount={}
		abbr_per={}
		for k in self.charges_type:
			k.conversion_currency=self.conversion_currency
			# k.exchange_rate=self.exchange_rate
			abbr_amount[k.abbr]=flt(k.amount)
			abbr_per[k.abbr]=k.percentage
		abbr_amount.update(self.as_dict())
		a.append(abbr_amount)
		print("&&&&&&&&&&&&&&&&",abbr_amount)
		for c in self.charges_type:
			print(c.formula,c.idx)
			if c.formula:
				v=frappe.safe_eval(c.formula, self.whitelisted_globals,abbr_amount)
				c.amount=flt(v)
				abbr_amount.update({str(c.abbr):c.amount})
		actual_weight=[]
		for j in self.booking_items:
			actual_weight.append(j.aw)
		if len(actual_weight)>0:
			self.total_actual_weight=sum(actual_weight)
		to_capacity=[]
		cp=0
		cp1=0
		for i in self.mmcs_transport:
			cp=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["capacity"])
			if i.additional_trailer:
				cp1=frappe.get_value("Vehicle Type",{"name":i.additional_trailer},["capacity"])
			cp=cp+cp1
			i.cp_weight=cp
			to_capacity.append(cp)
		if len(to_capacity)>0:
			self.total_capacity=sum(to_capacity)
		if sum(actual_weight) >sum(to_capacity):
			frappe.throw("Total Capacity of Vehicle Reached, Add another vehicle or additional Trailer")
	
		l=[]
		w=[]
		h=[]
		for j in self.booking_items:
			l.append(j.length)
			w.append(j.width)
			h.append(j.height)
		self.total_length=sum(l)
		self.total_width=sum(w)
		self.total_height=sum(h)
		lh=[]
		wh=[]
		hh=[]
		for i in self.mmcs_transport:
			cp=frappe.get_value("Vehicle Type",{"name":i.vehicle_type},["length","width","height"])
			
			cp1=frappe.get_value("Vehicle Type",{"name":i.additional_trailer},["length","width","height"])
			lh.append(cp[0])
			wh.append(cp[1])
			hh.append(cp[2])
			if cp1:
				lh.append(cp1[0])
				wh.append(cp1[1])
				hh.append(cp1[2])
		if sum(lh)<sum(l):
			frappe.throw("Total length of Vehicle Reached, Add another vehicle or additional Trailer")
		if sum(wh)<sum(w):
			frappe.throw("Total width of Vehicle Reached, Add another vehicle or additional Trailer")
		if sum(hh)<sum(h):
			frappe.throw("Total height of Vehicle Reached, Add another vehicle or additional Trailer")

			

	@frappe.whitelist()
	def item_list(self):
		item_list = []
		t_setting = frappe.get_doc("Transport Setting")	
		itm = frappe.db.get_all("Item",{'item_group':t_setting.item_group},["name"])
		for j in itm:
			item_list.append(j.name)
		return item_list

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
	
		
			