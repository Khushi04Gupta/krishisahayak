import { useState } from "react";

const API = "http://localhost:8000";

export default function AgroSenseDashboard() {
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lang, setLang] = useState("both");

  const t = (en, hi) => {
    if (lang === "hi") return hi;
    if (lang === "en") return en;
    return `${en} / ${hi}`;
  };

  // 📷 Upload
  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API}/predict-disease`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Backend not running!");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      
      <h1>🌱 {t("KrishiSahayak Dashboard", "कृषि सहायक डैशबोर्ड")}</h1>

      {/* Language */}
      <div>
        <button onClick={() => setLang("en")}>EN</button>
        <button onClick={() => setLang("hi")}>HI</button>
        <button onClick={() => setLang("both")}>Both</button>
      </div>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>

        {/* Upload */}
        <div style={cardStyle}>
          <h3>{t("Upload Image", "तस्वीर अपलोड करें")}</h3>
          <input type="file" onChange={handleImageUpload} />

          {preview && (
            <img src={preview} alt="" style={{ width: "100%", marginTop: "10px" }} />
          )}
        </div>

        {/* Result */}
        <div style={cardStyle}>
          <h3>{t("Prediction", "परिणाम")}</h3>

          {loading ? (
            <p>{t("Analyzing...", "विश्लेषण...")}</p>
          ) : result ? (
            <>
              <p>
                🌿 {t("Disease", "रोग")}:{" "}
                {t(
                  result.prediction.disease,
                  result.prediction.disease_hi
                )}
              </p>

              <p>
                🎯 {t("Confidence", "विश्वास")}:{" "}
                {Math.round(result.prediction.confidence * 100)}%
              </p>

              <p>
                ⚠️ {t("Severity", "गंभीरता")}:{" "}
                {result.prediction.severity}
              </p>
            </>
          ) : (
            <p>No result</p>
          )}
        </div>

        {/* Recommendation */}
        <div style={cardStyle}>
          <h3>{t("Recommendation", "सुझाव")}</h3>

          {result && (
            <>
              <p>
                {t(
                  result.recommendation.text_en,
                  result.recommendation.text_hi
                )}
              </p>

              <ul>
                {result.recommendation.steps.map((s, i) => (
                  <li key={i}>
                    {t(s.en, s.hi)}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        {/* Irrigation */}
        <div style={cardStyle}>
          <h3>{t("Irrigation Plan", "सिंचाई योजना")}</h3>

          {result &&
            result.forecast.irrigation_schedule.map((d, i) => (
              <p key={i}>
                {t(d.date, d.date_hi)} -{" "}
                {t(d.action_en, d.action_hi)} ({d.amount_mm}mm)
              </p>
            ))}
        </div>

        {/* Yield */}
        <div style={cardStyle}>
          <h3>{t("Yield Prediction", "उत्पादन अनुमान")}</h3>

          {result && (
            <>
              <p>
                ❌ {t("Without", "बिना इलाज")}:{" "}
                {result.forecast.yield_prediction.without_treatment}
              </p>
              <p>
                ✅ {t("With", "इलाज के बाद")}:{" "}
                {result.forecast.yield_prediction.with_treatment}
              </p>
            </>
          )}
        </div>

        {/* Sustainability */}
        <div style={cardStyle}>
          <h3>{t("Sustainability", "स्थिरता")}</h3>

          {result && (
            <>
              <p>
                💧 {result.sustainability.water_saved_litres} L saved
              </p>
              <p>
                💰 ₹{result.sustainability.economic_protection_inr}
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

const cardStyle = {
  border: "1px solid #ddd",
  padding: "15px",
  borderRadius: "10px",
  width: "300px",
};