"""
🧅 PyaazMani — AI Onion Quality & Mandi Suite
Modular Chapter-Based Architecture with High-Contrast Theming & Role Logins.
"""

import streamlit as st
import streamlit.components.v1 as components
import tempfile
import html
import io
import json
import textwrap
import re
import importlib
from pathlib import Path
from datetime import datetime

# Hot-reload backend modules to avoid in-memory caching
import backend.i18n
import backend.theme
import backend.auth
import backend.service
import backend.database
import backend.pdf_generator
import backend.mandi_service
import backend.disease_detector

importlib.reload(backend.i18n)
importlib.reload(backend.theme)
importlib.reload(backend.auth)
importlib.reload(backend.service)
importlib.reload(backend.database)
importlib.reload(backend.pdf_generator)
importlib.reload(backend.mandi_service)
importlib.reload(backend.disease_detector)

from backend.i18n import t, TRANSLATIONS
from backend.theme import get_theme_css
from backend.auth import ROLES, get_role_info
from backend.service import analyze_onion, save_grading_result
from backend.database import initialize_database, get_all_records
from backend.pdf_generator import generate_pdf_report
from backend.mandi_service import get_nearby_mandis, get_all_mandis, MANDI_DATABASE

# =========================================================
# 1. INITIALIZE APP CONFIG & DATABASE
# =========================================================
st.set_page_config(
    page_title="PyaazMani | AI Onion Quality & Mandi Suite",
    page_icon="🧅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

initialize_database()

# Session State
if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "font_size" not in st.session_state:
    st.session_state.font_size = "normal"

if "role" not in st.session_state:
    st.session_state.role = "farmer"

if "user_name" not in st.session_state:
    st.session_state.user_name = "Ramesh Kumar (Nashik)"

if "user_id" not in st.session_state:
    st.session_state.user_id = "FARM-1042"

if "active_chapter" not in st.session_state:
    st.session_state.active_chapter = "home"

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "saved_result_hash" not in st.session_state:
    st.session_state.saved_result_hash = None

if "user_coords" not in st.session_state:
    st.session_state.user_coords = (20.0059, 73.7898)
    st.session_state.user_location_key = "city_nashik"

if "voice_assistant" not in st.session_state:
    st.session_state.voice_assistant = False

lang = st.session_state.lang
theme = st.session_state.theme
font_size = st.session_state.font_size
role = st.session_state.role


def speak_with_browser_voice(text: str, language: str = "en-US") -> None:
    """Trigger browser speech synthesis if the user has enabled the voice assistant."""
    if not st.session_state.get("voice_assistant", False) or not text:
        return

    script = f"""
    <script>
      function speakVoiceAssistant() {{
        const text = {json.dumps(text)};
        const lang = {json.dumps(language)};
        if ('speechSynthesis' in window) {{
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = lang;
          utterance.rate = 1;
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(utterance);
        }}
      }}
      speakVoiceAssistant();
    </script>
    """
    components.html(script, height=0)

# Apply Scoped Dynamic CSS
st.markdown(get_theme_css(theme=theme, font_size=font_size), unsafe_allow_html=True)


def render_html(content: str):
    """Render HTML safely without triggering Markdown indentation code blocks."""
    cleaned = textwrap.dedent(content).strip()
    cleaned = re.sub(r"\n[ \t]*\n", "\n", cleaned)
    lines = [line.strip() for line in cleaned.split("\n")]
    single_line_html = "".join(lines)
    st.markdown(single_line_html, unsafe_allow_html=True)


def normalize_record(r):
    """Ensure record is always a dictionary with valid values."""
    if isinstance(r, dict):
        return {
            "id": r.get("id", 1),
            "farmer_name": str(r.get("farmer_name", "")),
            "farmer_id": str(r.get("farmer_id", "")),
            "lot_id": str(r.get("lot_id", "")),
            "center": str(r.get("center", "")),
            "quantity": float(r.get("quantity", 100.0)),
            "grade": str(r.get("grade", "A")),
            "confidence": float(r.get("confidence", 0.9)),
            "quality_score": float(r.get("quality_score", 85.0)),
            "urs_percentage": float(r.get("urs_percentage", 2.5)),
            "disease_name": str(r.get("disease_name", "Healthy")),
            "disease_severity": str(r.get("disease_severity", "None")),
            "price_per_kg": float(r.get("price_per_kg", 25.0)),
            "total_value": float(r.get("total_value", 2500.0)),
            "role": str(r.get("role", "farmer")),
            "timestamp": str(r.get("timestamp", "")),
            "previous_hash": str(r.get("previous_hash", "0")),
            "record_hash": str(r.get("record_hash", ""))
        }
    elif isinstance(r, (list, tuple)):
        return {
            "id": r[0] if len(r) > 0 else 1,
            "farmer_name": str(r[1]) if len(r) > 1 else "",
            "farmer_id": str(r[2]) if len(r) > 2 else "",
            "lot_id": str(r[3]) if len(r) > 3 else "",
            "center": str(r[4]) if len(r) > 4 else "",
            "quantity": float(r[5]) if len(r) > 5 else 100.0,
            "grade": str(r[6]) if len(r) > 6 else "A",
            "confidence": float(r[7]) if len(r) > 7 else 0.9,
            "quality_score": float(r[8]) if len(r) > 8 else 85.0,
            "urs_percentage": float(r[9]) if len(r) > 9 and r[9] is not None else 2.5,
            "disease_name": str(r[10]) if len(r) > 10 and r[10] is not None else "Healthy",
            "disease_severity": str(r[11]) if len(r) > 11 and r[11] is not None else "None",
            "price_per_kg": float(r[12]) if len(r) > 12 and r[12] is not None else 25.0,
            "total_value": float(r[13]) if len(r) > 13 and r[13] is not None else 2500.0,
            "role": str(r[14]) if len(r) > 14 and r[14] is not None else "farmer",
            "timestamp": str(r[15]) if len(r) > 15 else "",
            "previous_hash": str(r[16]) if len(r) > 16 else "0",
            "record_hash": str(r[17]) if len(r) > 17 else ""
        }
    return {}


# =========================================================
# 2. TOP BRANDING & ROLE PERSONA BAR
# =========================================================
role_info = get_role_info(role)
role_display_name = role_info.get(f"name_{lang}", role_info["name"])

# Navbar Header (Strictly Single-Line Brand)
render_html(f"""
<div class="pm-navbar">
    <div class="pm-brand-wrap">
        <div class="pm-brand">
            🧅&nbsp;{t('app_brand', lang)}
        </div>
        <div class="pm-tagline">
            &nbsp;|&nbsp; {html.escape(t('app_tagline', lang))}
        </div>
    </div>
    <div class="pm-role-pill" style="background: {role_info['badge_color']}33; border-color: {role_info['badge_color']};">
        <span>{role_info['icon']}</span>
        <span><b>{html.escape(role_display_name)}</b> ({html.escape(st.session_state.user_name)})</span>
        <span style="color: #22C55E; font-size: 11px;">● {t('mandi_status_online', lang)}</span>
    </div>
</div>
""")

# Top Quick Switchers Bar (Role Buttons, Language, Theme)
top_cols = st.columns([3.6, 1.1, 1.3])

with top_cols[0]:
    # 3 Distinct Instant Role Switcher Pills
    r_cols = st.columns(3)
    with r_cols[0]:
        is_farmer = (role == "farmer")
        if st.button(f"🧑‍🌾 {t('role_farmer', lang)}", use_container_width=True, type="primary" if is_farmer else "secondary", key="btn_role_farmer"):
            st.session_state.role = "farmer"
            st.session_state.user_name = ROLES["farmer"]["default_name"]
            st.session_state.user_id = ROLES["farmer"]["default_user"]
            st.session_state.active_chapter = "home"
            st.rerun()

    with r_cols[1]:
        is_inspector = (role == "inspector")
        if st.button(f"🔬 {t('role_inspector', lang)}", use_container_width=True, type="primary" if is_inspector else "secondary", key="btn_role_inspector"):
            st.session_state.role = "inspector"
            st.session_state.user_name = ROLES["inspector"]["default_name"]
            st.session_state.user_id = ROLES["inspector"]["default_user"]
            st.session_state.active_chapter = "home"
            st.rerun()

    with r_cols[2]:
        is_official = (role == "official")
        if st.button(f"🏛️ {t('role_official', lang)}", use_container_width=True, type="primary" if is_official else "secondary", key="btn_role_official"):
            st.session_state.role = "official"
            st.session_state.user_name = ROLES["official"]["default_name"]
            st.session_state.user_id = ROLES["official"]["default_user"]
            st.session_state.active_chapter = "home"
            st.rerun()

with top_cols[1]:
    # Quick Language Selector
    lang_opts = {"en": "English", "hi": "हिन्दी", "kn": "ಕನ್ನಡ", "bn": "বাংলা", "mr": "मराठी", "ta": "தமிழ்"}
    new_lang = st.selectbox(
        "Language",
        options=list(lang_opts.keys()),
        format_func=lambda x: lang_opts[x],
        index=list(lang_opts.keys()).index(lang),
        label_visibility="collapsed",
        key="top_lang_selector"
    )
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

with top_cols[2]:
    # Quick Theme Toggle
    theme_text = ("🌙 " + ("डार्क थीम" if lang == "hi" else ("ಡಾರ್ಕ್ ಥೀಮ್" if lang == "kn" else "Dark Theme"))) if theme == "light" else ("🌸 " + ("लाइट थीम" if lang == "hi" else ("ಲೈಟ್ ಥೀಮ್" if lang == "kn" else "Light Theme")))
    if st.button(theme_text, use_container_width=True, key="top_theme_toggle_btn"):
        st.session_state.theme = "dark" if theme == "light" else "light"
        st.rerun()

st.write("")


# Back Button Handler (shown on sub-pages)
if st.session_state.active_chapter != "home":
    b_col1, b_col2 = st.columns([1.8, 4.2])
    with b_col1:
        if st.button(t("back_to_home", lang), use_container_width=True, key="back_to_home_btn"):
            st.session_state.active_chapter = "home"
            st.rerun()
    st.write("")


# =========================================================
# 3. HOME VIEW: CHAPTERS GRID (MATCHING USER REFERENCE IMAGE)
# =========================================================
if st.session_state.active_chapter == "home":

    render_html(f"""
    <div class="pm-hero">
        <h1>🧅 {html.escape(t('home_hero_title', lang))}</h1>
        <p>{html.escape(t('home_hero_desc', lang))}</p>
    </div>
    """)

    st.markdown(f'<div class="pm-section-title">📂 {t("home_chapters_title", lang)}</div>', unsafe_allow_html=True)
    st.caption(t("home_chapters_subtitle", lang))

    allowed_frags = ROLES[role]["allowed_fragments"]

    # Chapter definitions
    chapters = [
        {
            "id": "grade",
            "icon": "🔬",
            "title": t("nav_grade", lang),
            "desc": t("nav_grade_desc", lang),
            "visible": ("grade" in allowed_frags)
        },
        {
            "id": "mandi",
            "icon": "📈",
            "title": t("nav_mandi", lang),
            "desc": t("nav_mandi_desc", lang),
            "visible": ("mandi" in allowed_frags)
        },
        {
            "id": "reports",
            "icon": "📑",
            "title": t("nav_reports", lang),
            "desc": t("nav_reports_desc", lang),
            "visible": ("reports" in allowed_frags),
            "badge": t("badge_gov_exclusive", lang)
        },
        {
            "id": "analytics",
            "icon": "🏛️",
            "title": t("nav_analytics", lang),
            "desc": t("nav_analytics_desc", lang),
            "visible": ("analytics" in allowed_frags)
        },
        {
            "id": "settings",
            "icon": "⚙️",
            "title": t("nav_settings", lang),
            "desc": t("nav_settings_desc", lang),
            "visible": ("settings" in allowed_frags)
        }
    ]

    visible_chapters = [c for c in chapters if c["visible"]]

    # Responsive chapter grid: on mobile, keep only the application chapters in a 2-column layout
    st.markdown('<div class="pm-chapter-grid-anchor"></div>', unsafe_allow_html=True)
    num_cols = 2 if len(visible_chapters) <= 4 else 3
    grid_cols = st.columns(num_cols)

    for idx, chap in enumerate(visible_chapters):
        col = grid_cols[idx % num_cols]
        with col:
            badge_html = f'<div style="background: #2563EB; color: #FFFFFF; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 10px; margin-top: 8px; display: inline-block;">🔒 {chap["badge"]}</div>' if "badge" in chap else ""
            
            render_html(f"""<div class="pm-chapter-card"><div class="pm-chapter-icon">{chap['icon']}</div><div class="pm-chapter-title">{html.escape(chap['title'])}</div><div class="pm-chapter-desc">{html.escape(chap['desc'])}</div>{badge_html}</div>""")

            btn_label = f"✨ {t('open_chapter_btn', lang)}"
            if st.button(btn_label, use_container_width=True, key=f"open_chap_{chap['id']}"):
                st.session_state.active_chapter = chap["id"]
                st.rerun()

            st.write("")


# =========================================================
# 4. CHAPTER 1: CHECK ONION QUALITY & DISEASE DETECTION
# =========================================================
elif st.session_state.active_chapter == "grade":

    render_html(f"""
    <div class="pm-hero">
        <h1>🔬 {html.escape(t('grade_header', lang))}</h1>
        <p>{html.escape(t('grade_subtitle', lang))}</p>
    </div>
    """)

    # Farmer Lot Metadata Section
    st.markdown(f'<div class="pm-section-title">📝 {t("section_lot_info", lang)}</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.2])

    with c1:
        farmer_name = st.text_input(t("farmer_name", lang), value=st.session_state.user_name if role == "farmer" else ("रमेश कुमार" if lang == "hi" else ("ರಮೇಶ್ ಕುಮಾರ್" if lang == "kn" else "Ramesh Kumar")))

    with c2:
        farmer_id = st.text_input(t("farmer_id", lang), value=st.session_state.user_id if role == "farmer" else "FARM-1042")

    with c3:
        lot_id = st.text_input(t("lot_id", lang), value="LOT-2026-N89")

    with c4:
        mandi_center_options = [
            t("city_nashik", lang),
            t("city_bangalore", lang),
            t("city_hubli", lang),
            t("city_kalaburagi", lang),
            t("city_solapur", lang),
            t("city_delhi", lang)
        ]
        mandi_center = st.selectbox(t("mandi_center", lang), mandi_center_options)

    c5, c6 = st.columns([1, 1])
    with c5:
        quantity = st.number_input(t("quantity_kg", lang), min_value=1.0, value=250.0, step=10.0)

    with c6:
        variety_options = [
            t("variety_rabi", lang),
            t("variety_kharif", lang),
            t("variety_late_kharif", lang)
        ]
        variety = st.selectbox(t("variety_label", lang), variety_options)

    st.write("")

    # Photo Upload Section
    st.markdown(f'<div class="pm-section-title">📸 {t("section_photo", lang)}</div>', unsafe_allow_html=True)
    st.caption(t("upload_desc", lang))

    # Sample demo buttons
    demo_cols = st.columns([2, 1, 1, 1])
    sample_img_path = None

    with demo_cols[1]:
        if st.button(t("demo_grade_a", lang), use_container_width=True, key="demo_a"):
            sample_img_path = "data/grade_A/images.jpg"

    with demo_cols[2]:
        if st.button(t("demo_grade_b", lang), use_container_width=True, key="demo_b"):
            sample_img_path = "data/grade_B/images.jpg"

    with demo_cols[3]:
        if st.button(t("demo_grade_c", lang), use_container_width=True, key="demo_c"):
            sample_img_path = "data/grade_C/images.jpg"

    render_html(f"""
    <div class="pm-upload-box">
        <div class="pm-upload-icon">📷</div>
        <div style="font-weight: 800; font-size: 16px; margin-bottom: 4px;">{html.escape(t('upload_dropzone_title', lang))}</div>
        <div style="font-size: 13px; color: { '#475569' if theme == 'light' else '#FBCFE8' };">{html.escape(t('upload_dropzone_sub', lang))}</div>
    </div>
    """)

    uploaded_file = st.file_uploader(
        "Upload onion photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="onion_photo_uploader"
    )

    active_image = None
    if uploaded_file is not None:
        active_image = uploaded_file.read()
    elif sample_img_path and Path(sample_img_path).exists():
        with open(sample_img_path, "rb") as f:
            active_image = f.read()

    if active_image:
        col_img, col_info = st.columns([1.1, 0.9])

        with col_img:
            st.image(active_image, caption="Onion Sample", use_container_width=True)

        with col_info:
            render_html(f"""
            <div class="pm-card">
                <div class="pm-card-title">🔍 {html.escape(t('img_ready_title', lang))}</div>
                <div class="pm-card-text">
                    {html.escape(t('img_ready_desc', lang))}
                    <ul style="margin-top: 8px; margin-bottom: 8px; padding-left: 20px;">
                        <li><b>{html.escape(t('feat_item_1', lang))}</b></li>
                        <li><b>{html.escape(t('feat_item_2', lang))}</b></li>
                        <li><b>{html.escape(t('feat_item_3', lang))}</b></li>
                        <li><b>{html.escape(t('feat_item_4', lang))}</b></li>
                    </ul>
                </div>
            </div>
            """)

            if st.button(t("btn_grade", lang), type="primary", use_container_width=True, key="btn_run_grading"):
                with st.spinner(t("analyzing_spinner", lang)):
                    try:
                        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                            tmp.write(active_image)
                            temp_path = tmp.name

                        analysis = analyze_onion(
                            image_path=temp_path,
                            farmer_name=farmer_name,
                            farmer_id=farmer_id,
                            lot_id=lot_id,
                            center=mandi_center,
                            quantity=quantity,
                            role=role,
                            lang=lang
                        )

                        st.session_state.last_result = analysis
                        st.session_state.saved_result_hash = None
                        st.success(t("inspection_complete", lang))

                    except Exception as e:
                        st.error(f"Error during inspection: {str(e)}")
                        st.exception(e)

    # ----------------------------------------------------
    # GRADING RESULT DISPLAY
    # ----------------------------------------------------
    if st.session_state.last_result:
        res = st.session_state.last_result
        grade = res["grade"]
        conf = res["confidence"]
        score = res["quality_score"]
        urs = res["urs_percentage"]
        rate = res["price_per_kg"]
        total_val = res["total_value"]
        disease_name = res["disease_name"]
        severity = res["disease_severity"]
        remedy = res["remedy"]
        is_healthy = res["is_healthy"]

        st.markdown("---")
        st.markdown(f'<div class="pm-section-title">📊 {t("results_title", lang)}</div>', unsafe_allow_html=True)

        grade_class = f"grade-{grade.lower()}"
        grade_title_key = f"grade_{grade.lower()}_title"
        grade_desc_key = f"grade_{grade.lower()}_desc"

        render_html(f"""
        <div class="pm-grade-box {grade_class}">
            <h1>{t('grade_badge', lang).upper()} {html.escape(grade)}</h1>
            <p>{html.escape(t(grade_title_key, lang))}</p>
            <div style="font-size: 13px; opacity: 0.95; margin-top: 6px;">{html.escape(t(grade_desc_key, lang))}</div>
        </div>
        """)

        # Metric Tiles
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_html(f"""
            <div class="pm-metric-tile">
                <div class="pm-metric-val">{conf:.1%}</div>
                <div class="pm-metric-lbl">{t('confidence', lang)}</div>
            </div>
            """)

        with m2:
            render_html(f"""
            <div class="pm-metric-tile">
                <div class="pm-metric-val">{score:.1f}/100</div>
                <div class="pm-metric-lbl">{t('quality_score', lang)}</div>
            </div>
            """)

        with m3:
            render_html(f"""
            <div class="pm-metric-tile">
                <div class="pm-metric-val">{urs:.1f}%</div>
                <div class="pm-metric-lbl">{t('urs_percentage', lang)}</div>
            </div>
            """)

        with m4:
            render_html(f"""
            <div class="pm-metric-tile">
                <div class="pm-metric-val">₹{rate:.1f} <span style="font-size: 16px;">/kg</span></div>
                <div class="pm-metric-lbl">{t('estimated_rate', lang)}</div>
            </div>
            """)

        st.write("")

        # Disease Box
        badge_cls = "badge-healthy" if is_healthy else ("badge-warning" if severity == "Low" else "badge-danger")
        render_html(f"""
        <div class="pm-disease-box">
            <div class="pm-disease-title">
                <span>🔬 {t('disease_status', lang)}:</span>
                <b>{html.escape(disease_name)}</b>
                <span class="pm-disease-badge {badge_cls}">{t('disease_severity', lang)}: {html.escape(severity)}</span>
            </div>
            <div style="color: inherit; font-size: 14px; margin-top: 8px; font-weight: 600;">
                <b>💡 {t('disease_remedy', lang)}:</b> {html.escape(remedy)}
            </div>
        </div>
        """)

        # Feature Biometrics
        with st.expander(t("biometrics_expander", lang), expanded=False):
            feature_labels = [
                t("feat_area", lang), t("feat_perimeter", lang), t("feat_circularity", lang), t("feat_hue", lang),
                t("feat_sat", lang), t("feat_brightness", lang), t("feat_bright_std", lang),
                t("feat_spot_count", lang), t("feat_spot_ratio", lang), t("feat_edge_density", lang)
            ]
            f_cols = st.columns(5)
            for idx, (f_name, f_val) in enumerate(zip(feature_labels, res["features"])):
                col = f_cols[idx % 5]
                with col:
                    st.metric(f_name, f"{f_val:.2f}")

        # PDF & Save Actions (ONLY SHOWN TO INSPECTOR AND GOVERNMENT OFFICIAL, NOT FARMER)
        if role != "farmer":
            st.markdown("---")
            act_col1, act_col2 = st.columns([1, 1])

            with act_col1:
                pdf_bytes = generate_pdf_report(res["record"])
                file_name = f"PyaazMani_Certificate_{res['record']['lot_id']}.pdf"

                st.download_button(
                    label=t("btn_download_pdf", lang),
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_current_pdf"
                )

            with act_col2:
                if st.session_state.saved_result_hash:
                    st.success(f"{t('record_saved', lang)} ({t('sha256_seal_lbl', lang)}: {st.session_state.saved_result_hash[:16]}...)")
                else:
                    if st.button(t("btn_save_record", lang), type="primary", use_container_width=True, key="save_current_rec"):
                        saved_rec = save_grading_result(res)
                        st.session_state.saved_result_hash = saved_rec["record_hash"]
                        st.rerun()


# =========================================================
# 5. CHAPTER 2: NEARBY MANDI PRICES (₹/1 KG)
# =========================================================
elif st.session_state.active_chapter == "mandi":

    render_html(f"""
    <div class="pm-hero">
        <h1>📈 {html.escape(t('mandi_header', lang))}</h1>
        <p>{html.escape(t('mandi_subtitle', lang))}</p>
    </div>
    """)

    geo_col1, geo_col2 = st.columns([1.5, 2.5])

    # Localized Region List
    city_list = [
        ("city_nashik", (20.0059, 73.7898)),
        ("city_bangalore", (13.0238, 77.5529)),
        ("city_hubli", (15.3647, 75.1240)),
        ("city_kalaburagi", (17.3297, 76.8343)),
        ("city_belgaum", (15.8497, 74.4977)),
        ("city_solapur", (17.6599, 75.9064)),
        ("city_pune", (18.4965, 73.8643)),
        ("city_delhi", (28.7126, 77.1752)),
        ("city_indore", (22.6841, 75.8504)),
        ("city_rajkot", (21.9619, 70.7997))
    ]

    city_dict = {t(k, lang): coords for k, coords in city_list}
    city_keys_map = {t(k, lang): k for k, coords in city_list}
    labels = list(city_dict.keys())

    with geo_col1:
        st.markdown(f'<div class="pm-section-title">📍 {t("location_gps_title", lang)}</div>', unsafe_allow_html=True)
        
        current_loc_label = t(st.session_state.user_location_key, lang)
        selected_index = labels.index(current_loc_label) if current_loc_label in labels else 0

        selected_label = st.selectbox(
            t("select_region_label", lang),
            options=labels,
            index=selected_index
        )

        user_lat, user_lon = city_dict[selected_label]
        st.session_state.user_coords = (user_lat, user_lon)
        st.session_state.user_location_key = city_keys_map[selected_label]

        st.caption(f"{t('detected_coords', lang)}: `{user_lat:.4f}° N, {user_lon:.4f}° E`")

    with geo_col2:
        st.markdown(f'<div class="pm-section-title">💡 {t("market_advisory_title", lang)}</div>', unsafe_allow_html=True)
        render_html(f"""
        <div class="pm-card" style="margin-bottom: 0;">
            <div class="pm-card-text">
                📌 {html.escape(t('market_advisory_text', lang))}
            </div>
        </div>
        """)

    st.write("")
    st.markdown(f'<div class="pm-section-title">🏪 {t("nearest_mandi", lang)}</div>', unsafe_allow_html=True)

    nearby_mandis = get_nearby_mandis(user_lat, user_lon, limit=6, lang=lang)

    for mandi in nearby_mandis:
        trend_icon = "📈" if mandi["trend"] == "up" else ("📉" if mandi["trend"] == "down" else "⚖️")
        trend_key = f"trend_{mandi['trend']}"
        trend_text = t(trend_key, lang)
        qtl_text = t("qtl_unit", lang)

        render_html(f"""
        <div class="pm-mandi-card">
            <div>
                <div class="pm-mandi-name">🧅 {html.escape(mandi['name'])}</div>
                <div class="pm-mandi-dist">
                    📍 {html.escape(mandi['district'])}, {html.escape(mandi['state'])} &nbsp;•&nbsp;
                    <b>{mandi['distance_km']} km {t('distance_away', lang)}</b> &nbsp;•&nbsp;
                    {t('daily_arrivals_lbl', lang)}: <b>{mandi['arrivals_qtl']:,} {qtl_text}</b>
                </div>
                <div style="margin-top: 6px; font-size: 13px; font-weight: 700;">
                    {trend_icon} <b>{t('price_trend', lang)}:</b> {html.escape(trend_text)}
                </div>
            </div>
            <div>
                <div class="pm-mandi-rate">₹{mandi['modal_price_per_kg']:.2f} <span style="font-size: 14px;">/ 1 kg</span></div>
                <div style="font-size: 12px; color: { '#475569' if theme == 'light' else '#FBCFE8' }; text-align: right; font-weight: 700;">
                    {t('range_lbl', lang)}: ₹{mandi['min_price_per_kg']:.1f} - ₹{mandi['max_price_per_kg']:.1f}/kg
                </div>
            </div>
        </div>
        """)


# =========================================================
# 6. CHAPTER 3: OFFICIAL PDF REPORTS & HISTORY (GOVERNMENT OFFICIAL EXCLUSIVE)
# =========================================================
elif st.session_state.active_chapter == "reports":

    if role != "official":
        st.warning(t("gov_restricted_msg", lang))
    else:
        render_html(f"""
        <div class="pm-hero">
            <h1>📑 {html.escape(t('reports_header', lang))}</h1>
            <p>{html.escape(t('reports_subtitle', lang))}</p>
        </div>
        """)

        raw_records = get_all_records()
        records = [normalize_record(r) for r in raw_records]

        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_query = st.text_input(t("search_records", lang), placeholder=t("search_placeholder", lang))

        with f2:
            grade_filter = st.selectbox(t("filter_grade", lang), [t("all_grades", lang), "Grade A", "Grade B", "Grade C"])

        with f3:
            st.metric(t("total_certified_records", lang), len(records))

        filtered_records = []
        for rec in records:
            match_search = True
            if search_query.strip():
                sq = search_query.lower()
                match_search = (
                    sq in rec["farmer_name"].lower() or
                    sq in rec["lot_id"].lower() or
                    sq in rec["center"].lower() or
                    sq in str(rec["farmer_id"]).lower()
                )

            match_grade = True
            if grade_filter != t("all_grades", lang):
                selected_letter = grade_filter.split()[-1]
                match_grade = (rec["grade"].split("_")[-1] == selected_letter)

            if match_search and match_grade:
                filtered_records.append(rec)

        st.write("")

        if filtered_records:
            for rec in filtered_records:
                grade_letter = rec["grade"].split("_")[-1]
                grade_badge_color = "#15803D" if grade_letter == "A" else ("#C2410C" if grade_letter == "B" else "#DC2626")

                with st.container():
                    render_html(f"""
                    <div class="pm-card" style="border-left: 6px solid {grade_badge_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 18px; font-weight: 900;">
                                🧅 {t('batch_lot_lbl', lang)}: <b>{html.escape(str(rec['lot_id']))}</b> &nbsp;—&nbsp;
                                <span style="color: {grade_badge_color}; font-weight: 900;">{t('grade_badge', lang).upper()} {html.escape(grade_letter)}</span>
                            </div>
                            <div style="font-size: 12px; color: { '#475569' if theme == 'light' else '#FBCFE8' }; font-weight: 700;">
                                🕒 {html.escape(str(rec['timestamp']))}
                            </div>
                        </div>
                        <div style="margin-top: 8px; font-size: 14px; display: flex; flex-wrap: wrap; gap: 18px;">
                            <span>👨‍🌾 <b>{t('farmer_name_lbl', lang)}:</b> {html.escape(str(rec['farmer_name']))}</span>
                            <span>🆔 <b>{t('farmer_id_lbl', lang)}:</b> {html.escape(str(rec['farmer_id']))}</span>
                            <span>⚖ <b>{t('quantity_lbl', lang)}:</b> {rec['quantity']:.0f} kg</span>
                            <span>📍 <b>{t('location_mandi_lbl', lang)}:</b> {html.escape(str(rec['center']))}</span>
                            <span>⭐ <b>{t('quality_score_lbl', lang)}:</b> {rec['quality_score']:.1f}/100</span>
                            <span>🔬 <b>{t('urs_lbl', lang)}:</b> {rec.get('urs_percentage', 2.0):.1f}%</span>
                            <span>🩺 <b>{t('pathology_lbl', lang)}:</b> {html.escape(str(rec.get('disease_name', 'Healthy')))}</span>
                            <span>💰 <b>{t('valuation_lbl', lang)}:</b> ₹{rec.get('price_per_kg', 25.0):.1f}/kg (₹{rec.get('total_value', 2500.0):,.0f})</span>
                        </div>
                        <div style="margin-top: 10px; font-family: monospace; font-size: 11px; color: { '#475569' if theme == 'light' else '#FBCFE8' }; word-break: break-all;">
                            🔐 <b>{t('sha256_seal_lbl', lang)}:</b> {html.escape(str(rec['record_hash']))}
                        </div>
                    </div>
                    """)

                    pdf_data = generate_pdf_report(rec)
                    st.download_button(
                        label=f"{t('btn_download_cert_pdf', lang)} ({rec['lot_id']})",
                        data=pdf_data,
                        file_name=f"PyaazMani_Certificate_{rec['lot_id']}.pdf",
                        mime="application/pdf",
                        key=f"dl_rep_{rec['id']}"
                    )
                    st.write("")
        else:
            st.info(t("no_records", lang))


# =========================================================
# 7. CHAPTER 4: MANDI & APMC ANALYTICS
# =========================================================
elif st.session_state.active_chapter == "analytics":

    render_html(f"""
    <div class="pm-hero">
        <h1>🏛️ {html.escape(t('analytics_header', lang))}</h1>
        <p>{html.escape(t('analytics_subtitle', lang))}</p>
    </div>
    """)

    raw_records = get_all_records()
    all_records = [normalize_record(r) for r in raw_records]

    k1, k2, k3, k4 = st.columns(4)
    total_lots = len(all_records)
    total_qty = sum(r.get("quantity", 0.0) for r in all_records)
    grade_a_cnt = sum(1 for r in all_records if r.get("grade", "").split("_")[-1] == "A")
    grade_b_cnt = sum(1 for r in all_records if r.get("grade", "").split("_")[-1] == "B")
    grade_c_cnt = sum(1 for r in all_records if r.get("grade", "").split("_")[-1] == "C")

    with k1:
        st.metric(t("stat_total_lots", lang), total_lots)
    with k2:
        st.metric(t("stat_total_volume", lang), f"{total_qty:,.0f} kg")
    with k3:
        st.metric(t("stat_grade_a", lang), f"{grade_a_cnt} ({(grade_a_cnt/total_lots*100) if total_lots else 0:.1f}%)")
    with k4:
        st.metric(t("stat_avg_score", lang), f"{(sum(r.get('quality_score', 85.0) for r in all_records)/total_lots) if total_lots else 85.0:.1f} / 100")

    st.write("")

    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        st.subheader(t("chart_grade_dist", lang))
        chart_data = {
            f"{t('grade_badge', lang)} A": grade_a_cnt,
            f"{t('grade_badge', lang)} B": grade_b_cnt,
            f"{t('grade_badge', lang)} C": grade_c_cnt
        }
        st.bar_chart(chart_data)

    with c_chart2:
        st.subheader(t("chart_price_comp", lang))
        mandis_for_chart = get_all_mandis(lang=lang)[:6]
        mandi_rates = {m["name"].split()[0]: m["modal_price_per_kg"] for m in mandis_for_chart}
        st.bar_chart(mandi_rates)

    st.write("")

    st.subheader(t("audit_trail_title", lang))
    if all_records:
        table_rows = []
        for r in all_records:
            table_rows.append({
                t("batch_lot_lbl", lang): r["lot_id"],
                t("farmer_name_lbl", lang): r["farmer_name"],
                t("location_mandi_lbl", lang): r["center"],
                t("quantity_lbl", lang) + " (kg)": r["quantity"],
                t("grade_badge", lang): r["grade"].split("_")[-1],
                t("quality_score_lbl", lang): f"{r['quality_score']:.1f}",
                t("urs_lbl", lang): f"{r.get('urs_percentage', 2.0):.1f}%",
                t("pathology_lbl", lang): r.get("disease_name", "Healthy"),
                "Timestamp": r["timestamp"]
            })
        st.dataframe(table_rows, use_container_width=True)
    else:
        st.info(t("audit_no_data", lang))


# =========================================================
# 8. CHAPTER 5: SETTINGS & DISPLAY PREFERENCES
# =========================================================
elif st.session_state.active_chapter == "settings":

    render_html(f"""
    <div class="pm-hero">
        <h1>⚙️ {html.escape(t('settings_header', lang))}</h1>
        <p>{html.escape(t('settings_subtitle', lang))}</p>
    </div>
    """)

    # Theme Settings
    st.markdown(f'<div class="pm-section-title">🎨 {t("theme_section", lang)}</div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        if st.button(t("theme_light", lang), use_container_width=True, type="primary" if theme == "light" else "secondary", key="set_light"):
            st.session_state.theme = "light"
            st.rerun()

    with t_col2:
        if st.button(t("theme_dark", lang), use_container_width=True, type="primary" if theme == "dark" else "secondary", key="set_dark"):
            st.session_state.theme = "dark"
            st.rerun()

    st.write("")

    # Font Size Settings
    st.markdown(f'<div class="pm-section-title">🔤 {t("font_section", lang)}</div>', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)

    with f_col1:
        if st.button(t("font_normal", lang), use_container_width=True, type="primary" if font_size == "normal" else "secondary", key="font_norm"):
            st.session_state.font_size = "normal"
            st.rerun()

    with f_col2:
        if st.button(t("font_large", lang), use_container_width=True, type="primary" if font_size == "large" else "secondary", key="font_lg"):
            st.session_state.font_size = "large"
            st.rerun()

    with f_col3:
        if st.button(t("font_xlarge", lang), use_container_width=True, type="primary" if font_size == "xlarge" else "secondary", key="font_xl"):
            st.session_state.font_size = "xlarge"
            st.rerun()

    st.write("")

    # Language Settings
    st.markdown(f'<div class="pm-section-title">🌐 {t("lang_section", lang)}</div>', unsafe_allow_html=True)
    l_col1, l_col2, l_col3, l_col4, l_col5, l_col6 = st.columns(6)

    with l_col1:
        if st.button("English", use_container_width=True, type="primary" if lang == "en" else "secondary", key="lang_en_btn"):
            st.session_state.lang = "en"
            st.rerun()

    with l_col2:
        if st.button("हिन्दी (Hindi)", use_container_width=True, type="primary" if lang == "hi" else "secondary", key="lang_hi_btn"):
            st.session_state.lang = "hi"
            st.rerun()

    with l_col3:
        if st.button("ಕನ್ನಡ (Kannada)", use_container_width=True, type="primary" if lang == "kn" else "secondary", key="lang_kn_btn"):
            st.session_state.lang = "kn"
            st.rerun()

    with l_col4:
        if st.button("বাংলা (Bengali)", use_container_width=True, type="primary" if lang == "bn" else "secondary", key="lang_bn_btn"):
            st.session_state.lang = "bn"
            st.rerun()

    with l_col5:
        if st.button("मराठी (Marathi)", use_container_width=True, type="primary" if lang == "mr" else "secondary", key="lang_mr_btn"):
            st.session_state.lang = "mr"
            st.rerun()

    with l_col6:
        if st.button("தமிழ் (Tamil)", use_container_width=True, type="primary" if lang == "ta" else "secondary", key="lang_ta_btn"):
            st.session_state.lang = "ta"
            st.rerun()

    st.write("")

    st.markdown('<div class="pm-section-title">🎙️ Voice Assistant</div>', unsafe_allow_html=True)
    voice_enabled = st.toggle("Enable Voice Assistant", value=st.session_state.voice_assistant, key="voice_assistant_toggle")
    st.session_state.voice_assistant = voice_enabled

    if voice_enabled:
        st.success("Voice assistant is ON. The browser can read the current guidance aloud.")
    else:
        st.info("Voice assistant is OFF. Turn it on to enable spoken guidance.")

    if st.button("🔊 Test Voice Assistant", use_container_width=True, key="voice_assistant_test"):
        speech_text = "Voice assistant is ready. PyaazMani is running." if voice_enabled else "Voice assistant is currently off."
        speak_with_browser_voice(speech_text, language="en-US")

    st.write("")

    # User Profile & Role Settings
    st.markdown(f'<div class="pm-section-title">👤 {t("profile_section", lang)}</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)

    with p1:
        new_u_name = st.text_input(t("display_name_lbl", lang), value=st.session_state.user_name)
        if new_u_name != st.session_state.user_name:
            st.session_state.user_name = new_u_name

    with p2:
        new_u_id = st.text_input(t("assigned_id_lbl", lang), value=st.session_state.user_id)
        if new_u_id != st.session_state.user_id:
            st.session_state.user_id = new_u_id

    with p3:
        st.write("")
        st.write("")
        st.caption(f"{t('active_role_label', lang)}: **{role_display_name}**")


# =========================================================
# 9. FOOTER
# =========================================================
st.markdown("---")
render_html(f"""
<div style="text-align: center; padding: 20px; color: { '#475569' if theme == 'light' else '#FBCFE8' }; font-size: 13px; font-weight: 700;">
    🧅 <b>{t('app_brand', lang)}</b> &nbsp;|&nbsp; {t('app_tagline', lang)}
    <br><br>
    {t('footer_text', lang)}
</div>
""")