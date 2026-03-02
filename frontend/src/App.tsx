import React, { useState, useEffect } from 'react';

interface Ticket {
  id: string;
  subject: string;
  description: string;
  status: 'processing' | 'awaiting_review' | 'resolved' | 'failed';
  resolution?: {
    response: string;
    confidence_score: number;
  };
}

const App: React.FC = () => {
  const [tickets, setTickets] = useState<any[]>([]);
  const [subject, setSubject] = useState('');
  const [description, setDescription] = useState('');
  const [activeTab, setActiveTab] = useState<'customer' | 'dashboard'>('dashboard');

  const fetchTickets = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/tickets');
      const data = await res.json();
      setTickets(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchTickets();
    const interval = setInterval(fetchTickets, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/tickets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subject, description, customer_id: 'CUST-DEMO' }),
    });
    setSubject('');
    setDescription('');
    setActiveTab('dashboard');
  };

  const handleReview = async (id: string, approved: boolean, feedback?: string) => {
    await fetch(`http://localhost:8000/api/tickets/${id}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approved, feedback }),
    });
    fetchTickets();
  };

  return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
        <h1>AI Support Nexus</h1>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            className={`premium-button ${activeTab === 'customer' ? '' : 'ghost'}`}
            style={{ background: activeTab === 'customer' ? undefined : 'transparent' }}
            onClick={() => setActiveTab('customer')}
          >
            Customer Portal
          </button>
          <button
            className={`premium-button ${activeTab === 'dashboard' ? '' : 'ghost'}`}
            style={{ background: activeTab === 'dashboard' ? undefined : 'transparent' }}
            onClick={() => setActiveTab('dashboard')}
          >
            Agent Dashboard
          </button>
        </div>
      </header>

      {activeTab === 'customer' ? (
        <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto' }}>
          <h2>Submit a Request</h2>
          <form onSubmit={handleSubmit}>
            <input
              className="input-field"
              placeholder="Subject (e.g. Login issues)"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            />
            <textarea
              className="input-field"
              placeholder="Describe your issue..."
              rows={5}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              style={{ resize: 'none' }}
            />
            <button className="premium-button" type="submit" style={{ width: '100%' }}>Send Message</button>
          </form>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '20px' }}>
          {tickets.map((t) => (
            <div key={t.ticket.id} className="glass-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h3 style={{ margin: 0, background: 'none', WebkitTextFillColor: 'white' }}>{t.ticket.subject}</h3>
                  <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>{t.ticket.description}</p>
                </div>
                <span className={`status-pill status-${t.status.replace('_', '-')}`}>
                  {t.status.replace('_', ' ')}
                </span>
              </div>

              {t.status === 'awaiting_review' && (
                <div style={{ marginTop: '24px', padding: '20px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--accent-blue)' }}>
                  <p style={{ fontWeight: 600, color: 'var(--accent-blue)', marginBottom: '12px' }}>AI SUGGESTED RESPONSE (Confidence: {t.resolution.confidence_score.toFixed(2)})</p>
                  <p style={{ fontStyle: 'italic', marginBottom: '20px' }}>"{t.resolution.response}"</p>
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button className="premium-button" onClick={() => handleReview(t.ticket.id, true)}>Approve & Send</button>
                    <button className="premium-button" style={{ background: 'var(--error)' }} onClick={() => handleReview(t.ticket.id, false, "Escalated to human supervisor.")}>Escalate</button>
                  </div>
                </div>
              )}

              {t.status === 'resolved' && t.resolution && (
                <div style={{ marginTop: '16px', color: 'var(--success)', fontSize: '0.9rem' }}>
                  ✓ Resolved: {t.resolution.response}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
