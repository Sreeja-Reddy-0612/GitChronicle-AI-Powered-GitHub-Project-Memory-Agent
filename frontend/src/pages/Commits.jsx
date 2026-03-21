import { useState } from "react";
import "./Commits.css";

export default function Commits() {
  const data = JSON.parse(localStorage.getItem("repoData"));
  const [expandedCommit, setExpandedCommit] = useState(null);

  if (!data || !data.commits) return <h2 className="container">No Data (Go to Dashboard)</h2>;

  const toggleCommit = (sha) => {
    if (expandedCommit === sha) {
      setExpandedCommit(null);
    } else {
      setExpandedCommit(sha);
    }
  };

  const getBadgeClass = (type) => {
    switch (type?.toLowerCase()) {
      case 'bugfix': return 'badge badge-bugfix';
      case 'feature': return 'badge badge-feature';
      case 'refactor': return 'badge badge-refactor';
      case 'test': return 'badge badge-test';
      case 'maintenance': return 'badge badge-maintenance';
      case 'docs': return 'badge badge-docs';
      default: return 'badge badge-default';
    }
  };

  return (
    <div className="container" style={{ maxWidth: '900px', margin: '0 auto' }}>
      <h1>📝 Commits</h1>
      <p style={{ color: "#9ca3af", marginBottom: "20px" }}>Total Commits: {data.total_commits} | Repository: {data.owner}/{data.repo}</p>

      <div className="commit-list">
        {data.commits.map((commit) => {
          const isExpanded = expandedCommit === commit.sha;

          return (
            <div 
              key={commit.sha} 
              className={`card accordion-card ${isExpanded ? 'expanded' : ''}`}
              onClick={() => toggleCommit(commit.sha)}
            >
              <div className="accordion-header">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                    <span className={getBadgeClass(commit.type)}>{commit.type || 'commit'}</span>
                    <strong style={{ fontSize: '1.1rem' }}>{commit.message.split('\n')[0]}</strong>
                  </div>
                  <div style={{ display: 'flex', gap: '15px', color: '#9ca3af', fontSize: '14px' }}>
                    <span>👤 {commit.author}</span>
                    <span>🕒 {new Date(commit.date).toLocaleString()}</span>
                    <span>🔑 {commit.sha.substring(0, 7)}</span>
                  </div>
                </div>
                <div className="expand-icon">
                  {isExpanded ? '▲' : '▼'}
                </div>
              </div>

              {isExpanded && (
                <div className="accordion-content" onClick={(e) => e.stopPropagation()}>
                  <div style={{ marginBottom: '15px' }}>
                    <strong>Full Message:</strong>
                    <pre style={{ background: '#0f172a', padding: '10px', borderRadius: '6px', whiteSpace: 'pre-wrap', fontFamily: 'inherit', marginTop: '5px' }}>
                      {commit.message}
                    </pre>
                  </div>
                  
                  <div style={{ marginBottom: '15px' }}>
                    <a href={commit.url} target="_blank" rel="noopener noreferrer" className="commit-link">
                      🔗 View Commit on GitHub
                    </a>
                  </div>

                  <div>
                    <strong>Files Changed ({commit.files?.length || 0}):</strong>
                    <div className="files-container">
                      {commit.files?.map((file, idx) => (
                        <div key={idx} className="file-change">
                          <span className="file-name">{file.filename}</span>
                          <div>
                            {file.additions > 0 && <span className="additions">+{file.additions}</span>}
                            {file.deletions > 0 && <span className="deletions">-{file.deletions}</span>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
