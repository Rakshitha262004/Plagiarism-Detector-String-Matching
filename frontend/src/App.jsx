import React, { useState } from 'react';

export default function App() {
  const [sourceDoc, setSourceDoc] = useState('');
  const [studentDoc, setStudentDoc] = useState('');
  const [algorithm, setAlgorithm] = useState('kmp');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runAnalysis = async () => {
    if (!sourceDoc.trim() || !studentDoc.trim()) {
      setError('Please populate both document fields to run analysis.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_doc: sourceDoc, student_doc: studentDoc, algorithm }),
      });
      if (!response.ok) throw new Error('Backend computation failed.');
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Error communicating with backend analysis engine.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <header className="app-header">
        <div className="header-title">
          <h1>Plagiarism Verification Engine</h1>
          <p>String Matching Algorithms Portfolio Asset</p>
        </div>
        <div className="status-badge">System Engine Online</div>
      </header>

      <main className="main-container">
        {error && <div style={{color: 'red', marginBottom: '15px'}}>{error}</div>}

        {/* Left Inputs Card */}
        <div className="dashboard-card">
          <h2 className="card-title">Document Repositories</h2>
          
          <div className="input-group">
            <label className="input-label">Original Source Document Material</label>
            <textarea
              className="text-workspace"
              placeholder="Paste authorized master textbook text or verified original source document here..."
              value={sourceDoc}
              onChange={(e) => setSourceDoc(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label className="input-label">Submitted Copy To Inspect</label>
            <textarea
              className="text-workspace"
              placeholder="Paste the student's work or the copy file to check for plagiarism here..."
              value={studentDoc}
              onChange={(e) => setStudentDoc(e.target.value)}
            />
          </div>

          <div className="control-bar">
            <div>
              <label className="input-label" style={{fontSize: '11px', textTransform: 'uppercase'}}>DSA Strategy</label>
              <select
                className="select-dropdown"
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value)}
              >
                <option value="kmp">Knuth-Morris-Pratt (Automata-Based)</option>
                <option value="rabin_karp">Rabin-Karp (Rolling Hashing)</option>
              </select>
            </div>

            <button onClick={runAnalysis} disabled={loading} className="analyze-button">
              {loading ? 'Processing Search...' : 'Verify Content Integrity'}
            </button>
          </div>
        </div>

        {/* Right Outputs Card */}
        <div className="dashboard-card">
          <h2 className="card-title">Mathematical Analysis & Reports</h2>
          
          {!results && !loading && (
            <p style={{color: '#64748b', textAlign: 'center', marginTop: '40px'}}>Submit text content to run algorithmic comparisons.</p>
          )}
          
          {loading && (
            <p style={{color: '#2563eb', textAlign: 'center', marginTop: '40px'}}>Running exact substring matches...</p>
          )}

          {results && !loading && (
            <div>
              <div className="results-header-box">
                <div className={`metric-circle ${
                  results.plagiarism_percentage > 40 ? 'bg-danger' : results.plagiarism_percentage > 15 ? 'bg-warning' : 'bg-safe'
                }`}>
                  {results.plagiarism_percentage}%
                </div>
                <div>
                  <h3 style={{fontSize: '16px', fontWeight: 'bold'}}>Computed Plagiarism Flag</h3>
                  <p style={{color: '#64748b', fontSize: '13px', marginTop: '4px'}}>
                    Evaluated {results.total_sentences_checked} structural strings
                  </p>
                </div>
              </div>

              <h4 style={{fontSize: '12px', color: '#64748b', marginBottom: '8px', textTransform: 'uppercase'}}>Highlighted Alignment Outputs</h4>
              <div className="highlight-output-window">
                {results.matched_sentences.map((sentence, idx) => (
                  <span 
                    key={idx} 
                    className={sentence.match_found ? "copied-block" : "clean-block"}
                  >
                    {sentence.text}.
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="footer-metrics">
            <span>Time Complexity: O(N + M)</span>
            <span>Space Complexity: O(M)</span>
          </div>
        </div>
      </main>
    </div>
  );
}