"""
PyaazMani Mandi Pricing & Geolocation Service
Tracks live and indicative onion prices per 1 kg across prominent Indian mandis with multilingual support.
"""

import math
from typing import List, Dict, Tuple

MANDI_DATABASE = [
    {
        "id": "lasalgaon",
        "name_en": "Lasalgaon APMC (Asia's Largest Onion Market)",
        "name_hi": "लासलगांव एपीएमसी (एशिया का सबसे बड़ा प्याज बाजार)",
        "name_kn": "ಲಾಸಲಗಾಂವ್ APMC (ಏಷ್ಯಾದ ಅತಿದೊಡ್ಡ ಈರುಳ್ಳಿ ಮಾರುಕಟ್ಟೆ)",
        "district_en": "Nashik",
        "district_hi": "नासिक",
        "district_kn": "ನಾಸಿಕ್",
        "state_en": "Maharashtra",
        "state_hi": "महाराष्ट्र",
        "state_kn": "ಮಹಾರಾಷ್ಟ್ರ",
        "lat": 20.1472,
        "lon": 74.2255,
        "modal_price_per_kg": 28.50,
        "min_price_per_kg": 22.00,
        "max_price_per_kg": 34.00,
        "arrivals_qtl": 34500,
        "trend": "up",
        "grade_a_rate": 34.0,
        "grade_b_rate": 28.5,
        "grade_c_rate": 19.0
    },
    {
        "id": "pimpalgaon",
        "name_en": "Pimpalgaon Baswant APMC",
        "name_hi": "पिंपलगांव बसवंत एपीएमसी",
        "name_kn": "ಪಿಂಪಲಗಾಂವ್ ಬಸವಂತ್ APMC",
        "district_en": "Nashik",
        "district_hi": "नासिक",
        "district_kn": "ನಾಸಿಕ್",
        "state_en": "Maharashtra",
        "state_hi": "महाराष्ट्र",
        "state_kn": "ಮಹಾರಾಷ್ಟ್ರ",
        "lat": 20.1706,
        "lon": 73.9858,
        "modal_price_per_kg": 27.80,
        "min_price_per_kg": 21.50,
        "max_price_per_kg": 33.50,
        "arrivals_qtl": 26800,
        "trend": "up",
        "grade_a_rate": 33.5,
        "grade_b_rate": 27.8,
        "grade_c_rate": 18.5
    },
    {
        "id": "yeshwanthpur",
        "name_en": "Bangalore / Yeshwanthpur APMC",
        "name_hi": "बेंगलुरु / यशवंतपुर एपीएमसी",
        "name_kn": "ಬೆಂಗಳೂರು / ಯಶವಂತಪುರ APMC",
        "district_en": "Bengaluru Urban",
        "district_hi": "बेंगलुरु शहरी",
        "district_kn": "ಬೆಂಗಳೂರು ನಗರ",
        "state_en": "Karnataka",
        "state_hi": "कर्नाटक",
        "state_kn": "ಕರ್ನಾಟಕ",
        "lat": 13.0238,
        "lon": 77.5529,
        "modal_price_per_kg": 32.00,
        "min_price_per_kg": 25.00,
        "max_price_per_kg": 38.00,
        "arrivals_qtl": 18200,
        "trend": "up",
        "grade_a_rate": 38.0,
        "grade_b_rate": 32.0,
        "grade_c_rate": 22.0
    },
    {
        "id": "hubli",
        "name_en": "Hubli (Amaragol) APMC",
        "name_hi": "हुबली (अमरगोल) एपीएमसी",
        "name_kn": "ಹುಬ್ಬಳ್ಳಿ (ಅಮರಗೋಳ) APMC",
        "district_en": "Dharwad",
        "district_hi": "धारवाड़",
        "district_kn": "ಧಾರವಾಡ",
        "state_en": "Karnataka",
        "state_hi": "कर्नाटक",
        "state_kn": "ಕರ್ನಾಟಕ",
        "lat": 15.3647,
        "lon": 75.1240,
        "modal_price_per_kg": 29.20,
        "min_price_per_kg": 23.00,
        "max_price_per_kg": 35.00,
        "arrivals_qtl": 14500,
        "trend": "stable",
        "grade_a_rate": 35.0,
        "grade_b_rate": 29.2,
        "grade_c_rate": 20.0
    },
    {
        "id": "kalaburagi",
        "name_en": "Kalaburagi APMC Yard",
        "name_hi": "कलबुर्गी एपीएमसी यार्ड",
        "name_kn": "ಕಲಬುರಗಿ APMC ಯಾರ್ಡ್",
        "district_en": "Kalaburagi",
        "district_hi": "कलबुर्गी",
        "district_kn": "ಕಲಬುರಗಿ",
        "state_en": "Karnataka",
        "state_hi": "कर्नाटक",
        "state_kn": "ಕರ್ನಾಟಕ",
        "lat": 17.3297,
        "lon": 76.8343,
        "modal_price_per_kg": 30.50,
        "min_price_per_kg": 24.00,
        "max_price_per_kg": 36.00,
        "arrivals_qtl": 9800,
        "trend": "stable",
        "grade_a_rate": 36.0,
        "grade_b_rate": 30.5,
        "grade_c_rate": 21.0
    },
    {
        "id": "belgaum",
        "name_en": "Belgaum APMC Sub-Yard",
        "name_hi": "बेलगाम (बेलगावी) एपीएमसी उप-यार्ड",
        "name_kn": "ಬೆಳಗಾವಿ APMC ಉಪ-ಯಾರ್ಡ್",
        "district_en": "Belagavi",
        "district_hi": "बेलगावी",
        "district_kn": "ಬೆಳಗಾವಿ",
        "state_en": "Karnataka",
        "state_hi": "कर्नाटक",
        "state_kn": "ಕರ್ನಾಟಕ",
        "lat": 15.8497,
        "lon": 74.4977,
        "modal_price_per_kg": 29.80,
        "min_price_per_kg": 23.50,
        "max_price_per_kg": 35.50,
        "arrivals_qtl": 11200,
        "trend": "stable",
        "grade_a_rate": 35.5,
        "grade_b_rate": 29.8,
        "grade_c_rate": 20.5
    },
    {
        "id": "solapur",
        "name_en": "Solapur APMC Market",
        "name_hi": "सोलापुर एपीएमसी मार्केट",
        "name_kn": "ಸೋಲಾಪುರ APMC ಮಾರುಕಟ್ಟೆ",
        "district_en": "Solapur",
        "district_hi": "सोलापुर",
        "district_kn": "ಸೋಲಾಪುರ",
        "state_en": "Maharashtra",
        "state_hi": "महाराष्ट्र",
        "state_kn": "ಮಹಾರಾಷ್ಟ್ರ",
        "lat": 17.6599,
        "lon": 75.9064,
        "modal_price_per_kg": 26.50,
        "min_price_per_kg": 20.00,
        "max_price_per_kg": 32.00,
        "arrivals_qtl": 21000,
        "trend": "down",
        "grade_a_rate": 32.0,
        "grade_b_rate": 26.5,
        "grade_c_rate": 18.0
    },
    {
        "id": "pune",
        "name_en": "Pune (Gultekdi) APMC",
        "name_hi": "पुणे (गुलटेकड़ी) एपीएमसी",
        "name_kn": "ಪುಣೆ (ಗುಲ್ತೇಕಡಿ) APMC",
        "district_en": "Pune",
        "district_hi": "पुणे",
        "district_kn": "ಪುಣೆ",
        "state_en": "Maharashtra",
        "state_hi": "महाराष्ट्र",
        "state_kn": "ಮಹಾರಾಷ್ಟ್ರ",
        "lat": 18.4965,
        "lon": 73.8643,
        "modal_price_per_kg": 30.00,
        "min_price_per_kg": 24.00,
        "max_price_per_kg": 36.50,
        "arrivals_qtl": 19500,
        "trend": "stable",
        "grade_a_rate": 36.5,
        "grade_b_rate": 30.0,
        "grade_c_rate": 21.0
    },
    {
        "id": "azadpur",
        "name_en": "Azadpur APMC (Delhi Terminal)",
        "name_hi": "आज़ादपुर एपीएमसी (दिल्ली मंडी)",
        "name_kn": "ಆಜಾದ್‌ಪುರ APMC (ದೆಹಲಿ ಮಂಡಿ)",
        "district_en": "North Delhi",
        "district_hi": "उत्तर दिल्ली",
        "district_kn": "ಉತ್ತರ ದೆಹಲಿ",
        "state_en": "Delhi",
        "state_hi": "दिल्ली",
        "state_kn": "ದೆಹಲಿ",
        "lat": 28.7126,
        "lon": 77.1752,
        "modal_price_per_kg": 35.00,
        "min_price_per_kg": 28.00,
        "max_price_per_kg": 42.00,
        "arrivals_qtl": 42000,
        "trend": "up",
        "grade_a_rate": 42.0,
        "grade_b_rate": 35.0,
        "grade_c_rate": 25.0
    },
    {
        "id": "indore",
        "name_en": "Indore (Choithram) Mandi",
        "name_hi": "इंदौर (चोइथराम) मंडी",
        "name_kn": "ಇಂದೋರ್ (ಚೋಯಿತ್‌ರಾಮ್) ಮಂಡಿ",
        "district_en": "Indore",
        "district_hi": "इंदौर",
        "district_kn": "ಇಂದೋರ್",
        "state_en": "Madhya Pradesh",
        "state_hi": "मध्य प्रदेश",
        "state_kn": "ಮಧ್ಯಪ್ರದೇಶ",
        "lat": 22.6841,
        "lon": 75.8504,
        "modal_price_per_kg": 27.00,
        "min_price_per_kg": 21.00,
        "max_price_per_kg": 33.00,
        "arrivals_qtl": 16000,
        "trend": "stable",
        "grade_a_rate": 33.0,
        "grade_b_rate": 27.0,
        "grade_c_rate": 18.0
    },
    {
        "id": "gondal",
        "name_en": "Gondal APMC Market Yard",
        "name_hi": "गोंडल एपीएमसी मार्केट यार्ड",
        "name_kn": "ಗೊಂಡಲ್ APMC ಮಾರ್ಕೆಟ್ ಯಾರ್ಡ್",
        "district_en": "Rajkot",
        "district_hi": "राजकोट",
        "district_kn": "ರಾಜಕೋಟ್",
        "state_en": "Gujarat",
        "state_hi": "गुजरात",
        "state_kn": "ಗುಜರಾತ್",
        "lat": 21.9619,
        "lon": 70.7997,
        "modal_price_per_kg": 28.00,
        "min_price_per_kg": 22.00,
        "max_price_per_kg": 34.00,
        "arrivals_qtl": 22400,
        "trend": "up",
        "grade_a_rate": 34.0,
        "grade_b_rate": 28.0,
        "grade_c_rate": 19.5
    },
    {
        "id": "vashi",
        "name_en": "Mumbai APMC (Vashi)",
        "name_hi": "मुंबई एपीएमसी (वाशी)",
        "name_kn": "ಮುಂಬೈ APMC (ವಾಶಿ)",
        "district_en": "Thane / Navi Mumbai",
        "district_hi": "ठाणे / नवी मुंबई",
        "district_kn": "ಥಾಣೆ / ನವಿ ಮುಂಬೈ",
        "state_en": "Maharashtra",
        "state_hi": "महाराष्ट्र",
        "state_kn": "ಮಹಾರಾಷ್ಟ್ರ",
        "lat": 19.0771,
        "lon": 73.0069,
        "modal_price_per_kg": 33.50,
        "min_price_per_kg": 26.00,
        "max_price_per_kg": 40.00,
        "arrivals_qtl": 31000,
        "trend": "up",
        "grade_a_rate": 40.0,
        "grade_b_rate": 33.5,
        "grade_c_rate": 23.0
    }
]


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Great Circle distance in kilometers between two coordinates."""
    R = 6371.0

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2.0) ** 2)

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)


def get_nearby_mandis(user_lat: float, user_lon: float, limit: int = 6, lang: str = "en") -> List[Dict]:
    """Sort and return nearest mandis with localized names in selected language."""
    mandis_with_dist = []
    for mandi in MANDI_DATABASE:
        dist = haversine_distance(user_lat, user_lon, mandi["lat"], mandi["lon"])
        item = dict(mandi)
        item["distance_km"] = dist
        item["name"] = mandi.get(f"name_{lang}", mandi["name_en"])
        item["district"] = mandi.get(f"district_{lang}", mandi["district_en"])
        item["state"] = mandi.get(f"state_{lang}", mandi["state_en"])
        mandis_with_dist.append(item)

    mandis_with_dist.sort(key=lambda x: x["distance_km"])
    return mandis_with_dist[:limit]


def get_all_mandis(lang: str = "en") -> List[Dict]:
    """Return all mandis with localized names."""
    out = []
    for mandi in MANDI_DATABASE:
        item = dict(mandi)
        item["name"] = mandi.get(f"name_{lang}", mandi["name_en"])
        item["district"] = mandi.get(f"district_{lang}", mandi["district_en"])
        item["state"] = mandi.get(f"state_{lang}", mandi["state_en"])
        out.append(item)
    return out
