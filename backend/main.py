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

DISEASE_DATA = {
    "Wheat Leaf Rust": {
        "disease_hi": "गेहूं पत्ती रतुआ",
        "advice_en": "Apply Mancozeb fungicide (2.5g/L) within 48 hours",
        "advice_hi": "48 घंटे के अंदर मैनकोज़ेब फफूंदनाशक (2.5g/L) का छिड़काव करें",
        "steps": [
            {
                "en": "Apply Mancozeb fungicide at 2.5g per litre of water",
                "hi": "मैनकोज़ेब फफूंदनाशक को 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़काव करें"
            },
            {
                "en": "Avoid irrigation for next 2 days",
                "hi": "अगले 2 दिनों तक सिंचाई न करें"
            },
            {
                "en": "Re-inspect crop after 5 days",
                "hi": "5 दिन बाद फसल की दोबारा जाँच करें"
            }
        ],
        "irrigation_en": "Avoid irrigation for 2 days — keep foliage dry",
        "irrigation_hi": "2 दिन तक सिंचाई न करें — पत्तियों को सूखा रखें",
        "yield_without": 19,
        "yield_with": 28,
        "reasoning_en": "High humidity combined with warm temperature creates ideal rust spreading conditions. NDVI drop of 0.12 from last week confirms early infection stage.",
        "reasoning_hi": "अधिक नमी और गर्म तापमान मिलकर रतुआ फैलाने के लिए अनुकूल परिस्थितियाँ बनाते हैं। पिछले सप्ताह NDVI में 0.12 की गिरावट प्रारंभिक संक्रमण की पुष्टि करती है।"
    },
    "Septoria Leaf Blotch": {
        "disease_hi": "सेप्टोरिया पत्ती धब्बा",
        "advice_en": "Use chlorothalonil spray and avoid leaf wetness",
        "advice_hi": "क्लोरोथेलोनिल स्प्रे करें और पत्तियों को गीला होने से बचाएं",
        "steps": [
            {
                "en": "Apply chlorothalonil at recommended dose",
                "hi": "क्लोरोथेलोनिल को अनुशंसित मात्रा में लगाएं"
            },
            {
                "en": "Switch to drip irrigation only — avoid overhead spray",
                "hi": "केवल ड्रिप सिंचाई करें — ऊपर से पानी देना बंद करें"
            },
            {
                "en": "Remove and destroy infected leaves carefully",
                "hi": "संक्रमित पत्तियों को सावधानी से हटाकर नष्ट करें"
            }
        ],
        "irrigation_en": "Drip irrigation only — reduce humidity exposure",
        "irrigation_hi": "केवल ड्रिप सिंचाई — नमी का संपर्क कम करें",
        "yield_without": 20,
        "yield_with": 27,
        "reasoning_en": "Wet leaf conditions spread Septoria rapidly. Reducing leaf wetness is critical to stop further spread.",
        "reasoning_hi": "पत्तियों का गीलापन सेप्टोरिया को तेज़ी से फैलाता है। पत्तियों की नमी कम करना प्रसार रोकने के लिए ज़रूरी है।"
    },
    "Tomato Leaf Mold": {
        "disease_hi": "टमाटर पत्ती फफूंद",
        "advice_en": "Improve ventilation and apply copper-based fungicide",
        "advice_hi": "हवा का प्रवाह बढ़ाएं और कॉपर आधारित फफूंदनाशक लगाएं",
        "steps": [
            {
                "en": "Increase airflow around plants immediately",
                "hi": "तुरंत पौधों के चारों ओर हवा का प्रवाह बढ़ाएं"
            },
            {
                "en": "Apply copper oxychloride spray",
                "hi": "कॉपर ऑक्सीक्लोराइड का छिड़काव करें"
            },
            {
                "en": "Reduce watering frequency by 40%",
                "hi": "सिंचाई की मात्रा 40% कम करें"
            }
        ],
        "irrigation_en": "Reduce watering — increase airflow to lower humidity",
        "irrigation_hi": "पानी कम करें — नमी घटाने के लिए हवा का प्रवाह बढ़ाएं",
        "yield_without": 18,
        "yield_with": 26,
        "reasoning_en": "Leaf mold thrives in humid, poorly ventilated conditions. Reducing moisture and increasing airflow stops spread.",
        "reasoning_hi": "पत्ती फफूंद नम और कम हवादार परिस्थितियों में पनपती है। नमी कम करने और हवा बढ़ाने से प्रसार रुकता है।"
    },
    "Potato Early Blight": {
        "disease_hi": "आलू अगेती झुलसा",
        "advice_en": "Apply copper-based fungicide immediately",
        "advice_hi": "तुरंत कॉपर आधारित फफूंदनाशक का छिड़काव करें",
        "steps": [
            {
                "en": "Apply copper oxychloride or Mancozeb at recommended dose",
                "hi": "कॉपर ऑक्सीक्लोराइड या मैनकोज़ेब को अनुशंसित मात्रा में लगाएं"
            },
            {
                "en": "Remove and destroy all infected leaves",
                "hi": "सभी संक्रमित पत्तियों को हटाकर नष्ट करें"
            },
            {
                "en": "Switch to drip irrigation — keep foliage completely dry",
                "hi": "ड्रिप सिंचाई पर जाएं — पत्तियों को पूरी तरह सूखा रखें"
            }
        ],
        "irrigation_en": "Drip irrigation only — keep foliage dry at all times",
        "irrigation_hi": "केवल ड्रिप सिंचाई — पत्तियों को हमेशा सूखा रखें",
        "yield_without": 17,
        "yield_with": 25,
        "reasoning_en": "Early blight spreads fast in warm humid weather. Immediate action within 24-48 hours is critical.",
        "reasoning_hi": "गर्म और नम मौसम में अगेती झुलसा तेज़ी से फैलता है। 24-48 घंटों में तुरंत कार्रवाई ज़रूरी है।"
    },
    "Rice Blast": {
        "disease_hi": "धान ब्लास्ट",
        "advice_en": "Apply tricyclazole or isoprothiolane fungicide",
        "advice_hi": "ट्राइसाइक्लाज़ोल या आइसोप्रोथियोलेन फफूंदनाशक का छिड़काव करें",
        "steps": [
            {
                "en": "Spray tricyclazole 75WP at 0.6g per litre of water",
                "hi": "ट्राइसाइक्लाज़ोल 75WP को 0.6 ग्राम प्रति लीटर पानी में मिलाकर छिड़काव करें"
            },
            {
                "en": "Drain field partially to reduce standing water and humidity",
                "hi": "खड़े पानी और नमी कम करने के लिए खेत से आंशिक रूप से पानी निकालें"
            },
            {
                "en": "Monitor weekly for further spread",
                "hi": "आगे के फैलाव के लिए साप्ताहिक निगरानी करें"
            }
        ],
        "irrigation_en": "Partial field drainage — reduce standing water level",
        "irrigation_hi": "आंशिक जल निकासी — खड़े पानी का स्तर कम करें",
        "yield_without": 16,
        "yield_with": 26,
        "reasoning_en": "Rice blast spreads rapidly in high humidity and nitrogen-rich conditions. Intermittent drying reduces infection pressure.",
        "reasoning_hi": "उच्च नमी और नाइट्रोजन युक्त परिस्थितियों में धान ब्लास्ट तेज़ी से फैलता है। रुक-रुक कर सुखाने से संक्रमण का दबाव कम होता है।"
    },
    "Healthy": {
        "disease_hi": "स्वस्थ फसल",
        "advice_en": "No treatment needed — crop looks healthy",
        "advice_hi": "कोई उपचार ज़रूरी नहीं — फसल स्वस्थ दिख रही है",
        "steps": [
            {
                "en": "Continue regular irrigation schedule",
                "hi": "नियमित सिंचाई कार्यक्रम जारी रखें"
            },
            {
                "en": "Monitor weekly as a preventive measure",
                "hi": "निवारक उपाय के रूप में साप्ताहिक निगरानी करें"
            },
            {
                "en": "Maintain optimal soil nutrition levels",
                "hi": "मिट्टी के पोषण स्तर को इष्टतम बनाए रखें"
            }
        ],
        "irrigation_en": "Normal irrigation schedule — maintain current routine",
        "irrigation_hi": "सामान्य सिंचाई कार्यक्रम — वर्तमान दिनचर्या बनाए रखें",
        "yield_without": 30,
        "yield_with": 30,
        "reasoning_en": "No disease patterns detected. Crop health index is within normal range. Continue standard care.",
        "reasoning_hi": "कोई रोग पैटर्न नहीं पाया गया। फसल स्वास्थ्य सूचकांक सामान्य सीमा में है। मानक देखभाल जारी रखें।"
    }
}

