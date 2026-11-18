__version__ = "1.1.1"

try:  # Frappe 15 support; a no-op on Frappe 16 and when frappe is not importable (packaging).
	from .compat import install_test_case_aliases

	install_test_case_aliases()
except Exception:  # never let a compatibility shim stop the app from importing
	pass
