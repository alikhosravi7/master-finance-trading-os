"use client";
import { useMemo, useState } from "react";

type Candle = {o:number;h:number;l:number;c:number;v:number};
const markets = [
  {symbol:"BTC/USDT",name:"Bitcoin",price:"91,842.50",change:"+2.41%",up:true},
  {symbol:"ETH/USDT",name:"Ethereum",price:"3,124.80",change:"+1.82%",up:true},
  {symbol:"XAU/USD",name:"Gold",price:"4,086.20",change:"-0.38%",up:false},
  {symbol:"EUR/USD",name:"Euro / US Dollar",price:"1.15842",change:"+0.24%",up:true},
  {symbol:"GBP/USD",name:"Pound / US Dollar",price:"1.32180",change:"-0.12%",up:false},
  {symbol:"USOIL",name:"Crude Oil",price:"62.84",change:"+0.67%",up:true},
  {symbol:"SPY",name:"S&P 500 ETF",price:"672.18",change:"+0.31%",up:true},
];
const seed:Candle[] = [
  [58,64,53,61,42],[61,67,57,59,38],[59,63,50,52,55],[52,57,47,55,48],[55,65,53,63,61],[63,70,60,67,53],[67,72,61,64,45],[64,69,58,60,47],[60,66,56,64,51],[64,75,62,72,66],[72,78,68,70,58],[70,76,65,74,63],[74,81,70,78,70],[78,84,73,76,59],[76,82,69,72,56],[72,80,70,78,62],[78,88,75,85,76],[85,91,80,83,68],[83,89,77,80,57],[80,87,76,85,72],[85,94,82,91,83],[91,97,86,89,74],[89,95,84,93,80],[93,99,88,96,88]
].map(([o,h,l,c,v])=>({o,h,l,c,v}));
function Chart({symbol,tf}:{symbol:string;tf:string}) {
  const candles = useMemo(()=>seed.map((x,i)=>{const drift=((symbol.length*7+i*3)%9)-4; const base=x.o+drift; return {o:base,h:base+(x.h-x.o)+2,l:base-(x.o-x.l)-2,c:base+(x.c-x.o),v:x.v+((i*7)%19)};}),[symbol,tf]);
  const min=Math.min(...candles.map(x=>x.l))-4, max=Math.max(...candles.map(x=>x.h))+4;
  const y=(v:number)=>12+(max-v)/(max-min)*190;
  return <div className="chart-wrap"><div className="chart-legend"><span><i className="dot up"/> Bullish</span><span><i className="dot down"/> Bearish</span><span className="muted">{symbol} · {tf}</span></div>
    <svg className="chart" viewBox="0 0 620 270" role="img" aria-label={`Candlestick chart for ${symbol}`}>
      {[35,80,125,170,215].map((v)=><g key={v}><line x1="0" x2="570" y1={v} y2={v} className="gridline"/><text x="580" y={v+4} className="axis">{(max-(v-12)/190*(max-min)).toFixed(1)}</text></g>)}
      {candles.map((c,i)=>{const x=10+i*23.1, rising=c.c>=c.o, color=rising?"#31e6b3":"#ff647d"; const top=y(Math.max(c.o,c.c)), bottom=y(Math.min(c.o,c.c)); return <g key={i}><line x1={x+6} x2={x+6} y1={y(c.h)} y2={y(c.l)} stroke={color} strokeWidth="1.5"/><rect x={x} y={top} width="12" height={Math.max(3,bottom-top)} rx="1" fill={color}/><rect x={x} y={215+(70-c.v)*.72} width="12" height={c.v*.72} fill={color} opacity=".35"/></g>})}
      <line x1="0" x2="570" y1={y(candles[candles.length-1].c)} y2={y(candles[candles.length-1].c)} className="price-line"/>
      <text x="8" y="258" className="axis">09:00</text><text x="180" y="258" className="axis">12:00</text><text x="350" y="258" className="axis">15:00</text><text x="500" y="258" className="axis">18:00</text>
    </svg>
    <div className="chart-foot"><span>VOL · Sample</span><span>Indicators: FVG · OB · Liquidity</span></div>
  </div>
}
function InstallHint(){return <div className="install-hint"><span>⬇</span><div><b>Install on your phone</b><small>Browser menu → Add to Home Screen</small></div></div>}
export default function Home(){
  const [symbol,setSymbol]=useState("BTC/USDT"); const [tf,setTf]=useState("15m"); const [tab,setTab]=useState("Overview"); const [layer,setLayer]=useState("All");
  const active=markets.find(m=>m.symbol===symbol)!;
  return <main className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-mark">TI</div><div><b>TRADING<span> INTELLIGENCE</span></b><small>PRO MARKET TERMINAL</small></div></div><div className="top-actions"><span className="status-pill"><i/> DEMO MODE</span><button className="icon-btn" aria-label="Notifications">♧</button><div className="avatar">AK</div></div></header>
    <nav className="desktop-nav">{["Overview","Signals","Markets","Backtest","Traders"].map(x=><button key={x} className={tab===x?"nav-active":""} onClick={()=>setTab(x)}>{x}</button>)}</nav>
    <section className="welcome"><div><p className="eyebrow">THURSDAY · MARKET SESSION</p><h1>Market intelligence, <em>in focus.</em></h1><p className="sub">Multi-asset analytics and systematic signal research.</p></div><div className="market-state"><span className="pulse"/> DEMO ENVIRONMENT <small>Market feed not connected</small></div></section>
    <section className="stats-grid"><article className="stat-card"><small>TOTAL MARKET CAP</small><strong>$3.42T</strong><span className="positive">↗ 1.64% <i>24H</i></span></article><article className="stat-card"><small>BTC DOMINANCE</small><strong>58.2%</strong><span className="positive">↗ 0.31% <i>24H</i></span></article><article className="stat-card"><small>ACTIVE SIGNALS</small><strong>08</strong><span className="neutral">Sample records</span></article><article className="stat-card"><small>TRACKED MARKETS</small><strong>07</strong><span className="neutral">Across 5 asset classes</span></article></section>
    <div className="content-grid"><section className="panel chart-panel"><div className="panel-head"><div><p className="eyebrow">PRICE ACTION</p><h2>Advanced chart</h2></div><select value={symbol} onChange={e=>setSymbol(e.target.value)} aria-label="Select market">{markets.map(m=><option key={m.symbol}>{m.symbol}</option>)}</select></div>
      <div className="quote-row"><div><span className="quote-name">{active.name} <small>{symbol}</small></span><strong>{active.price}</strong><span className={active.up?"positive":"negative"}>{active.change} <small>24H</small></span></div><button className="outline-btn">☆ Watch</button></div>
      <div className="chart-tools"><div className="timeframes">{["5m","15m","1H","4H","1D","1W"].map(x=><button key={x} onClick={()=>setTf(x)} className={tf===x?"selected": ""}>{x}</button>)}</div><div className="tool-actions"><button title="Indicators">ƒx Indicators</button><button title="Chart settings">⚙</button><button title="Fullscreen">⛶</button></div></div>
      <Chart symbol={symbol} tf={tf}/><div className="layers"><span>ANALYSIS LAYERS</span>{["All","FVG","Order Blocks","Liquidity","MSS / CHoCH"].map(x=><button key={x} onClick={()=>setLayer(x)} className={layer===x?"layer-on":""}>{x}</button>)}</div>
      <div className="chart-disclaimer">Illustrative OHLC candles only. Not exchange data; overlays are conceptual and not yet drawn on live price history.</div>
    </section>
    <aside className="side-column"><section className="panel"><div className="panel-head"><div><p className="eyebrow">MARKET RADAR</p><h2>Watchlist</h2></div><button className="text-btn">View all ↗</button></div>{markets.slice(0,5).map(m=><button className={`watch-row ${symbol===m.symbol?"watch-active":""}`} key={m.symbol} onClick={()=>setSymbol(m.symbol)}><span><b>{m.symbol}</b><small>{m.name}</small></span><span className="watch-price"><b>{m.price}</b><small className={m.up?"positive":"negative"}>{m.change}</small></span></button>)}</section>
    <section className="panel signal-panel"><div className="panel-head"><div><p className="eyebrow">STRATEGY FEED</p><h2>Latest signals</h2></div><span className="live-tag">DEMO</span></div><div className="signal-item"><div className="signal-top"><b>BTC / USDT</b><span className="long-tag">LONG</span></div><div className="signal-meta"><span>ICT · 15m</span><span>Risk / Reward <b>1:3</b></span></div><div className="signal-levels"><span>ENTRY <b>91,250</b></span><span>STOP <b>90,400</b></span><span>TARGET <b>93,800</b></span></div><div className="signal-reason">Sweep → Displacement → MSS → FVG</div></div><button className="full-btn" onClick={()=>setTab("Signals")}>Open signal desk</button></section></aside></div>
    <section className="panel bottom-panel"><div className="panel-head"><div><p className="eyebrow">RESEARCH WORKSPACE</p><h2>From signal to evidence</h2></div></div><div className="workspace-grid"><div><span className="workspace-icon">⌁</span><b>Signal journal</b><small>Versioned entries, edits and outcome tracking.</small></div><div><span className="workspace-icon">◫</span><b>Backtest lab</b><small>Rule-based historical testing with auditable metrics.</small></div><div><span className="workspace-icon">◎</span><b>Trader analytics</b><small>Verified track records and risk-adjusted performance.</small></div></div></section>
    <InstallHint/>
    <nav className="mobile-nav">{[{n:"Overview",i:"⌂"},{n:"Signals",i:"⌁"},{n:"Markets",i:"▥"},{n:"Profile",i:"◉"}].map(x=><button key={x.n} onClick={()=>setTab(x.n)} className={tab===x.n?"mobile-active":""}><b>{x.i}</b><small>{x.n}</small></button>)}</nav>
    <footer>TRADING INTELLIGENCE <span>·</span> MOBILE-FIRST MVP <span>·</span> ALL DATA SHOWN IS DEMONSTRATION DATA</footer>
  </main>
}
