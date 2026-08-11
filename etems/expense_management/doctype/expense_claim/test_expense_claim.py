# Copyright (c) 2026, ajish and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.model.workflow import apply_workflow

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestExpenseClaim(IntegrationTestCase):
	"""
	Integration tests for ExpenseClaim.
	Use this class for testing interactions between multiple components.
	"""
	def test_expense_claim(self):
		doc=frappe.get_doc({"doctype":"Expense Claim"})
		doc.employee_id="EMP-0002"
		doc.purpose="Test Expense Claim"
		doc.append("expense_details", {
			"category": "Bus",
			"date":"2026-03-01",
			"amount":1000,
			"approve_amount":1000
		})
		doc.append("expense_details", {
			"category": "Bus",
			"date":"2026-03-01",
			"amount":1000,
			"approve_amount":1000
		})
		doc.insert()
		doc.save()
		# self.assertEqual(doc.total_claimed_amount, 2000)
		apply_workflow(doc, "Submit")
		self.assertEqual(doc.status, "Pending Manager Approval")
		apply_workflow(doc, "Approve")
		self.assertEqual(doc.status, "Pending Finance Verification")
		apply_workflow(doc, "Verified")
		self.assertEqual(doc.status, "Verified")
		apply_workflow(doc, "Approve")
		self.assertEqual(doc.status, "Approved")
		apply_workflow(doc, "Settled")
		self.assertEqual(doc.status, "Settled")
