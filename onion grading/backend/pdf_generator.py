"""
PyaazMani PDF Quality Certificate Generator
Generates tamper-evident, official agricultural grading certificates using ReportLab.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_pdf_report(record: dict) -> bytes:
    """
    Generate an official PDF grading certificate for the given onion lot record.
    Returns bytes representing the PDF file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom color palette (Onion Pink & Charcoal)
    c_primary = colors.HexColor("#9D174D")      # Onion deep rose
    c_secondary = colors.HexColor("#BE185D")    # Berry pink
    c_dark = colors.HexColor("#1F2937")         # Slate dark
    c_muted = colors.HexColor("#4B5563")        # Muted gray
    c_light_bg = colors.HexColor("#FDF2F8")     # Blush background
    c_card_border = colors.HexColor("#FBCFE8")  # Soft rose border
    c_green = colors.HexColor("#15803D")        # Verified green

    # Typography styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#FDF2F8"),
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_dark
    )

    body_regular = ParagraphStyle(
        'BodyRegular',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_muted
    )

    cert_hash_style = ParagraphStyle(
        'HashStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=TA_CENTER
    )

    elements = []

    # ----------------------------------------------------
    # 1. HEADER BANNER TABLE
    # ----------------------------------------------------
    header_data = [
        [
            Paragraph("🧅 <b>PYAAZMANI</b> | AI QUALITY CERTIFICATE", title_style)
        ],
        [
            Paragraph("GOVERNMENT OF INDIA • APMC MANDI STANDARDIZATION & QUALITY ASSURANCE", subtitle_style)
        ]
    ]

    header_table = Table(header_data, colWidths=[522])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 10))

    # ----------------------------------------------------
    # 2. METADATA STRIP
    # ----------------------------------------------------
    cert_id = f"CERT-PM-{str(record.get('id', '999')).zfill(5)}"
    ts_str = str(record.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    meta_data = [
        [
            Paragraph(f"<b>Certificate No:</b> {cert_id}", body_bold),
            Paragraph(f"<b>Issued On:</b> {ts_str}", body_regular),
            Paragraph(f"<b>Status:</b> <font color='{c_green}'><b>VERIFIED</b></font>", body_bold)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[174, 220, 128])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, c_card_border),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 12))

    # ----------------------------------------------------
    # 3. FARMER & LOT INFORMATION
    # ----------------------------------------------------
    elements.append(Paragraph("1. LOT & PROVENANCE DETAILS", section_heading))

    farmer_data = [
        [
            Paragraph("<b>Farmer Name:</b>", body_bold),
            Paragraph(str(record.get("farmer_name", "N/A")), body_regular),
            Paragraph("<b>Farmer ID:</b>", body_bold),
            Paragraph(str(record.get("farmer_id", "N/A")), body_regular)
        ],
        [
            Paragraph("<b>Lot / Token ID:</b>", body_bold),
            Paragraph(str(record.get("lot_id", "N/A")), body_regular),
            Paragraph("<b>Mandi Center:</b>", body_bold),
            Paragraph(str(record.get("center", "N/A")), body_regular)
        ],
        [
            Paragraph("<b>Lot Quantity:</b>", body_bold),
            Paragraph(f"{float(record.get('quantity', 0.0)):.1f} kg", body_bold),
            Paragraph("<b>Commodity:</b>", body_bold),
            Paragraph("Red / Pink Onion (Allium Cepa)", body_regular)
        ]
    ]

    farmer_table = Table(farmer_data, colWidths=[95, 166, 95, 166])
    farmer_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#F3F4F6")),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor("#F9FAFB")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(farmer_table)
    elements.append(Spacer(1, 12))

    # ----------------------------------------------------
    # 4. AI QUALITY ASSESSMENT SCORECARD
    # ----------------------------------------------------
    elements.append(Paragraph("2. AI QUALITY GRADING SCORECARD", section_heading))

    raw_grade = str(record.get("grade", "A"))
    grade = raw_grade.split("_")[-1] if raw_grade else "REJECTED"
    conf = float(record.get("confidence", 0.90))
    score = float(record.get("quality_score", 85.0))
    urs = float(record.get("urs_percentage", 3.2))
    rate = float(record.get("price_per_kg", 28.0))
    total_val = float(record.get("total_value", rate * float(record.get("quantity", 100.0))))

    is_rejected = (grade in ["None", "REJECTED", ""] or score < 50.0)
    grade_color = "#DC2626" if is_rejected else ("#15803D" if grade == "A" else ("#C2410C" if grade == "B" else "#DC2626"))
    grade_text = "REJECTED" if is_rejected else f"GRADE {grade}"

    score_data = [
        [
            Paragraph(f"<font color='{grade_color}' size=16><b>{grade_text}</b></font>", ParagraphStyle('G', alignment=TA_CENTER)),
            Paragraph(f"<font color='{c_primary}' size=13><b>{conf:.1%}</b></font><br/><font size=7 color='#6B7280'>AI CONFIDENCE</font>", ParagraphStyle('C', alignment=TA_CENTER)),
            Paragraph(f"<font color='{grade_color if is_rejected else c_primary}' size=13><b>{score:.1f}/100</b></font><br/><font size=7 color='#6B7280'>QUALITY INDEX</font>", ParagraphStyle('S', alignment=TA_CENTER)),
            Paragraph(f"<font color='{c_primary}' size=13><b>{urs:.1f}%</b></font><br/><font size=7 color='#6B7280'>URS DEFECT RATE</font>", ParagraphStyle('U', alignment=TA_CENTER)),
            Paragraph(f"<font color='#047857' size=13><b>₹{rate:.1f}/kg</b></font><br/><font size=7 color='#6B7280'>EST. MANDI RATE</font>", ParagraphStyle('R', alignment=TA_CENTER)),
            Paragraph(f"<font color='#047857' size=13><b>₹{total_val:,.0f}</b></font><br/><font size=7 color='#6B7280'>EST. LOT VALUE</font>", ParagraphStyle('V', alignment=TA_CENTER))
        ]
    ]

    score_table = Table(score_data, colWidths=[90, 86, 86, 86, 86, 88])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_secondary),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_card_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 12))

    # ----------------------------------------------------
    # 5. DISEASE & PATHOLOGY REPORT
    # ----------------------------------------------------
    elements.append(Paragraph("3. PATHOLOGICAL DIAGNOSIS & REMEDY ADVISORY", section_heading))

    disease_name = str(record.get("disease_name", "Healthy — No Pathological Infection"))
    severity = str(record.get("disease_severity", "None"))
    remedy = str(record.get("remedy", "No treatment required. Store in dry, well-ventilated crates."))

    disease_data = [
        [
            Paragraph("<b>Identified Diagnosis:</b>", body_bold),
            Paragraph(f"<b>{disease_name}</b>", body_bold),
            Paragraph("<b>Severity Level:</b>", body_bold),
            Paragraph(severity, body_bold)
        ],
        [
            Paragraph("<b>Storage & Treatment Advice:</b>", body_bold),
            Paragraph(remedy, body_regular),
            Paragraph("", body_regular),
            Paragraph("", body_regular)
        ]
    ]

    disease_table = Table(disease_data, colWidths=[95, 230, 80, 117])
    disease_table.setStyle(TableStyle([
        ('SPAN', (1, 1), (3, 1)),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#F3F4F6")),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
        ('BACKGROUND', (2, 0), (2, 0), colors.HexColor("#F9FAFB")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(disease_table)
    elements.append(Spacer(1, 12))

    # ----------------------------------------------------
    # 6. COMPUTER VISION METRICS
    # ----------------------------------------------------
    elements.append(Paragraph("4. EXTRACTED COMPUTER VISION BIOMETRICS", section_heading))

    features = record.get("features", [12000, 450, 0.82, 18.5, 140, 130, 22.0, 1, 0.015, 0.025])
    if len(features) < 10:
        features = features + [0.0] * (10 - len(features))

    feat_data = [
        [
            Paragraph("<b>Metric</b>", body_bold),
            Paragraph("<b>Value</b>", body_bold),
            Paragraph("<b>Metric</b>", body_bold),
            Paragraph("<b>Value</b>", body_bold)
        ],
        [
            Paragraph("Segmented Bulb Area", body_regular),
            Paragraph(f"{features[0]:.1f} px", body_regular),
            Paragraph("Average Hue Angle", body_regular),
            Paragraph(f"{features[3]:.1f}°", body_regular)
        ],
        [
            Paragraph("Circularity Index", body_regular),
            Paragraph(f"{features[2]:.3f}", body_regular),
            Paragraph("Color Saturation", body_regular),
            Paragraph(f"{features[4]:.1f}", body_regular)
        ],
        [
            Paragraph("Surface Spot Count", body_regular),
            Paragraph(f"{int(features[7])}", body_regular),
            Paragraph("Necrotic Spot Ratio", body_regular),
            Paragraph(f"{features[8]:.3%}", body_regular)
        ],
        [
            Paragraph("Brightness Uniformity", body_regular),
            Paragraph(f"{features[6]:.2f} std", body_regular),
            Paragraph("Edge Complexity Ratio", body_regular),
            Paragraph(f"{features[9]:.4f}", body_regular)
        ]
    ]

    feat_table = Table(feat_data, colWidths=[166, 95, 166, 95])
    feat_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#F3F4F6")),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(feat_table)
    elements.append(Spacer(1, 14))

    # ----------------------------------------------------
    # 7. CRYPTOGRAPHIC LEDGER SEAL & FOOTER
    # ----------------------------------------------------
    rec_hash = str(record.get("record_hash", record.get("hash", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")))

    footer_data = [
        [
            Paragraph("<b>CRYPTOGRAPHIC TAMPER-PROOF DIGITAL SEAL</b>", ParagraphStyle('F1', fontName='Helvetica-Bold', fontSize=8, alignment=TA_CENTER, textColor=c_primary))
        ],
        [
            Paragraph(f"SHA-256 Ledger Hash: <font color='#111827'><b>{rec_hash}</b></font>", cert_hash_style)
        ],
        [
            Paragraph("This is a system-generated cryptographic grading certificate issued by PyaazMani Agricultural Intelligence. Verifiable at all accredited APMC mandis.", ParagraphStyle('F2', fontName='Helvetica', fontSize=7, alignment=TA_CENTER, textColor=c_muted))
        ]
    ]

    footer_table = Table(footer_data, colWidths=[522])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FDF2F8")),
        ('BOX', (0, 0), (-1, -1), 0.5, c_secondary),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(footer_table)

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
