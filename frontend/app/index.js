"use client";

import { useState } from "react";

const SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"];

export default function HomePage() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState(SUPPORTED_LANGUAGES[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Use environment variables for Vercel
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an MP3 file");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onload = async () => {
      const base64Audio = reader.result.split(",")[1]; // remove prefix
      const payload = {
        language,
        audioFormat: "mp3",
        audioBase64: base64Audio,
      };

      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
          body: JSON.stringify(payload),
        });

        let data;
        try {
          data = await res.json();
        } catch {
          setError("Invalid response from backend");
          setLoading(false);
          return;
        }

        if (data.status === "success") {
          setResult(data);
        } else {
          setError(data.message || JSON.stringify(data));
        }
      } catch (err) {
        setError("Network error: " + err.message);
      } finally {
        setLoading(false);
      }
    };
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>AI Voice Detection</h1>

      <div style={{ margin: "1rem 0" }}>
        <label>
          Select Language:{" "}
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            {SUPPORTED_LANGUAGES.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div style={{ margin: "1rem 0" }}>
        <input type="file" accept="audio/mp3" onChange={handleFileChange} />
      </div>

      <button onClick={handleSubmit} disabled={loading || !file}>
        {loading ? "Detecting..." : "Detect Voice"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "1rem" }}>
          {error}
        </p>
      )}

      {result && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <p><b>Language:</b> {result.language}</p>
          <p><b>Classification:</b> {result.classification}</p>
          <p><b>Confidence Score:</b> {result.confidenceScore}</p>
          <p><b>Explanation:</b> {result.explanation}</p>
        </div>
      )}
    </div>
  );
}








