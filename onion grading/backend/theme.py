"""
PyaazMani Theme Engine
High-contrast Onion Pink Styling with Light & Dark Mode + Custom Uploader & Dropzone.
"""

def get_theme_css(theme: str = "light", font_size: str = "normal") -> str:
    """Generate scoped CSS tailored for Onion Pink palette with high text contrast."""
    
    # Font scale multiplier
    if font_size == "xlarge":
        base_size = "19px"
        h1_size = "38px"
        h2_size = "28px"
        h3_size = "22px"
        metric_size = "34px"
        btn_size = "19px"
    elif font_size == "large":
        base_size = "17px"
        h1_size = "34px"
        h2_size = "25px"
        h3_size = "20px"
        metric_size = "30px"
        btn_size = "17px"
    else:  # normal
        base_size = "15px"
        h1_size = "30px"
        h2_size = "22px"
        h3_size = "18px"
        metric_size = "26px"
        btn_size = "15px"

    is_dark = (theme == "dark")

    if is_dark:
        bg_main = "#12050D"
        bg_card = "#1F0A17"
        bg_card_hover = "#2A0D20"
        bg_card_alt = "#260C1D"
        border_color = "rgba(244, 114, 182, 0.28)"
        text_primary = "#FFFFFF"
        text_secondary = "#FBCFE8"
        text_muted = "#F472B6"
        primary_pink = "#EC4899"
        primary_pink_hover = "#DB2777"
        rose_accent = "#FB7185"
        shadow_card = "0 8px 24px rgba(0, 0, 0, 0.55)"
        nav_bg = "linear-gradient(135deg, #2D0C22 0%, #4A1033 100%)"
        hero_bg = "linear-gradient(135deg, #3B0D2B 0%, #58123E 50%, #831843 100%)"
        grade_a_bg = "linear-gradient(135deg, #14532D, #16A34A)"
        grade_b_bg = "linear-gradient(135deg, #7C2D12, #EA580C)"
        grade_c_bg = "linear-gradient(135deg, #7F1D1D, #DC2626)"
        badge_bg = "rgba(236, 72, 153, 0.25)"
        tile_bg = "linear-gradient(145deg, #250B1B 0%, #340E27 100%)"
        tile_border = "#EC4899"
        uploader_bg = "#1F0A17"
    else:
        # High-Contrast Light Mode with Dark Charcoal/Black Text
        bg_main = "#FDF2F4"
        bg_card = "#FFFFFF"
        bg_card_hover = "#FFF5F8"
        bg_card_alt = "#FCE7EC"
        border_color = "rgba(190, 24, 93, 0.22)"
        text_primary = "#0F172A"       # Deep dark slate (100% visible)
        text_secondary = "#1E293B"     # Dark charcoal
        text_muted = "#334155"         # High-contrast slate
        primary_pink = "#BE185D"       # Deep Onion Rose
        primary_pink_hover = "#9D174D"
        rose_accent = "#E11D48"
        shadow_card = "0 6px 20px rgba(190, 24, 93, 0.09)"
        nav_bg = "linear-gradient(135deg, #831843 0%, #9D174D 50%, #BE185D 100%)"
        hero_bg = "linear-gradient(135deg, #831843 0%, #BE185D 50%, #DB2777 100%)"
        grade_a_bg = "linear-gradient(135deg, #15803D, #22C55E)"
        grade_b_bg = "linear-gradient(135deg, #C2410C, #F97316)"
        grade_c_bg = "linear-gradient(135deg, #B91C1C, #EF4444)"
        badge_bg = "rgba(255, 255, 255, 0.22)"
        tile_bg = "linear-gradient(145deg, #FFFFFF 0%, #FFF1F5 100%)"
        tile_border = "rgba(190, 24, 93, 0.3)"
        uploader_bg = "#FFFFFF"

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Noto+Sans+Kannada:wght@400;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Noto Sans Kannada', sans-serif !important;
        font-size: {base_size};
        background-color: {bg_main} !important;
        color: {text_primary} !important;
    }}

    p, span, label, div, h1, h2, h3, h4, h5, h6 {{
        color: {text_primary};
    }}

    .stMarkdown, .stText {{
        color: {text_primary} !important;
    }}

    /* Global Container */
    .block-container {{
        max-width: 1280px;
        padding-top: 0.8rem;
        padding-bottom: 3.5rem;
    }}

    /* Top Brand Navigation Bar */
    .pm-navbar {{
        background: {nav_bg};
        padding: 14px 22px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 18px;
        box-shadow: {shadow_card};
        border: 1px solid {border_color};
    }}

    .pm-brand-wrap {{
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: nowrap;
        white-space: nowrap;
    }}

    .pm-brand {{
        color: #FFFFFF !important;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap !important;
    }}

    .pm-brand span {{
        color: #FCE7F3 !important;
        white-space: nowrap !important;
    }}

    .pm-tagline {{
        color: #FDF2F8 !important;
        font-size: 13px;
        opacity: 0.92;
        font-weight: 600;
        white-space: nowrap;
    }}

    .pm-role-pill {{
        background: {badge_bg};
        color: #FFFFFF !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.35);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
    }}

    /* Chapter Tiles Grid (Matching Reference Screenshot) */
    .pm-tile-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 20px;
        margin-top: 14px;
        margin-bottom: 24px;
    }}

    .pm-chapter-card {{
        background: {tile_bg};
        border: 2px solid {tile_border};
        border-radius: 24px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: {shadow_card};
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 200px;
    }}

    .pm-chapter-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(190, 24, 93, 0.22);
        border-color: {primary_pink};
    }}

    .pm-chapter-icon {{
        font-size: 52px;
        margin-bottom: 12px;
        line-height: 1;
    }}

    .pm-chapter-title {{
        font-size: 18px;
        font-weight: 800;
        color: {text_primary} !important;
        margin-bottom: 6px;
    }}

    .pm-chapter-desc {{
        font-size: 13px;
        color: {text_muted} !important;
        line-height: 1.4;
        font-weight: 600;
    }}

    /* Hero Banner */
    .pm-hero {{
        background: {hero_bg};
        padding: 28px 32px;
        border-radius: 20px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        box-shadow: {shadow_card};
        position: relative;
        overflow: hidden;
    }}

    .pm-hero h1 {{
        color: #FFFFFF !important;
        font-size: {h1_size};
        font-weight: 900;
        line-height: 1.2;
        margin: 0 0 8px 0;
    }}

    .pm-hero p {{
        color: #FDF2F8 !important;
        font-size: {base_size};
        line-height: 1.5;
        max-width: 760px;
        margin: 0;
        opacity: 0.95;
        font-weight: 500;
    }}

    /* Standard Cards */
    .pm-card {{
        background: {bg_card};
        border-radius: 18px;
        padding: 22px;
        border: 1px solid {border_color};
        box-shadow: {shadow_card};
        margin-bottom: 18px;
    }}

    .pm-card-title {{
        font-size: {h3_size};
        font-weight: 800;
        color: {text_primary} !important;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .pm-card-text {{
        color: {text_secondary} !important;
        font-size: {base_size};
        line-height: 1.5;
        font-weight: 600;
    }}

    /* Upload Box Card */
    .pm-upload-box {{
        background: {bg_card};
        border: 2px dashed {primary_pink};
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        box-shadow: {shadow_card};
        margin-bottom: 14px;
    }}

    .pm-upload-icon {{
        background: #FFFFFF;
        color: {primary_pink};
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }}

    /* Streamlit File Uploader Custom Styling (Pure White Button Text with 100% Contrast) */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {uploader_bg} !important;
        border: 2px dashed {border_color} !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }}

    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {primary_pink} !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 22px !important;
        box-shadow: 0 4px 12px rgba(190, 24, 93, 0.3) !important;
    }}

    [data-testid="stFileUploaderDropzone"] button *, [data-testid="stFileUploaderDropzone"] button span, [data-testid="stFileUploaderDropzone"] button svg {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }}

    [data-testid="stFileUploaderDropzone"] button:hover {{
        background-color: {primary_pink_hover} !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stFileUploaderDropzone"] [data-testid="stMarkdownContainer"] p {{
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stFileUploaderDropzone"] small {{
        color: {text_muted} !important;
        font-weight: 600 !important;
    }}

    /* Grade Display Box */
    .pm-grade-box {{
        padding: 24px 20px;
        border-radius: 20px;
        text-align: center;
        color: #FFFFFF !important;
        margin-bottom: 16px;
        box-shadow: {shadow_card};
    }}

    .pm-grade-box.grade-a {{
        background: {grade_a_bg};
    }}

    .pm-grade-box.grade-b {{
        background: {grade_b_bg};
    }}

    .pm-grade-box.grade-c {{
        background: {grade_c_bg};
    }}

    .pm-grade-box h1 {{
        color: #FFFFFF !important;
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
    }}

    .pm-grade-box p {{
        color: #FFFFFF !important;
        font-size: 16px;
        font-weight: 700;
        margin: 4px 0 0 0;
    }}

    /* Disease Box */
    .pm-disease-box {{
        background: {bg_card_alt};
        border: 1px solid {border_color};
        border-left: 6px solid {rose_accent};
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 14px;
        margin-bottom: 14px;
    }}

    .pm-disease-title {{
        font-size: {h3_size};
        font-weight: 800;
        color: {text_primary} !important;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}

    .pm-disease-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 800;
    }}

    .badge-healthy {{
        background: #DCFCE7;
        color: #15803D !important;
    }}

    .badge-warning {{
        background: #FEF3C7;
        color: #B45309 !important;
    }}

    .badge-danger {{
        background: #FEE2E2;
        color: #B91C1C !important;
    }}

    /* Metric Tiles */
    .pm-metric-tile {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: {shadow_card};
    }}

    .pm-metric-val {{
        font-size: {metric_size};
        font-weight: 900;
        color: {primary_pink} !important;
    }}

    .pm-metric-lbl {{
        font-size: 13px;
        font-weight: 700;
        color: {text_secondary} !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }}

    /* Section Headings */
    .pm-section-title {{
        font-size: {h2_size};
        font-weight: 900;
        color: {text_primary} !important;
        margin-top: 8px;
        margin-bottom: 6px;
    }}

    .pm-section-subtitle {{
        font-size: {base_size};
        color: {text_secondary} !important;
        font-weight: 500;
        margin-bottom: 16px;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {primary_pink} !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: {btn_size} !important;
        border: none !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(190, 24, 93, 0.25) !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        background-color: {primary_pink_hover} !important;
        transform: translateY(-1px) !important;
    }}

    .stDownloadButton > button {{
        background-color: #047857 !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: {btn_size} !important;
        border: none !important;
        padding: 10px 20px !important;
    }}

    /* Mandi Pricing Card */
    .pm-mandi-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: {shadow_card};
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .pm-mandi-name {{
        font-size: {h3_size};
        font-weight: 800;
        color: {text_primary} !important;
    }}

    .pm-mandi-dist {{
        font-size: 13px;
        font-weight: 600;
        color: {text_muted} !important;
    }}

    .pm-mandi-rate {{
        font-size: 28px;
        font-weight: 900;
        color: {primary_pink} !important;
        text-align: right;
    }}

    /* Streamlit Input Labels & Values */
    .stTextInput label, .stNumberInput label, .stSelectbox label {{
        color: {text_primary} !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }}

    .stTextInput input, .stNumberInput input, .stSelectbox select {{
        border-radius: 10px !important;
        border: 1.5px solid {border_color} !important;
        background-color: {bg_card} !important;
        color: {text_primary} !important;
        font-weight: 600 !important;
    }}

    /* Mobile Responsive Optimizations */
    @media (max-width: 768px) {{
        .pm-navbar {{
            flex-direction: column;
            gap: 10px;
            align-items: flex-start;
            padding: 12px 16px;
        }}
        .pm-tagline {{
            display: none;
        }}
        .pm-hero {{
            padding: 20px 18px;
        }}
        .pm-hero h1 {{
            font-size: 24px;
        }}
        .pm-tile-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        .pm-chapter-card {{
            padding: 18px 12px;
            min-height: 160px;
        }}
        .pm-chapter-icon {{
            font-size: 40px;
        }}
        .pm-chapter-title {{
            font-size: 15px;
        }}
    }}
</style>
"""
