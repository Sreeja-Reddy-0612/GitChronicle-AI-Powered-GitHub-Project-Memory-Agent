import { useState } from 'react';
import { analyzeCommit } from '../api/api';
import './CommitExplanation.css';

export default function CommitExplanation() {
  const data = JSON.parse(localStorage.getItem('repoData') || 'null');
  
  const [selectedSha, setSelectedSha] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [expandedFiles, setExpandedFiles] = useState(new Set());

  if (!data || !data.commits) return <h2 className="container">No Data (Go to Dashboard)</h2>;

  const handleAnalyze = async () => {
    if (!selectedSha) return;
    
    setLoading(true);
    setAnalysisResult(null);
    setError('');
    setExpandedFiles(new Set());
    
    try {
      const res = await analyzeCommit(data.repository, selectedSha);
      setAnalysisResult(res);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch commit explanation from the backend.');
    } finally {
      setLoading(false);
    }
  };

  const toggleFileExpansion = (filename) => {
    const newExpanded = new Set(expandedFiles);
    if (newExpanded.has(filename)) {
      newExpanded.delete(filename);
    } else {
      newExpanded.add(filename);
    }
    setExpandedFiles(newExpanded);
  };

  // Helper to render text with bold headings
  const renderFormattedText = (text) => {
    if (typeof text !== 'string') return text;
    return text.split('\n').map((line, i) => {
      if (line.startsWith('**') && line.endsWith('**')) {
        return <strong key={i} style={{ display: 'block', marginTop: '8px', color: '#60a5fa' }}>{line.replace(/\*\*/g, '')}</strong>;
      }
      return <p key={i} style={{ margin: '4px 0' }}>{line}</p>;
    });
  };

  return (
    <div className="container commit-explain-container" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div>
        <h1>🤖 Commit Explanation</h1>
        <p style={{ color: '#9ca3af' }}>AI-Powered Analysis for <a href={data.repository} target="_blank" rel="noreferrer" style={{ color: "#60a5fa" }}>{data.owner}/{data.repo}</a></p>
      </div>

      <div className="selector-section">
        <label style={{ fontWeight: 'bold' }}>Select a Commit:</label>
        <select 
          className="commit-select" 
          value={selectedSha} 
          onChange={(e) => setSelectedSha(e.target.value)}
        >
          <option value="">-- Choose a commit --</option>
          {data.commits.map(commit => (
            <option key={commit.sha} value={commit.sha}>
              {commit.sha.substring(0, 7)} - {commit.message.split('\n')[0]} ({commit.author})
            </option>
          ))}
        </select>
        
        <button 
          className="analyze-btn" 
          onClick={handleAnalyze} 
          disabled={!selectedSha || loading}
        >
          {loading ? 'Analyzing...' : 'Explain Commit'}
        </button>
        
        {error && <p style={{ color: '#f87171' }}>{error}</p>}
      </div>

      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div> Generating AI Insights...
        </div>
      )}

      {analysisResult && (
        <div className="explanation-section">
          <div className="llm-card">
            <h3>✨ AI Analysis</h3>
            <div className="llm-content">
              {renderFormattedText(analysisResult.analysis?.overall_summary || analysisResult.analysis)}
            </div>
          </div>
          
          <div className="files-card">
            <h3>📁 Files Changed ({analysisResult.files?.length || 0})</h3>
            <p className="hint-text">Click on a file to see its specific AI explanation</p>
            <div className="file-list">
              {analysisResult.files?.map((f, idx) => {
                const isExpanded = expandedFiles.has(f.filename);
                const fileInsight = analysisResult.analysis?.file_insights?.[f.filename];

                return (
                  <div key={idx} className={`file-item-container ${isExpanded ? 'expanded' : ''}`}>
                    <div 
                      className="file-item clickable" 
                      onClick={() => toggleFileExpansion(f.filename)}
                    >
                      <span className="file-name colored">{f.filename}</span>
                      <div className="file-stats">
                        <span className="stat-changes">{f.changes} changes</span>
                        <span className={`expand-icon ${isExpanded ? 'open' : ''}`}>▼</span>
                      </div>
                    </div>
                    {isExpanded && (
                      <div className="file-explanation">
                        {fileInsight ? (
                          renderFormattedText(fileInsight)
                        ) : (
                          <p className="no-insight">No specific insight generated for this file.</p>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
