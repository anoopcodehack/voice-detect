"use client";

import { useState, useRef } from "react";  // ✅ Added useRef

export default function HomePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detectionResult, setDetectionResult] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const fileInputRef = useRef(null);  // ✅ Added file input ref

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    // Reset result when new file selected
    setDetectionResult(null);
    setShowResult(false);
  };

  const handleDetectVoice = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    setLoading(true);
    setShowResult(false);

    const formData = new FormData();
    formData.append("audio", selectedFile);

    try {
      const response = await fetch("http://localhost:8000/detect", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Backend returned an error");
      }

      const result = await response.json();
      setDetectionResult(result);
      setShowResult(true);
      
    } catch (err) {
      console.error(err);
      alert("Failed to detect voice. Check backend at http://localhost:8000");
    } finally {
      setLoading(false);
    }
  };

  const resetDetection = () => {
    setSelectedFile(null);
    setDetectionResult(null);
    setShowResult(false);
    // ✅ FIXED: Use ref instead of document.querySelector
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      padding: "40px",
      fontFamily: "Arial, sans-serif"
    }}>
      <div style={{ maxWidth: "500px", margin: "0 auto" }}>
        <h1 style={{ 
          color: "white", 
          textAlign: "center", 
          fontSize: "2.5rem", 
          marginBottom: "2rem",
          textShadow: "0 2px 10px rgba(0,0,0,0.3)"
        }}>
          🎙️ AI Voice Detection
        </h1>

        {!showResult ? (
          <>
            <div style={{
              background: "rgba(255,255,255,0.95)",
              padding: "2rem",
              borderRadius: "20px",
              boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
              marginBottom: "1rem"
            }}>
              <label style={{
                display: "block",
                color: "#333",
                fontSize: "1.1rem",
                marginBottom: "1rem",
                fontWeight: "500"
              }}>
                Select Audio File
              </label>
              <input 
                type="file" 
                accept="audio/*" 
                onChange={handleFileChange}
                ref={fileInputRef}  // ✅ FIXED: Added ref here
                style={{
                  width: "100%",
                  padding: "12px",
                  border: "2px dashed #667eea",
                  borderRadius: "10px",
                  background: "white",
                  cursor: "pointer"
                }}
              />
              {selectedFile && (
                <p style={{ marginTop: "10px", color: "#27ae60", fontSize: "0.95rem" }}>
                  ✅ {selectedFile.name}
                </p>
              )}
            </div>

            <button
              style={{
                width: "100%",
                padding: "15px",
                background: loading ? "#bdc3c7" : "#5c5cff",
                color: "#fff",
                border: "none",
                borderRadius: "15px",
                fontSize: "1.2rem",
                fontWeight: "bold",
                cursor: loading ? "not-allowed" : "pointer",
                boxShadow: "0 10px 30px rgba(92, 92, 255, 0.4)",
                transition: "all 0.3s ease"
              }}
              onClick={handleDetectVoice}
              disabled={loading || !selectedFile}
            >
              {loading ? "🔄 Detecting..." : "🚀 Detect Voice"}
            </button>
          </>
        ) : (
          <div style={{
            background: "rgba(255,255,255,0.95)",
            backdropFilter: "blur(20px)",
            padding: "2.5rem",
            borderRadius: "25px",
            textAlign: "center",
            boxShadow: "0 25px 50px rgba(0,0,0,0.15)",
            border: "1px solid rgba(255,255,255,0.2)"
          }}>
            <h2 style={{ 
              color: "#2c3e50", 
              marginBottom: "1.5rem",
              fontSize: "1.8rem"
            }}>
              🎯 Detection Complete!
            </h2>
            
            <div style={{
              fontSize: "3rem",
              fontWeight: "bold",
              margin: "1.5rem 0",
              padding: "1.5rem",
              borderRadius: "20px",
              display: "inline-block",
              background: detectionResult.classification === "Human" ? 
                "rgba(46, 204, 113, 0.2)" : "rgba(231, 76, 60, 0.2)",
              border: `3px solid ${detectionResult.classification === "Human" ? "#27ae60" : "#e74c3c"}`
            }}>
              {detectionResult.classification}
            </div>

            <div style={{
              fontSize: "1.3rem",
              margin: "1.5rem 0",
              color: "#34495e",
              fontWeight: "500"
            }}>
              Confidence: <span style={{
                fontSize: "2.2rem",
                color: "#e67e22",
                fontWeight: "bold"
              }}>
                {(detectionResult.confidence * 100).toFixed(0)}%
              </span>
            </div>

            <div style={{
              textAlign: "left",
              marginTop: "2rem"
            }}>
              <h3 style={{
                color: "#2c3e50",
                marginBottom: "1rem",
                fontSize: "1.3rem"
              }}>📋 Explanation</h3>
              <ul style={{ margin: 0, paddingLeft: "1.5rem" }}>
                {detectionResult.explanation.map((feature, i) => (
                  <li key={i} style={{
                    background: "rgba(52, 152, 219, 0.1)",
                    margin: "0.5rem 0",
                    padding: "1rem",
                    borderRadius: "12px",
                    borderLeft: "4px solid #3498db",
                    fontSize: "1rem",
                    color: "#2c3e50"
                  }}>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            <button
              onClick={resetDetection}
              style={{
                width: "100%",
                marginTop: "2rem",
                padding: "12px",
                background: "#e74c3c",
                color: "white",
                border: "none",
                borderRadius: "12px",
                fontSize: "1.1rem",
                fontWeight: "bold",
                cursor: "pointer",
                boxShadow: "0 8px 25px rgba(231, 76, 60, 0.3)"
              }}
            >
              🔄 Try Another Audio
            </button>
          </div>
        )}
      </div>
    </div>
  );
}




