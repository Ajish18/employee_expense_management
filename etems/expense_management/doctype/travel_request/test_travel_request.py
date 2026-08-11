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


class IntegrationTestTravelRequest(IntegrationTestCase):
    """
    Integration tests for TravelRequest.
    Use this class for testing interactions between multiple components.
    """

    def test_travel_request(self):
        travel_request=frappe.new_doc("Travel Request")
        travel_request.employee_id="EMP-0002"
        travel_request.purpose="Frappe-Build"
        travel_request.from_location="Banglore"
        travel_request.to_location="Chennai"
        travel_request.start_date="2026-03-01"
        travel_request.end_date="2026-03-04"
        travel_request.estimated_cost=2000
        travel_request.advance_required=1
        travel_request.append("travel_itinerary",{
            "date":"2026-03-01",
            "from_location":"Banglore",
            "to_location":"Chennai",
            "mode_of_travel":"Bus",
            "expected_amount":1000
        })
        travel_request.save()
        emp = frappe.get_doc("Employee Details", travel_request.employee_id)
        self.assertEqual(travel_request.employee_name, emp.employee_name)

        apply_workflow(travel_request, "Submit")
        self.assertEqual(travel_request.status, "Pending Manager Approval")
        apply_workflow(travel_request, "Approve")
        self.assertEqual(travel_request.status, "Pending Finance Verification")
        apply_workflow(travel_request, "Approve")
        self.assertEqual(travel_request.status, "Approved")
