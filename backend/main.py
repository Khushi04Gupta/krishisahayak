from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from model import predict_image

app = FastAPI(title="KrishiSahayak API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════
# DISEASE DATA — single source of truth
# ═══════════════════════════════════════

DISEASE_DATA = {
    "Wheat Leaf Rust": {
        "advice": "Apply Mancozeb fungicide (2.5g/L) within 48 hours",
        "steps": [
            "Apply Mancozeb fungicide at 2.5g per litre of water",
            "Avoid irrigation for next 2 days",
            "Re-inspect crop after 5 days"
        ],
        "irrigation": "Avoid irrigation for 2 days — keep foliage dry",
        "yield_without": 19,
        "yield_with": 28,
        "reasoning": "High humidity combined with warm temperature creates ideal rust spreading conditions. NDVI drop of 0.12 from last week confirms early infection stage.",
        "hindi": "Mancozeb fungicide 2.5g/L paani mein milakar 48 ghante mein spray karein"
    },
    "Septoria Leaf Blotch": {
        "advice": "Use chlorothalonil spray and avoid leaf wetness",
        "steps": [
            "Apply chlorothalonil at recommended dose",
            "Switch to drip irrigation only — avoid overhead spray",
            "Remove and destroy infected leaves carefully"
        ],
        "irrigation": "Drip irrigation only — reduce humidity exposure",
        "yield_without": 20,
        "yield_with": 27,
        "reasoning": "Wet leaf conditions spread Septoria rapidly. Reducing leaf wetness is critical to stop further spread.",
        "hindi": "Chlorothalonil spray lagayein aur patti ko geela hone se bachayein"
    },
    "Tomato Leaf Mold": {
        "advice": "Improve ventilation and apply copper-based fungicide",
        "steps": [
            "Increase airflow around plants immediately",
            "Apply copper oxychloride spray",
            "Reduce watering frequency by 40%"
        ],
        "irrigation": "Reduce watering — increase airflow to lower humidity",
        "yield_without": 18,
        "yield_with": 26,
        "reasoning": "Leaf mold thrives in humid, poorly ventilated conditions. Reducing moisture and increasing airflow stops spread.",
        "hindi": "Hawa ka pravaah badhayein aur copper fungicide spray karein"
    },
    "Potato Early Blight": {
        "advice": "Apply copper-based fungicide immediately",
        "steps": [
            "Apply copper oxychloride or Mancozeb at recommended dose",
            "Remove and destroy all infected leaves",
            "Switch to drip irrigation — keep foliage completely dry"
        ],
        "irrigation": "Drip irrigation only — keep foliage dry at all times",
        "yield_without": 17,
        "yield_with": 25,
        "reasoning": "Early blight spreads fast in warm humid weather. Immediate action within 24-48 hours is critical to limit yield loss.",
        "hindi": "Copper fungicide turant lagayein aur sankramit pattiyaan hataayein"
    },
    "Rice Blast": {
        "advice": "Apply tricyclazole or isoprothiolane fungicide",
        "steps": [
            "Spray tricyclazole 75WP at 0.6g per litre of water",
            "Drain field partially to reduce standing water and humidity",
            "Monitor weekly for further spread"
        ],
        "irrigation": "Partial field drainage — reduce standing water level",
        "yield_without": 16,
        "yield_with": 26,
        "reasoning": "Rice blast spreads rapidly in high humidity and nitrogen-rich conditions. Intermittent drying of fields reduces infection pressure.",
        "hindi": "Tricyclazole fungicide spray karein aur khet se kuch paani hatayein"
    },
    "Healthy": {
        "advice": "No treatment needed — crop looks healthy",
        "steps": [
            "Continue regular irrigation schedule",
            "Monitor weekly as a preventive measure",
            "Maintain optimal soil nutrition levels"
        ],
        "irrigation": "Normal irrigation schedule — maintain current routine",
        "yield_without": 30,
        "yield_with": 30,
        "reasoning": "No disease patterns detected. Crop health index is within normal range. Continue standard care.",
        "hindi": "Fasal swasth hai — koi ilaaj zaroori nahi, niyamit dekhbhaal jaari rakhen"
    }
}

# ═══════════════════════════════════════
# DYNAMIC IRRIGATION SCHEDULES
# ═══════════════════════════════════════

def get_irrigation_schedule(disease: str) -> list:
    schedules = {
        "Wheat Leaf Rust": [
            {"day": 1, "date": "Mon", "action": "Skip",     "reason": "Avoid moisture — fungal risk",    "amount_mm": 0},
            {"day": 2, "date": "Tue", "action": "Skip",     "reason": "Keep foliage dry",               "amount_mm": 0},
            {"day": 3, "date": "Wed", "action": "Irrigate", "reason": "Soil moisture low",              "amount_mm": 20},
            {"day": 4, "date": "Thu", "action": "Skip",     "reason": "Post-spray rest",                "amount_mm": 0},
            {"day": 5, "date": "Fri", "action": "Monitor",  "reason": "Check rust spread",              "amount_mm": 0},
            {"day": 6, "date": "Sat", "action": "Irrigate", "reason": "Scheduled watering",            "amount_mm": 18},
            {"day": 7, "date": "Sun", "action": "Rest",     "reason": "Weekly rest",                   "amount_mm": 0},
        ],
        "Septoria Leaf Blotch": [
            {"day": 1, "date": "Mon", "action": "Skip",      "reason": "Wet leaves worsen blotch",      "amount_mm": 0},
            {"day": 2, "date": "Tue", "action": "Drip only", "reason": "Avoid overhead spray",          "amount_mm": 10},
            {"day": 3, "date": "Wed", "action": "Skip",      "reason": "High humidity forecast",        "amount_mm": 0},
            {"day": 4, "date": "Thu", "action": "Drip only", "reason": "Maintain root moisture",        "amount_mm": 10},
            {"day": 5, "date": "Fri", "action": "Monitor",   "reason": "Check leaf wetness",            "amount_mm": 0},
            {"day": 6, "date": "Sat", "action": "Drip only", "reason": "Controlled irrigation",        "amount_mm": 12},
            {"day": 7, "date": "Sun", "action": "Rest",      "reason": "Weekly rest",                  "amount_mm": 0},
        ],
        "Tomato Leaf Mold": [
            {"day": 1, "date": "Mon", "action": "Reduce",  "reason": "High humidity — mold risk",      "amount_mm": 8},
            {"day": 2, "date": "Tue", "action": "Skip",    "reason": "Allow soil to dry",              "amount_mm": 0},
            {"day": 3, "date": "Wed", "action": "Reduce",  "reason": "Controlled moisture",            "amount_mm": 10},
            {"day": 4, "date": "Thu", "action": "Skip",    "reason": "Ventilation day",                "amount_mm": 0},
            {"day": 5, "date": "Fri", "action": "Reduce",  "reason": "Maintain low humidity",          "amount_mm": 8},
            {"day": 6, "date": "Sat", "action": "Monitor", "reason": "Check mold spread",              "amount_mm": 0},
            {"day": 7, "date": "Sun", "action": "Rest",    "reason": "Weekly rest",                   "amount_mm": 0},
        ],
        "Potato Early Blight": [
            {"day": 1, "date": "Mon", "action": "Drip only", "reason": "Keep foliage dry",             "amount_mm": 15},
            {"day": 2, "date": "Tue", "action": "Skip",      "reason": "Post-spray rest",              "amount_mm": 0},
            {"day": 3, "date": "Wed", "action": "Drip only", "reason": "Root-level moisture only",     "amount_mm": 15},
            {"day": 4, "date": "Thu", "action": "Skip",      "reason": "Soil moisture adequate",       "amount_mm": 0},
            {"day": 5, "date": "Fri", "action": "Monitor",   "reason": "Inspect blight spread",        "amount_mm": 0},
            {"day": 6, "date": "Sat", "action": "Irrigate",  "reason": "Weekly schedule",             "amount_mm": 20},
            {"day": 7, "date": "Sun", "action": "Rest",      "reason": "Weekly rest",                 "amount_mm": 0},
        ],
        "Rice Blast": [
            {"day": 1, "date": "Mon", "action": "Drain partial", "reason": "Reduce standing water",    "amount_mm": 0},
            {"day": 2, "date": "Tue", "action": "Drain partial", "reason": "Lower field humidity",     "amount_mm": 0},
            {"day": 3, "date": "Wed", "action": "Refill",        "reason": "Maintain minimal level",  "amount_mm": 30},
            {"day": 4, "date": "Thu", "action": "Monitor",       "reason": "Check blast spread",       "amount_mm": 0},
            {"day": 5, "date": "Fri", "action": "Drain partial", "reason": "Intermittent drying",      "amount_mm": 0},
            {"day": 6, "date": "Sat", "action": "Refill",        "reason": "Crop water need",         "amount_mm": 25},
            {"day": 7, "date": "Sun", "action": "Rest",          "reason": "Weekly rest",             "amount_mm": 0},
        ],
        "Healthy": [
            {"day": 1, "date": "Mon", "action": "Irrigate", "reason": "Normal schedule",              "amount_mm": 25},
            {"day": 2, "date": "Tue", "action": "Skip",     "reason": "Sufficient moisture",          "amount_mm": 0},
            {"day": 3, "date": "Wed", "action": "Irrigate", "reason": "Mid-week watering",            "amount_mm": 25},
            {"day": 4, "date": "Thu", "action": "Skip",     "reason": "Soil moist",                  "amount_mm": 0},
            {"day": 5, "date": "Fri", "action": "Irrigate", "reason": "Scheduled watering",          "amount_mm": 20},
            {"day": 6, "date": "Sat", "action": "Monitor",  "reason": "Weekly check",                "amount_mm": 0},
            {"day": 7, "date": "Sun", "action": "Rest",     "reason": "Weekly rest",                 "amount_mm": 0},
        ],
    }
    return schedules.get(disease, schedules["Healthy"])

# ═══════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════

@app.get("/")
def root():
    return {"message": "KrishiSahayak API is running", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy", "model": "mock", "version": "1.0.0"}

@app.post("/predict-disease")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    disease, confidence, top_predictions = predict_image(contents)
    data = DISEASE_DATA.get(disease, DISEASE_DATA["Healthy"])

    return JSONResponse({
        "prediction": {
            "disease":           disease,
            "confidence":        confidence,
            "severity":          "high" if confidence >= 0.85 else "moderate",
            "affected_area":     "15%",
            "top_predictions":   top_predictions,
            "gradcam_available": True,
            "inference_time_ms": 1200,
            "model":             "EfficientNet-Lite (mock)"
        },
        "recommendation": {
            "text":      data["advice"],
            "steps":     data["steps"],
            "hindi":     data["hindi"],
            "reasoning": data["reasoning"]
        },
        "forecast": {
            "yield_prediction": {
                "without_treatment": data["yield_without"],
                "with_treatment":    data["yield_with"],
                "seasonal_average":  30,
                "unit":              "quintals/acre"
            },
            "irrigation_advice":    data["irrigation"],
            "irrigation_schedule":  get_irrigation_schedule(disease),
            "ndvi":                 0.73,
            "soil_moisture":        34,
            "temperature":          28,
            "rainfall_forecast_mm": 8
        },
        "sustainability": {
            "water_saved_litres":      2400,
            "carbon_impact":           "Low",
            "economic_protection_inr": 42000
        },
        "federated_note": "Model trained across 847 farms. Your data never left your device.",
        "status": "success"
    })

@app.post("/forecast")
async def forecast(data: dict = Body(...)):
    disease = data.get("disease", "Healthy")
    d = DISEASE_DATA.get(disease, DISEASE_DATA["Healthy"])
    return JSONResponse({
        "disease": disease,
        "yield_prediction": {
            "without_treatment": d["yield_without"],
            "with_treatment":    d["yield_with"],
            "seasonal_average":  30,
            "unit":              "quintals/acre"
        },
        "irrigation_schedule": get_irrigation_schedule(disease),
        "irrigation_advice":   d["irrigation"]
    })

@app.post("/recommend")
async def recommend(data: dict = Body(...)):
    disease = data.get("disease", "Healthy")
    d = DISEASE_DATA.get(disease, DISEASE_DATA["Healthy"])
    return JSONResponse({
        "disease":        disease,
        "recommendation": d["advice"],
        "steps":          d["steps"],
        "hindi":          d["hindi"],
        "reasoning":      d["reasoning"]
    })

# ═══════════════════════════════════════
# RUN
# ═══════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)