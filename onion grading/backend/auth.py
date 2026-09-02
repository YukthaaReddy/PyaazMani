"""
PyaazMani Authentication & Role Manager
Supports 3 Roles: Farmer, Inspector, Government Official.
"""

ROLES = {
    "farmer": {
        "id": "farmer",
        "name": "Farmer",
        "name_hi": "किसान",
        "name_kn": "ರೈತರು",
        "icon": "🧑‍🌾",
        "default_user": "FARM-1042",
        "default_name": "Ramesh Kumar (Nashik)",
        "allowed_fragments": ["grade", "mandi", "settings"],
        "badge_color": "#16A34A"
    },
    "inspector": {
        "id": "inspector",
        "name": "Mandi Quality Inspector",
        "name_hi": "गुणवत्ता निरीक्षक",
        "name_kn": "ಗುಣಮಟ್ಟ ಪರಿವೀಕ್ಷಕರು",
        "icon": "🔬",
        "default_user": "INS-8021",
        "default_name": "Inspector S. Patil (APMC Lasalgaon)",
        "allowed_fragments": ["grade", "mandi", "analytics", "settings"],
        "badge_color": "#BE185D"
    },
    "official": {
        "id": "official",
        "name": "Government Official",
        "name_hi": "सरकारी / एपीएमसी अधिकारी",
        "name_kn": "ಸರ್ಕಾರಿ ಅಧಿಕಾರಿ",
        "icon": "🏛️",
        "default_user": "GOV-5501",
        "default_name": "Director of APMC Quality Standards",
        "allowed_fragments": ["grade", "mandi", "reports", "analytics", "settings"],
        "badge_color": "#2563EB"
    }
}


def get_role_info(role_id: str) -> dict:
    """Retrieve metadata for a given role."""
    return ROLES.get(role_id, ROLES["farmer"])
