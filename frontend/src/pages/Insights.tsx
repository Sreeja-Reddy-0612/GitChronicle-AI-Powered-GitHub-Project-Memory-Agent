import "./Insights.css";

export default function Insights() {
  const data = JSON.parse(localStorage.getItem("repoData") || "null");

  if (!data || !data.insights) return <h2 className="container">No Data (Go to Dashboard)</h2>;

  const insights = data.insights;

  return (
    <div className="container" style={{ maxWidth: "1000px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "5px" }}>📊 Repository Insights</h1>
      <p style={{ color: "#9ca3af", marginBottom: "30px" }}>
        Analyzing <a href={data.repository} target="_blank" rel="noreferrer" style={{ color: "#60a5fa" }}>{data.owner}/{data.repo}</a> ({data.total_commits} commits)
      </p>

      <div className="insights-grid">
        {/* Most Active Developer */}
        <div className="insight-card highlight-card">
          <div className="card-icon">👑</div>
          <h3>Most Active Developer</h3>
          <div className="stat-value">{insights.most_active_developer}</div>
          <p className="card-subtitle">
            {insights.developer_commit_counts?.[insights.most_active_developer]} commits
          </p>
        </div>

        {/* Largest Commit */}
        <div className="insight-card highlight-card">
          <div className="card-icon">🔥</div>
          <h3>Largest Commit</h3>
          <p className="commit-message-preview">
            {insights.largest_commit?.message?.split('\n')[0] || "N/A"}
          </p>
          <div style={{ marginTop: "10px", fontSize: "14px" }}>
            <span style={{ color: "#4ade80" }}>+{insights.largest_commit?.files?.reduce((acc: number, f: any) => acc + f.additions, 0) || 0}</span> / 
            <span style={{ color: "#f87171" }}> -{insights.largest_commit?.files?.reduce((acc: number, f: any) => acc + f.deletions, 0) || 0}</span> lines
          </div>
        </div>
      </div>

      <div className="insights-grid" style={{ marginTop: "20px" }}>
        {/* Commit Distribution */}
        <div className="insight-card">
          <h3>📈 Commit Distribution</h3>
          <div className="distribution-list">
            {insights.commit_type_distribution && Object.entries(insights.commit_type_distribution).map(([k, v]) => (
              <div key={k} className="dist-item">
                <span className="dist-label">{k}</span>
                <span className="dist-value">{v as React.ReactNode}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Most Modified Files */}
        <div className="insight-card">
          <h3>📂 Most Modified Files</h3>
          <div className="files-list">
            {insights.most_modified_files && insights.most_modified_files.map((f: any, i: number) => (
              <div key={i} className="file-item">
                <span className="file-name" title={f.filename}>{f.filename.split('/').pop()}</span>
                <span className="file-changes">{f.changes} edits</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}