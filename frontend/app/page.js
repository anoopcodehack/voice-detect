"use client";

import { useState } from "react";

const API_URL = "https://voice-detect-1-c20t.onrender.com/api/voice-detection"; // Your backend
const API_KEY = "sk_test_123456789"; // Your API key
const SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"];

export default function HomePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [language, setLanguage] = useState(SUPPORTED_LANGUAGES[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (!selectedFile) return setError("Please select an MP3 file first");
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const reader = new FileReader();
      reader.readAsDataURL(selectedFile);
      reader.onload = async () => {
        const base64Audio = reader.result.split(",")[1];

        const payload = {
          language,
          audioFormat: "mp3",
          audioBase64: base64Audio,
        };

        const response = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.status === "success") {
          setResult(data);
        } else {
          setError(data.message || JSON.stringify(data));
        }
        setLoading(false);
      };
    } catch (err) {
      setError("Error sending request: " + err.message);
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>AI Voice Detection</h1>
      <div style={{ marginBottom: "1rem" }}>
        <label>
          Select Language:{" "}
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option key={lang} value={lang}>
                {lang}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <input type="file" accept="audio/mp3" onChange={handleFileChange} />
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Detecting..." : "Detect Voice"}
      </button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {result && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <h2>Result</h2>
          <p>
            <b>Language:</b> {result.language}
          </p>
          <p>
            <b>Classification:</b> {result.classification}
          </p>
          <p>
            <b>Confidence Score:</b> {result.confidenceScore}
          </p>
          <p>
            <b>Explanation:</b> {result.explanation}
          </p>
        </div>
      )}
    </div>
  );
}







