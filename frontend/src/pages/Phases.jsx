import { useState } from "react";
import "./Phases.css";

export default function Phases() {
  const data = JSON.parse(localStorage.getItem("repoData"));
  const [expandedPhase, setExpandedPhase] = useState(null);

  if (!data || !data.development_phases) return <h2 className="container">No Data (Go to Dashboard)</h2>;

  const togglePhase = (phaseId) => {
    setExpandedPhase(expandedPhase === phaseId ? null : phaseId);
  };

  const getBadgeClass = (type) => {
    switch (type?.toLowerCase()) {
      case 'bugfix': return 'phase-badge badge-bugfix';
      case 'feature': return 'phase-badge badge-feature';
      case 'refactor': return 'phase-badge badge-refactor';
      case 'test': return 'phase-badge badge-test';
      case 'maintenance': return 'phase-badge badge-maintenance';
      case 'docs': return 'phase-badge badge-docs';
      default: return 'phase-badge badge-default';
    }
  };

  return (
    <div className="container" style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h1>📌 Development Phases</h1>
      <p style={{ color: "#9ca3af", marginBottom: "30px" }}>Phases detected by AI analysis</p>

      <div className="phases-list">
        {data.development_phases.map((phase, index) => {
          const isExpanded = expandedPhase === phase.phase_number;
          
          return (
            <div 
              key={phase.phase_number || index} 
              className={`phase-card ${isExpanded ? 'phase-expanded' : ''}`}
              onClick={() => togglePhase(phase.phase_number)}
            >
              <div className="phase-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                  <div className="phase-number">{phase.phase_number}</div>
                  <div>
                    <h2 style={{ margin: 0, fontSize: '1.2rem', color: '#f8fafc' }}>{phase.phase_name}</h2>
                    <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>{phase.commit_count} commits</span>
                  </div>
                </div>
                <div className="phase-expand-icon">
                  {isExpanded ? '▲' : '▼'}
                </div>
              </div>

              {isExpanded && (
                <div className="phase-content" onClick={(e) => e.stopPropagation()}>
                  <div className="phase-commits">
                    {phase.commits && phase.commits.map((c) => (
                      <div key={c.sha} className="phase-commit-item">
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                          <strong style={{ color: '#e2e8f0', fontSize: '0.95rem' }}>{c.message.split('\n')[0]}</strong>
                          <span className={getBadgeClass(c.type)}>{c.type}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#94a3b8' }}>
                          <span>👤 {c.author}</span>
                          <a href={c.url} target="_blank" rel="noopener noreferrer" style={{ color: '#60a5fa', textDecoration: 'none' }}>
                            {c.sha.substring(0, 7)}
                          </a>
                        </div>
                      </div>
                    ))}
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