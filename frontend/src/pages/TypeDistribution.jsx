import { useMemo } from 'react';
import './TypeDistribution.css';

const TYPE_COLORS = {
  feature: '#4ade80',     // green
  bugfix: '#f87171',      // red
  refactor: '#fbbf24',    // yellow
  docs: '#60a5fa',        // blue
  test: '#a78bfa',        // purple
  optimization: '#2dd4bf',// teal
  chore: '#a1a1aa',       // gray
  other: '#9ca3af',
  maintenance: '#f472b6'  // pink
};

export default function TypeDistribution() {
  const data = JSON.parse(localStorage.getItem('repoData'));

  if (!data || !data.commits) return <h2 className="container">No Data (Go to Dashboard)</h2>;

  const typeCounts = useMemo(() => {
    const counts = {};
    data.commits.forEach(commit => {
      const type = (commit.type || 'other').toLowerCase();
      counts[type] = (counts[type] || 0) + 1;
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [data.commits]);

  const totalClassified = typeCounts.reduce((acc, curr) => acc + curr[1], 0);

  return (
    <div className="container type-dist-container" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div className="type-dist-header">
        <h1>📊 Commit Type Distribution</h1>
        <p style={{ color: '#9ca3af' }}>Semantic Multi-Label Analysis for <a href={data.repository} target="_blank" rel="noreferrer" style={{ color: "#60a5fa" }}>{data.owner}/{data.repo}</a></p>
      </div>

      <div className="commit-type-bar">
        {typeCounts.map(([type, count]) => (
          <div
            key={type}
            className="bar-segment"
            style={{
              width: `${(count / totalClassified) * 100}%`,
              background: TYPE_COLORS[type] || TYPE_COLORS.other
            }}
            title={`${type}: ${count} commits (${((count / totalClassified) * 100).toFixed(1)}%)`}
          >
            {((count / totalClassified) * 100) > 5 ? type : ''}
          </div>
        ))}
      </div>

      <div className="type-dist-grid">
        {typeCounts.map(([type, count]) => (
          <div key={type} className="type-card">
            <h3>
              <span className="breakdown-color" style={{ background: TYPE_COLORS[type] || TYPE_COLORS.other }} />
              <span style={{ textTransform: 'capitalize' }}>{type}</span>
            </h3>
            <div className="type-card-value">{count}</div>
            <p style={{ textAlign: 'center', color: '#9ca3af', margin: 0 }}>commits ({(count / totalClassified * 100).toFixed(1)}%)</p>
          </div>
        ))}
      </div>

      <div className="commit-dist-list">
        <h2>📑 Commit-Level Type Distribution</h2>
        {data.commits.map((commit) => (
          <div key={commit.sha} className="commit-dist-card">
            <div className="commit-dist-header">
              <div className="commit-dist-title">
                {commit.message.split('\n')[0]}
              </div>
              <div className="commit-dist-sha">
                {commit.sha.substring(0, 7)}
              </div>
            </div>
            
            <div style={{ marginBottom: "12px" }}>
              <span className="dist-stat-badge" style={{ display: 'inline-flex', background: TYPE_COLORS[commit.type?.toLowerCase()] || TYPE_COLORS.other, color: '#000', fontWeight: 'bold' }}>
                Overall Type: {commit.type || 'N/A'}
              </span>
            </div>

            <div className="commit-dist-stats">
              {commit.type_distribution && Object.entries(commit.type_distribution).map(([type, score]) => (
                <div key={type} className="dist-stat-badge">
                  <span className="dist-stat-color" style={{ background: TYPE_COLORS[type?.toLowerCase()] || TYPE_COLORS.other }}></span>
                  <span style={{ textTransform: 'capitalize' }}>{type}</span>: {Number(score).toFixed(3)}
                </div>
              ))}
              {!commit.type_distribution && <span style={{ color: '#9ca3af', fontSize: '13px' }}>No distribution data available.</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
