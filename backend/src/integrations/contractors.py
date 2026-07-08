# src/integrations/contractors.py
# ==============================================
# 🔧 Prep Cook: The Recipe Card (Contractor Lookup)
#
# When the chef says "This is a plumbing issue,"
# this module knows exactly which plumber to call.
# It's a simple address book: issue type → name, phone.
#
# In a real kitchen, this would be a clipboard on
# the wall. You replace it once, and every chef
# gets the update instantly.
# ==============================================

# The clipboard — you update this once, everything else stays the same
CONTRACTOR_DIRECTORY = {
    "Plumbing": ("Raju's Plumbing", "+91-6289565427"),
    "Electrical": ("Kiran Electricals", "+91-99999-22222"),
    "HVAC": ("CoolAir Services", "+91-99999-33333"),
    "Appliance": ("FixIt Appliances", "+91-99999-44444"),
    "Structural": ("BuildRight Repairs", "+91-99999-55555"),
    "Pest": ("PestFree India", "+91-99999-66666"),
    "Other": ("General Maintenance", "+91-99999-00000"),
}


def find_contractor(issue_type: str) -> tuple[str, str]:
    """
    Look up a contractor by issue type.
    Returns (name, phone) if found, or the default 'General Maintenance'.
    """
    return CONTRACTOR_DIRECTORY.get(issue_type, CONTRACTOR_DIRECTORY["Other"])
