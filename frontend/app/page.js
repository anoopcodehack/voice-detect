"use client";

import { useState } from "react";

const SUPPORTED_LANGUAGES = [
  "Tamil",
  "English",
  "Hindi",
  "Malayalam",
  "Telugu",
];

export default function HomePage() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("Tamil");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] || null);
    setResult(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an MP3 file");
      return;
    }

    const API_URL =
      process.env.NEXT_PUBLIC_API_URL +
      "/api/voice-detection";

    const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

    if (!API_URL || !API_KEY) {
      setError("Missing API configuration");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const reader = new FileReader();

    reader.onload = async () => {
      try {
        const base64Audio = reader.result.split(",")[1];

        const res = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
          body: JSON.stringify({
            language,
            audioFormat: "mp3",
            audioBase64: base64Audio,
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data?.detail || "Backend error");
        }

        setResult({
          ...data,
          confidenceScore: Number(data.confidenceScore),
        });
      } catch (err) {
        setError(err.message || "Request failed");
      } finally {
        setLoading(false);
      }
    };

    reader.onerror = () => {
      setError("Failed to read audio file");
      setLoading(false);
    };

    reader.readAsDataURL(file);
  };

 return (
  <div className="container">
    <h1 className="title">AI Voice Detection</h1>

    <div className="card">
      <label className="label">Select Language</label>
      <select
        className="select"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
      >
        {SUPPORTED_LANGUAGES.map((l) => (
          <option key={l} value={l}>
            {l}
          </option>
        ))}
      </select>

      <label className="file-label">
        <span className="mic">🎤</span> Upload Audio
        <input
          className="file"
          type="file"
          accept="audio/mp3"
          onChange={handleFileChange}
        />
      </label>

      <button className="btn" onClick={handleSubmit} disabled={loading}>
        {loading ? "Detecting..." : "Detect Voice"}
      </button>

      {error && <p className="error">{error}</p>}
    </div>

    {result && (
      <div className="result">
        <h2>Detection Result</h2>
        <p>
          <b>Language:</b> {result.language}
        </p>
        <p>
          <b>Classification:</b>{" "}
          <span className={result.classification === "HUMAN" ? "human" : "ai"}>
            {result.classification}
          </span>
        </p>
        <p>
          <b>Confidence:</b> {result.confidenceScore}
        </p>
        <div className="bar">
          <div
            className="fill"
            style={{ width: `${result.confidenceScore * 100}%` }}
          />
        </div>
        <p className="explanation">{result.explanation}</p>
      </div>
    )}

    <style jsx>{`
      .container {
        min-height: 100vh;
        background: #0f172a;
        color: #e5e7eb;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 40px 16px;
        font-family: system-ui, Arial, sans-serif;
      }
      .title {
        font-size: 32px;
        margin-bottom: 24px;
      }
      .card {
        background: #111827;
        padding: 24px;
        border-radius: 12px;
        width: 320px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
      }
      .label {
        font-size: 14px;
        margin-bottom: 6px;
        display: block;
      }
      .select {
        width: 100%;
        padding: 8px;
        margin-bottom: 14px;
        border-radius: 6px;
        border: none;
      }
      .file-label {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px;
        background: #1f2933;
        border-radius: 6px;
        cursor: pointer;
        margin-bottom: 14px;
        font-size: 14px;
        transition: background 0.2s;
      }
      .file-label:hover {
        background: #374151;
      }
      .mic {
        font-size: 18px;
      }
      .file {
        display: none;
      }
      .btn {
        width: 100%;
        padding: 10px;
        background: #6366f1;
        border: none;
        border-radius: 8px;
        color: white;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.1s;
      }
      .btn:hover:not(:disabled) {
        transform: scale(1.03);
      }
      .btn:disabled {
        background: #4b5563;
        cursor: not-allowed;
      }
      .error {
        color: #f87171;
        margin-top: 10px;
      }
      .result {
        margin-top: 30px;
        background: #020617;
        padding: 20px;
        border-radius: 12px;
        width: 360px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
      }
      .human {
        color: #22c55e;
        font-weight: bold;
      }
      .ai {
        color: #ef4444;
        font-weight: bold;
      }
      .bar {
        width: 100%;
        height: 8px;
        background: #1f2933;
        border-radius: 4px;
        margin: 8px 0 14px;
      }
      .fill {
        height: 100%;
        background: #22c55e;
        border-radius: 4px;
      }
      .explanation {
        font-size: 14px;
        color: #9ca3af;
      }
    `}</style>
  </div>
);
}