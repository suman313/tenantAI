# test_contractors.py
from backend.src.integrations.contractors import find_contractor

name, phone = find_contractor("HVAC")
print(f"HVAC → {name} ({phone})")

name, phone = find_contractor("Pest")
print(f"Pest → {name} ({phone})")

name, phone = find_contractor("Nuclear")  # not on the clipboard
print(f"Nuclear → {name} ({phone})")