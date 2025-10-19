import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const WS_URL = (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + (window.location.hostname || 'localhost') + ':8000/ws';

export default function App(){
  const [token,setToken]=useState(localStorage.getItem('token')||'');
  const [email,setEmail]=useState('');
  const [pw,setPw]=useState('');
  const [status,setStatus]=useState(null);
  const [signals,setSignals]=useState([]);
  const wsRef = useRef(null);
  const signalsRef = useRef(signals);
  signalsRef.current = signals;

  // Play beep using WebAudio API
  function playBeep(){
    try{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = 'sine';
      o.frequency.value = 880;
      g.gain.value = 0.1;
      o.connect(g);
      g.connect(ctx.destination);
      o.start();
      setTimeout(()=>{ o.stop(); ctx.close(); }, 160);
    }catch(e){
      // fallback silent
      console.warn('beep failed', e);
    }
  }

  useEffect(()=>{ if(token) fetchStatus(); }, [token]);

  useEffect(()=>{
    // establish WebSocket connection only when user is authenticated and license valid
    if(!token) return;
    const clientId = 'client-' + Math.random().toString(36).slice(2,9);
    const ws = new WebSocket(WS_URL + '?client_id=' + clientId);
    wsRef.current = ws;
    ws.onopen = () => { console.log('ws open'); };
    ws.onmessage = (evt) => {
      try{
        const d = JSON.parse(evt.data);
        if(d.type === 'signal' && d.data){
          // prepend signal to list and play sound
          const sig = { id: d.data.id || ('s-'+Date.now()), platform: d.data.platform || d.data.platform || 'multi', symbol: d.data.symbol || d.data.pair || 'unknown', direction: d.data.direction || 'CALL', confidence: d.data.confidence || null, created_at: d.data.generated_at || new Date().toISOString() };
          setSignals(prev=> [sig, ...prev].slice(0,200));
          playBeep();
        }
      }catch(e){ console.error('ws message error', e); }
    };
    ws.onclose = ()=>{ console.log('ws closed'); };
    ws.onerror = (e)=>{ console.error('ws error', e); };
    return ()=>{ try{ ws.close(); }catch{} };
  }, [token]);

  async function register(){
    try{
      const r = await axios.post(API + '/auth/register', {email, password: pw});
      if(r.data.access_token){ localStorage.setItem('token', r.data.access_token); setToken(r.data.access_token); }
    }catch(e){ alert('register error: '+(e.response?.data?.detail||e.message)); }
  }
  async function login(){
    try{
      const r = await axios.post(API + '/auth/login', {email, password: pw});
      if(r.data.access_token){ localStorage.setItem('token', r.data.access_token); setToken(r.data.access_token); }
    }catch(e){ alert('login error: '+(e.response?.data?.detail||e.message)); }
  }
  async function fetchStatus(){
    try{ const r = await axios.get(API + '/license/status', {headers:{Authorization:'Bearer '+token}}); setStatus(r.data); }catch(e){ setStatus({valid:false}); }
  }
  async function loadSignals(){
    try{ const r = await axios.get(API + '/signals', {headers:{Authorization:'Bearer '+token}}); setSignals(r.data); }catch(e){ alert('cannot load signals: '+(e.response?.data?.detail||e.message)) }
  }

  return (<div style={{padding:20}}>
    <h2>SignalMaster PRO — Real-time</h2>
    {!token && <div style={{marginBottom:12}}>
      <input placeholder='email' value={email} onChange={e=>setEmail(e.target.value)} style={{marginRight:6}}/>
      <input placeholder='password' type='password' value={pw} onChange={e=>setPw(e.target.value)} style={{marginRight:6}}/>
      <button onClick={register}>Register</button>
      <button onClick={login} style={{marginLeft:6}}>Login</button>
    </div>}
    {token && <div>
      <div style={{display:'flex', gap:10, alignItems:'center'}}>
        <button onClick={()=>{localStorage.removeItem('token'); setToken(''); setStatus(null); setSignals([]);}}>Logout</button>
        <button onClick={loadSignals}>Load Signals</button>
        <div style={{marginLeft:12}}>License status: {status? status.valid ? 'Valid' : status.reason : 'loading...'}</div>
      </div>
      <div style={{marginTop:12}}>
        <h3>Últimos sinais (em tempo real)</h3>
        <table style={{width:'100%',borderCollapse:'collapse'}}>
          <thead><tr style={{textAlign:'left',borderBottom:'1px solid #ddd'}}><th>Hora</th><th>Plataforma</th><th>Par</th><th>Direção</th><th>Confiança</th></tr></thead>
          <tbody>
            {signals.map(s=> (<tr key={s.id} style={{borderBottom:'1px solid #f0f0f0'}}>
              <td style={{padding:'8px'}}>{new Date(s.created_at).toLocaleString()}</td>
              <td style={{padding:'8px'}}>{s.platform}</td>
              <td style={{padding:'8px'}}>{s.symbol}</td>
              <td style={{padding:'8px'}}>{s.direction}</td>
              <td style={{padding:'8px'}}>{s.confidence ?? '-'}</td>
            </tr>))}
          </tbody>
        </table>
      </div>
    </div>}
  </div>);
}