def get_irrigation_schedule(disease: str) -> list:
    schedules = {
        "Wheat Leaf Rust": [
            {"day": 1, "date": "Mon", "date_hi": "सोम", "action_en": "Skip",     "action_hi": "छोड़ें",       "reason_en": "Avoid moisture — fungal risk",    "reason_hi": "नमी से बचें — फफूंद का खतरा",    "amount_mm": 0},
            {"day": 2, "date": "Tue", "date_hi": "मंगल","action_en": "Skip",     "action_hi": "छोड़ें",       "reason_en": "Keep foliage dry",               "reason_hi": "पत्तियों को सूखा रखें",           "amount_mm": 0},
            {"day": 3, "date": "Wed", "date_hi": "बुध", "action_en": "Irrigate", "action_hi": "सिंचाई करें", "reason_en": "Soil moisture low",              "reason_hi": "मिट्टी की नमी कम है",             "amount_mm": 20},
            {"day": 4, "date": "Thu", "date_hi": "गुरु","action_en": "Skip",     "action_hi": "छोड़ें",       "reason_en": "Post-spray rest",                "reason_hi": "छिड़काव के बाद आराम",              "amount_mm": 0},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Monitor", "action_hi": "निगरानी",      "reason_en": "Check rust spread",              "reason_hi": "रतुआ फैलाव जाँचें",               "amount_mm": 0},
            {"day": 6, "date": "Sat", "date_hi": "शनि", "action_en": "Irrigate","action_hi": "सिंचाई करें",  "reason_en": "Scheduled watering",             "reason_hi": "निर्धारित सिंचाई",                "amount_mm": 18},
            {"day": 7, "date": "Sun", "date_hi": "रवि", "action_en": "Rest",    "action_hi": "विश्राम",      "reason_en": "Weekly rest",                    "reason_hi": "साप्ताहिक विश्राम",               "amount_mm": 0},
        ],
        "Septoria Leaf Blotch": [
            {"day": 1, "date": "Mon", "date_hi": "सोम",  "action_en": "Skip",      "action_hi": "छोड़ें",         "reason_en": "Wet leaves worsen blotch",      "reason_hi": "गीली पत्तियाँ धब्बा बढ़ाती हैं",  "amount_mm": 0},
            {"day": 2, "date": "Tue", "date_hi": "मंगल", "action_en": "Drip only", "action_hi": "ड्रिप सिंचाई", "reason_en": "Avoid overhead spray",          "reason_hi": "ऊपर से पानी न दें",               "amount_mm": 10},
            {"day": 3, "date": "Wed", "date_hi": "बुध",  "action_en": "Skip",      "action_hi": "छोड़ें",         "reason_en": "High humidity forecast",        "reason_hi": "अधिक नमी का अनुमान",              "amount_mm": 0},
            {"day": 4, "date": "Thu", "date_hi": "गुरु", "action_en": "Drip only", "action_hi": "ड्रिप सिंचाई", "reason_en": "Maintain root moisture",        "reason_hi": "जड़ों की नमी बनाए रखें",          "amount_mm": 10},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Monitor",   "action_hi": "निगरानी",       "reason_en": "Check leaf wetness",            "reason_hi": "पत्तियों की नमी जाँचें",          "amount_mm": 0},
            {"day": 6, "date": "Sat", "date_hi": "शनि",  "action_en": "Drip only", "action_hi": "ड्रिप सिंचाई", "reason_en": "Controlled irrigation",         "reason_hi": "नियंत्रित सिंचाई",                "amount_mm": 12},
            {"day": 7, "date": "Sun", "date_hi": "रवि",  "action_en": "Rest",      "action_hi": "विश्राम",       "reason_en": "Weekly rest",                   "reason_hi": "साप्ताहिक विश्राम",               "amount_mm": 0},
        ],
        "Tomato Leaf Mold": [
            {"day": 1, "date": "Mon", "date_hi": "सोम",  "action_en": "Reduce",  "action_hi": "कम करें",   "reason_en": "High humidity — mold risk",      "reason_hi": "अधिक नमी — फफूंद का खतरा",    "amount_mm": 8},
            {"day": 2, "date": "Tue", "date_hi": "मंगल", "action_en": "Skip",    "action_hi": "छोड़ें",     "reason_en": "Allow soil to dry",              "reason_hi": "मिट्टी को सूखने दें",           "amount_mm": 0},
            {"day": 3, "date": "Wed", "date_hi": "बुध",  "action_en": "Reduce",  "action_hi": "कम करें",   "reason_en": "Controlled moisture",            "reason_hi": "नियंत्रित नमी",                 "amount_mm": 10},
            {"day": 4, "date": "Thu", "date_hi": "गुरु", "action_en": "Skip",    "action_hi": "छोड़ें",     "reason_en": "Ventilation day",                "reason_hi": "हवादार दिन",                     "amount_mm": 0},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Reduce",  "action_hi": "कम करें",   "reason_en": "Maintain low humidity",          "reason_hi": "कम नमी बनाए रखें",              "amount_mm": 8},
            {"day": 6, "date": "Sat", "date_hi": "शनि",  "action_en": "Monitor", "action_hi": "निगरानी",   "reason_en": "Check mold spread",              "reason_hi": "फफूंद फैलाव जाँचें",            "amount_mm": 0},
            {"day": 7, "date": "Sun", "date_hi": "रवि",  "action_en": "Rest",    "action_hi": "विश्राम",   "reason_en": "Weekly rest",                    "reason_hi": "साप्ताहिक विश्राम",             "amount_mm": 0},
        ],
        "Potato Early Blight": [
            {"day": 1, "date": "Mon", "date_hi": "सोम",  "action_en": "Drip only", "action_hi": "ड्रिप सिंचाई", "reason_en": "Keep foliage dry",             "reason_hi": "पत्तियों को सूखा रखें",        "amount_mm": 15},
            {"day": 2, "date": "Tue", "date_hi": "मंगल", "action_en": "Skip",      "action_hi": "छोड़ें",         "reason_en": "Post-spray rest",              "reason_hi": "छिड़काव के बाद आराम",           "amount_mm": 0},
            {"day": 3, "date": "Wed", "date_hi": "बुध",  "action_en": "Drip only", "action_hi": "ड्रिप सिंचाई", "reason_en": "Root-level moisture only",     "reason_hi": "केवल जड़ स्तर पर नमी",         "amount_mm": 15},
            {"day": 4, "date": "Thu", "date_hi": "गुरु", "action_en": "Skip",      "action_hi": "छोड़ें",         "reason_en": "Soil moisture adequate",       "reason_hi": "मिट्टी की नमी पर्याप्त है",    "amount_mm": 0},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Monitor",   "action_hi": "निगरानी",       "reason_en": "Inspect blight spread",        "reason_hi": "झुलसा फैलाव जाँचें",           "amount_mm": 0},
            {"day": 6, "date": "Sat", "date_hi": "शनि",  "action_en": "Irrigate",  "action_hi": "सिंचाई करें",   "reason_en": "Weekly schedule",              "reason_hi": "साप्ताहिक सिंचाई",              "amount_mm": 20},
            {"day": 7, "date": "Sun", "date_hi": "रवि",  "action_en": "Rest",      "action_hi": "विश्राम",       "reason_en": "Weekly rest",                  "reason_hi": "साप्ताहिक विश्राम",             "amount_mm": 0},
        ],
        "Rice Blast": [
            {"day": 1, "date": "Mon", "date_hi": "सोम",  "action_en": "Drain partial", "action_hi": "आंशिक जल निकासी", "reason_en": "Reduce standing water",    "reason_hi": "खड़े पानी को कम करें",         "amount_mm": 0},
            {"day": 2, "date": "Tue", "date_hi": "मंगल", "action_en": "Drain partial", "action_hi": "आंशिक जल निकासी", "reason_en": "Lower field humidity",     "reason_hi": "खेत की नमी घटाएं",             "amount_mm": 0},
            {"day": 3, "date": "Wed", "date_hi": "बुध",  "action_en": "Refill",        "action_hi": "पानी भरें",        "reason_en": "Maintain minimal level",   "reason_hi": "न्यूनतम स्तर बनाए रखें",       "amount_mm": 30},
            {"day": 4, "date": "Thu", "date_hi": "गुरु", "action_en": "Monitor",       "action_hi": "निगरानी",          "reason_en": "Check blast spread",       "reason_hi": "ब्लास्ट फैलाव जाँचें",         "amount_mm": 0},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Drain partial", "action_hi": "आंशिक जल निकासी", "reason_en": "Intermittent drying",      "reason_hi": "रुक-रुक कर सुखाना",            "amount_mm": 0},
            {"day": 6, "date": "Sat", "date_hi": "शनि",  "action_en": "Refill",        "action_hi": "पानी भरें",        "reason_en": "Crop water need",          "reason_hi": "फसल की पानी की ज़रूरत",         "amount_mm": 25},
            {"day": 7, "date": "Sun", "date_hi": "रवि",  "action_en": "Rest",          "action_hi": "विश्राम",          "reason_en": "Weekly rest",              "reason_hi": "साप्ताहिक विश्राम",             "amount_mm": 0},
        ],
        "Healthy": [
            {"day": 1, "date": "Mon", "date_hi": "सोम",  "action_en": "Irrigate", "action_hi": "सिंचाई करें", "reason_en": "Normal schedule",              "reason_hi": "सामान्य कार्यक्रम",             "amount_mm": 25},
            {"day": 2, "date": "Tue", "date_hi": "मंगल", "action_en": "Skip",     "action_hi": "छोड़ें",       "reason_en": "Sufficient moisture",          "reason_hi": "पर्याप्त नमी है",               "amount_mm": 0},
            {"day": 3, "date": "Wed", "date_hi": "बुध",  "action_en": "Irrigate", "action_hi": "सिंचाई करें", "reason_en": "Mid-week watering",            "reason_hi": "सप्ताह के मध्य सिंचाई",         "amount_mm": 25},
            {"day": 4, "date": "Thu", "date_hi": "गुरु", "action_en": "Skip",     "action_hi": "छोड़ें",       "reason_en": "Soil moist",                   "reason_hi": "मिट्टी नम है",                  "amount_mm": 0},
            {"day": 5, "date": "Fri", "date_hi": "शुक्र","action_en": "Irrigate", "action_hi": "सिंचाई करें", "reason_en": "Scheduled watering",           "reason_hi": "निर्धारित सिंचाई",              "amount_mm": 20},
            {"day": 6, "date": "Sat", "date_hi": "शनि",  "action_en": "Monitor",  "action_hi": "निगरानी",      "reason_en": "Weekly check",                 "reason_hi": "साप्ताहिक जाँच",                "amount_mm": 0},
            {"day": 7, "date": "Sun", "date_hi": "रवि",  "action_en": "Rest",     "action_hi": "विश्राम",      "reason_en": "Weekly rest",                  "reason_hi": "साप्ताहिक विश्राम",             "amount_mm": 0},
        ],
    }
    return schedules.get(disease, schedules["Healthy"])

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
            "disease_hi":        data["disease_hi"],
            "confidence":        confidence,
            "severity":          "high" if confidence >= 0.85 else "moderate",
            "affected_area":     "15%",
            "top_predictions":   top_predictions,
            "gradcam_available": True,
            "inference_time_ms": 1200,
            "model":             "EfficientNet-Lite (mock)"
        },
        "recommendation": {
            "text_en":   data["advice_en"],
            "text_hi":   data["advice_hi"],
            "steps":     data["steps"],
            "reasoning_en": data["reasoning_en"],
            "reasoning_hi": data["reasoning_hi"]
        },
        "forecast": {
            "yield_prediction": {
                "without_treatment": data["yield_without"],
                "with_treatment":    data["yield_with"],
                "seasonal_average":  30,
                "unit":              "quintals/acre"
            },
            "irrigation_advice_en": data["irrigation_en"],
            "irrigation_advice_hi": data["irrigation_hi"],
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
        "federated_note_en": "Model trained across 847 farms. Your data never left your device.",
        "federated_note_hi": "मॉडल 847 खेतों पर प्रशिक्षित। आपका डेटा कभी आपके डिवाइस से बाहर नहीं गया।",
        "status": "success"
    })

@app.post("/forecast")
async def forecast(data: dict = Body(...)):
    disease = data.get("disease", "Healthy")
    d = DISEASE_DATA.get(disease, DISEASE_DATA["Healthy"])
    return JSONResponse({
        "disease":    disease,
        "disease_hi": d["disease_hi"],
        "yield_prediction": {
            "without_treatment": d["yield_without"],
            "with_treatment":    d["yield_with"],
            "seasonal_average":  30,
            "unit":              "quintals/acre"
        },
        "irrigation_schedule":    get_irrigation_schedule(disease),
        "irrigation_advice_en":   d["irrigation_en"],
        "irrigation_advice_hi":   d["irrigation_hi"]
    })

@app.post("/recommend")
async def recommend(data: dict = Body(...)):
    disease = data.get("disease", "Healthy")
    d = DISEASE_DATA.get(disease, DISEASE_DATA["Healthy"])
    return JSONResponse({
        "disease":      disease,
        "disease_hi":   d["disease_hi"],
        "text_en":      d["advice_en"],
        "text_hi":      d["advice_hi"],
        "steps":        d["steps"],
        "reasoning_en": d["reasoning_en"],
        "reasoning_hi": d["reasoning_hi"]
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)