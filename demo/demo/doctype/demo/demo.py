# Copyright (c) 2024, omar and contributors
# For license information, please see license.txt
import base64
import frappe
from frappe.model.document import Document
from frappe import _

class Demo(Document):
	pass


@frappe.whitelist()
def upload_doc(full_name, attachment=None):
	try:
		new_doc = frappe.get_doc({
			"doctype": "Demo",
			"full_name": full_name,
			"img": attachment,
		})

		new_doc.insert(ignore_permissions=True)

	
		if attachment:
			file_content = base64.b64decode(attachment)

			print(file_content,'#################################')	
			file_doc = frappe.get_doc({
				"doctype": "File",
				"file_name": full_name,
				"attached_to_doctype": "Demo",
				"attached_to_name": new_doc.name,
				"content": file_content,
			})

			file_doc.insert(ignore_permissions=True)

			new_doc.set("attachment", file_doc.file_url)
			new_doc.save()

		frappe.db.commit()

		return new_doc.name
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("Error"))
		frappe.throw(_("Error while saving the document"))