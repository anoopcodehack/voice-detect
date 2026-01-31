// app/result/page.js
"use client";

import { useEffect, useState } from "react";

export default function ResultPage() {
  const [data, setData] = useState(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem("result");
    if (stored) {
      try {
        setData(JSON.parse(stored));
      } catch (e) {
        console.error("Failed to parse result from localStorage", e);
      }
    }
  }, []);

  if (!mounted) return null;

  if (!data) return <p style={{ padding: 40 }}>No result found.</p>;

  const confidencePercent = Math.round((data.confidence ?? 0) * 100);

  return (
    <main style={{ padding: 40 }}>
      <h2>AI Voice Detection Result</h2>
      <h3>{data.classification || "Unknown"}</h3>
      <progress value={confidencePercent} max="100" style={{ width: "300px", height: "20px" }} />
      <p>Confidence: {confidencePercent}%</p>
      <h4>Explanation</h4>
      {data.explanation && data.explanation.length > 0 ? (
        <ul>
          {data.explanation.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>No explanation available.</p>
      )}
    </main>
  );
}
