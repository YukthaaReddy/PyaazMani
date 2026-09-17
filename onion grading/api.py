from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from backend.auth import ROLES
from backend.database import get_all_records, initialize_database
from backend.i18n import TRANSLATIONS
from backend.mandi_service import get_all_mandis, get_nearby_mandis
from backend.pdf_generator import generate_pdf_report
from backend.service import analyze_onion, save_grading_result


app = FastAPI(title="PyaazMani API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
initialize_database()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "pyaazmani"}


@app.get("/api/bootstrap")
def bootstrap(lang: str = "en"):
    roles = {
        key: {
            "id": value["id"], "name": value.get(f"name_{lang}", value["name"]),
            "icon": value["icon"], "default_user": value["default_user"],
            "default_name": value["default_name"], "allowed_fragments": value["allowed_fragments"],
            "badge_color": value["badge_color"],
        }
        for key, value in ROLES.items()
    }
    return {"roles": roles, "mandis": get_all_mandis(lang=lang)}


@app.get("/api/translations")
def translations(lang: str = "en"):
    values = dict(TRANSLATIONS["en"])
    values.update(TRANSLATIONS.get(lang, {}))
    return values


@app.get("/api/mandis")
def mandis(lat: float = 20.0059, lon: float = 73.7898, lang: str = "en"):
    return {"items": get_nearby_mandis(lat, lon, limit=6, lang=lang)}


@app.post("/api/analyze")
async def analyze(
    image: UploadFile = File(...), farmer_name: str = Form(...), farmer_id: str = Form(...),
    lot_id: str = Form(...), center: str = Form(...), quantity: float = Form(...),
    role: str = Form("farmer"), lang: str = Form("en"),
):
    suffix = Path(image.filename or "onion.jpg").suffix or ".jpg"
    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded image is empty.")
    temp_path = None
    try:
        with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        return analyze_onion(image_path=temp_path, farmer_name=farmer_name, farmer_id=farmer_id, lot_id=lot_id, center=center, quantity=quantity, role=role, lang=lang)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


@app.post("/api/records")
def save_record(payload: dict):
    if not payload.get("record"):
        raise HTTPException(status_code=400, detail="A grading result is required.")
    return save_grading_result(payload)


@app.get("/api/records")
def records():
    return {"items": get_all_records()}


@app.get("/api/records/{record_id}/pdf")
def record_pdf(record_id: int):
    record = next((item for item in get_all_records() if item["id"] == record_id), None)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")
    return Response(content=generate_pdf_report(record), media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="PyaazMani_{record["lot_id"]}.pdf"'})


@app.get("/api/analytics")
def analytics():
    items = get_all_records()
    total_lots = len(items)
    grade_counts = {grade: sum(1 for item in items if str(item.get("grade", "")).split("_")[-1] == grade and float(item.get("quality_score", 0)) >= 50.0) for grade in "ABC"}
    grade_counts["REJECTED"] = sum(1 for item in items if str(item.get("grade", "")) in ["REJECTED", "None", ""] or float(item.get("quality_score", 0)) < 50.0)
    return {
        "total_lots": total_lots,
        "total_quantity": sum(item.get("quantity", 0) for item in items),
        "grade_counts": grade_counts,
        "average_score": round(sum(item.get("quality_score", 0) for item in items) / total_lots, 1) if items else 0,
    }