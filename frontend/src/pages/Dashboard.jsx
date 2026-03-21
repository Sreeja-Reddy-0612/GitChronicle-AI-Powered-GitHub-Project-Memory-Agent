import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeRepo } from "../api/api";

export default function Dashboard() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await analyzeRepo(repoUrl);

      localStorage.setItem("repoData", JSON.stringify(res));

      navigate("/insights");
    } catch (err) {
      alert("Backend error");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>GitHub Project Analyzer</h1>

      <div style={{ marginTop: "20px" }}>
        <input
          placeholder="Enter GitHub repo URL"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />

        <button onClick={handleAnalyze}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>
    </div>
  );
}