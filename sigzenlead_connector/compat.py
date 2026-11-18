"""Frappe 15 / Frappe 16 differences that are not a feature check at the call site.

Kept to one file so it is obvious what exists only to support Frappe 15.
"""

import os


def install_test_case_aliases():
	"""Let `from frappe.tests import IntegrationTestCase, UnitTestCase` work on Frappe 15.

	Frappe 16 ships those classes in frappe/tests/classes/. Frappe 15 has only
	frappe.tests.utils.FrappeTestCase, which does what both do here (connect, roll back the
	class's writes). On Frappe 15 -- and only there -- frappe.tests gets a module-level
	__getattr__ (PEP 562) that hands out FrappeTestCase under the v16 names. It resolves when a
	test imports them, so nothing is loaded outside a test run. Frappe 16 is left untouched.
	"""
	import frappe

	if os.path.isdir(os.path.join(os.path.dirname(frappe.__file__), "tests", "classes")):
		return  # Frappe 16+: the real classes exist.

	import frappe.tests as tests_package

	if "__getattr__" in vars(tests_package):
		return

	def __getattr__(name):
		if name in ("IntegrationTestCase", "UnitTestCase"):
			from frappe.tests.utils import FrappeTestCase

			return FrappeTestCase
		raise AttributeError(f"module 'frappe.tests' has no attribute {name!r}")

	tests_package.__getattr__ = __getattr__


def frappe_desk_mount():
	"""Where this Frappe mounts the desk: "/desk" on Frappe 16, "/app" on Frappe 15.

	Read from the installed frappe package, not the database, because hooks.py needs it
	before any site is connected. Frappe 16 is the release that ships the Workspace Sidebar
	DocType (and moved the desk to /desk).
	"""
	import frappe

	sidebar = os.path.join(os.path.dirname(frappe.__file__), "desk", "doctype", "workspace_sidebar")
	return "/desk" if os.path.isdir(sidebar) else "/app"


def remount_desk_route(route):
	"""A "/desk/..." route moved onto this Frappe's desk mount (unchanged on Frappe 16)."""
	mount = frappe_desk_mount()
	if mount != "/desk" and route.startswith("/desk/"):
		return mount + route[len("/desk") :]
	return route
