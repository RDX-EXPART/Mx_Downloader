
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0c10;--bg2:#111520;--bg3:#1a1f2e;
  --border:#2a3040;--border2:#3a4560;
  --accent:#6c8fff;--accent2:#a78bfa;--accent3:#34d399;
  --txt:#e2e8f0;--txt2:#94a3b8;--txt3:#64748b;
  --red:#f87171;--amber:#fbbf24;--teal:#2dd4bf;
}
body{background:var(--bg);color:var(--txt);font-family:'Syne',sans-serif;padding:0;min-height:100vh}
.wrap{max-width:860px;margin:0 auto;padding:2rem 1.5rem 4rem}
.header{text-align:center;padding:3rem 0 2.5rem;position:relative;overflow:hidden}
.header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 40% at 50% 0%,rgba(52,211,153,.1),transparent)}
.badge{display:inline-flex;align-items:center;gap:6px;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.25);color:var(--accent3);font-size:11px;font-family:'JetBrains Mono',monospace;padding:4px 12px;border-radius:20px;letter-spacing:.08em;margin-bottom:1rem;text-transform:uppercase}
.badge-dot{width:6px;height:6px;border-radius:50%;background:var(--accent3);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
h1{font-size:2.4rem;font-weight:800;letter-spacing:-.02em;background:linear-gradient(135deg,#e2e8f0 0%,#34d399 50%,#6c8fff 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.5rem}
.subtitle{color:var(--txt2);font-size:1rem;font-weight:400}
.section{margin:2rem 0}
.section-title{display:flex;align-items:center;gap:10px;font-size:.7rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:var(--txt3);margin-bottom:1rem;font-family:'JetBrains Mono',monospace}
.section-title::after{content:'';flex:1;height:1px;background:var(--border)}
.tree{background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.tree-header{background:var(--bg3);padding:.6rem 1rem;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--border)}
.dot{width:10px;height:10px;border-radius:50%}
.tree-body{padding:1rem 1.25rem;font-family:'JetBrains Mono',monospace;font-size:.82rem;line-height:2}
.tree-body .dir{color:var(--accent);font-weight:600}
.tree-body .file{color:var(--txt2)}
.tree-body .comment{color:var(--txt3)}
.tree-indent{padding-left:1.5rem}
.flow{display:flex;flex-direction:column;gap:.5rem}
.flow-step{display:flex;align-items:flex-start;gap:12px;padding:.75rem 1rem;background:var(--bg2);border:1px solid var(--border);border-radius:10px;transition:border-color .2s}
.flow-step:hover{border-color:var(--border2)}
.step-num{flex-shrink:0;width:26px;height:26px;border-radius:8px;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.25);color:var(--accent3);font-size:.75rem;font-weight:600;font-family:'JetBrains Mono',monospace;display:flex;align-items:center;justify-content:center}
.step-text{font-size:.88rem;color:var(--txt2);line-height:1.5;padding-top:3px}
.step-text code{background:rgba(255,255,255,.07);color:var(--teal);font-family:'JetBrains Mono',monospace;font-size:.8rem;padding:1px 5px;border-radius:4px}
.code-block{background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin:.5rem 0}
.code-header{background:var(--bg3);padding:.5rem 1rem;font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--txt3);display:flex;align-items:center;gap:6px;border-bottom:1px solid var(--border)}
.lang-tag{background:rgba(52,211,153,.12);color:var(--accent3);padding:1px 8px;border-radius:4px;font-size:.7rem}
.code-body{padding:1rem 1.25rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;line-height:1.8;color:var(--txt2)}
.code-body .cmd{color:var(--accent3)}
.code-body .flag{color:var(--amber)}
.code-body .comment{color:var(--txt3)}
.code-body .str{color:var(--accent2)}
.code-body .var{color:var(--accent2)}
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.84rem}
thead tr{border-bottom:1px solid var(--border2)}
th{color:var(--txt3);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;padding:.7rem .9rem;text-align:left}
td{padding:.65rem .9rem;border-bottom:1px solid var(--border);color:var(--txt2)}
tbody tr:hover td{background:rgba(255,255,255,.02)}
.tag{display:inline-block;font-size:.7rem;font-family:'JetBrains Mono',monospace;padding:2px 8px;border-radius:5px;font-weight:600}
.tag-blue{background:rgba(108,143,255,.15);color:var(--accent)}
.tag-green{background:rgba(52,211,153,.12);color:var(--accent3)}
.tag-purple{background:rgba(167,139,250,.12);color:var(--accent2)}
.tag-amber{background:rgba(251,191,36,.12);color:var(--amber)}
.tag-core{background:rgba(52,211,153,.18);color:#059669;border:1px solid rgba(52,211,153,.3)}
.env-grid{display:grid;gap:.5rem}
.env-row{display:flex;align-items:center;gap:0;background:var(--bg2);border:1px solid var(--border);border-radius:8px;overflow:hidden;font-family:'JetBrains Mono',monospace;font-size:.8rem}
.env-key{padding:.55rem .9rem;background:var(--bg3);color:var(--accent2);border-right:1px solid var(--border);white-space:nowrap;flex-shrink:0;min-width:140px}
.env-val{padding:.55rem .9rem;color:var(--txt3);font-style:italic}
.ytdlp-banner{background:linear-gradient(135deg,rgba(52,211,153,.08),rgba(108,143,255,.08));border:1px solid rgba(52,211,153,.2);border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:12px}
.ytdlp-icon{width:36px;height:36px;border-radius:8px;background:rgba(52,211,153,.15);border:1px solid rgba(52,211,153,.25);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--accent3);font-weight:600;flex-shrink:0}
.ytdlp-text{font-size:.85rem;color:var(--txt2);line-height:1.5}
.ytdlp-text strong{color:var(--accent3);font-weight:600}
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--border2),transparent);margin:2rem 0}
.credits{margin-top:3rem;border-top:1px solid var(--border);padding-top:2rem}
.credits-inner{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:1.5rem;display:flex;flex-direction:column;gap:1rem}
.credits-title{font-size:.65rem;font-family:'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--txt3);margin-bottom:.25rem}
.credit-list{display:flex;flex-wrap:wrap;gap:.75rem}
.credit-chip{display:flex;align-items:center;gap:8px;background:var(--bg3);border:1px solid var(--border2);border-radius:30px;padding:.4rem .9rem .4rem .5rem}
.avatar{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;flex-shrink:0}
.avatar-dk{background:linear-gradient(135deg,#6c8fff,#a78bfa);color:#fff}
.avatar-hy{background:linear-gradient(135deg,#34d399,#059669);color:#fff}
.avatar-an{background:linear-gradient(135deg,#64748b,#334155);color:#cbd5e1}
.credit-name{font-size:.85rem;font-weight:600;color:var(--txt)}
.credit-role{font-size:.72rem;color:var(--txt3);font-family:'JetBrains Mono',monospace}
</style>

<div class="wrap">
  <div class="header">
    <div class="badge"><span class="badge-dot"></span>yt-dlp powered</div>
    <h1>DsrBotz MX Player</h1>
    <p class="subtitle">Download MX Player / MXPlay videos in any quality — powered entirely by yt-dlp</p>
  </div>

  <div class="section">
    <div class="section-title">Why yt-dlp</div>
    <div class="ytdlp-banner">
      <div class="ytdlp-icon">yt</div>
      <div class="ytdlp-text">
        <strong>yt-dlp</strong> handles the full pipeline — stream resolution, quality listing, and downloading of m3u8 / mpd manifests. No external binary needed. Install once via pip and it works everywhere.
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">File structure</div>
    <div class="tree">
      <div class="tree-header">
        <div class="dot" style="background:#ff5f57"></div>
        <div class="dot" style="background:#ffbd2e"></div>
        <div class="dot" style="background:#28ca41"></div>
        <span style="margin-left:8px;font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--txt3)">mxbot/</span>
      </div>
      <div class="tree-body">
        <div><span class="dir">mxbot/</span></div>
        <div class="tree-indent"><span class="file">├── bot.py</span> <span class="comment">— Entry point · app.run()</span></div>
        <div class="tree-indent"><span class="file">├── config.py</span> <span class="comment">— Env variable config</span></div>
        <div class="tree-indent"><span class="file">├── database.py</span> <span class="comment">— MongoDB (Motor async) helper</span></div>
        <div class="tree-indent"><span class="file">├── helpers.py</span> <span class="comment">— API + yt-dlp download logic</span></div>
        <div class="tree-indent"><span class="file">├── requirements.txt</span> <span class="comment">— Python dependencies</span></div>
        <div class="tree-indent"><span class="dir">└── plugins/</span></div>
        <div class="tree-indent" style="padding-left:3rem"><span class="file">├── commands.py</span> <span class="comment">— /start /help /stats</span></div>
        <div class="tree-indent" style="padding-left:3rem"><span class="file">└── downloader.py</span> <span class="comment">— Link handler · quality picker · download/upload</span></div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Setup</div>

    <p style="font-size:.8rem;font-family:'JetBrains Mono',monospace;color:var(--accent3);margin-bottom:.5rem;letter-spacing:.05em">01 — Install all dependencies</p>
    <div class="code-block">
      <div class="code-header"><span class="lang-tag">bash</span></div>
      <div class="code-body"><span class="cmd">pip install</span> -r requirements.txt</div>
    </div>
    <p style="font-size:.78rem;color:var(--txt3);font-family:'JetBrains Mono',monospace;margin:.6rem 0 1.2rem;padding:.5rem .75rem;background:rgba(52,211,153,.06);border-left:2px solid rgba(52,211,153,.3);border-radius:0 6px 6px 0">
      yt-dlp is installed via pip — no separate binary download required.
    </p>

    <p style="font-size:.8rem;font-family:'JetBrains Mono',monospace;color:var(--accent3);margin-bottom:.5rem;letter-spacing:.05em">02 — Verify yt-dlp installation</p>
    <div class="code-block">
      <div class="code-header"><span class="lang-tag">bash</span></div>
      <div class="code-body">
        <div>yt-dlp <span class="flag">--version</span></div>
        <div style="height:.4rem"></div>
        <div><span class="comment"># update yt-dlp to latest at any time</span></div>
        <div><span class="cmd">pip install</span> <span class="flag">-U</span> yt-dlp</div>
      </div>
    </div>

    <div style="height:1.2rem"></div>
    <p style="font-size:.8rem;font-family:'JetBrains Mono',monospace;color:var(--accent3);margin-bottom:.5rem;letter-spacing:.05em">03 — Set environment variables</p>
    <div class="env-grid">
      <div class="env-row"><span class="env-key">API_ID</span><span class="env-val">your_api_id</span></div>
      <div class="env-row"><span class="env-key">API_HASH</span><span class="env-val">your_api_hash</span></div>
      <div class="env-row"><span class="env-key">BOT_TOKEN</span><span class="env-val">your_bot_token</span></div>
      <div class="env-row"><span class="env-key">MONGO_URI</span><span class="env-val">mongodb://localhost:27017 or Atlas URI</span></div>
      <div class="env-row"><span class="env-key">DB_NAME</span><span class="env-val">dsrbotz_mx</span></div>
    </div>

    <div style="height:1.2rem"></div>
    <p style="font-size:.8rem;font-family:'JetBrains Mono',monospace;color:var(--accent3);margin-bottom:.5rem;letter-spacing:.05em">04 — Run the bot</p>
    <div class="code-block">
      <div class="code-header"><span class="lang-tag">bash</span></div>
      <div class="code-body"><span class="cmd">python</span> bot.py</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">yt-dlp usage in helpers.py</div>
    <div class="code-block">
      <div class="code-header"><span class="lang-tag">python</span> <span style="color:var(--txt3)">helpers.py · quality listing</span></div>
      <div class="code-body">
        <div><span class="var">import</span> yt_dlp</div>
        <div style="height:.5rem"></div>
        <div><span class="var">async def</span> <span style="color:var(--accent3)">get_formats</span>(url: str):</div>
        <div style="padding-left:1.5rem"><span class="var">ydl_opts</span> = {<span class="str">"quiet"</span>: True, <span class="str">"no_warnings"</span>: True}</div>
        <div style="padding-left:1.5rem"><span class="var">with</span> yt_dlp.YoutubeDL(ydl_opts) <span class="var">as</span> ydl:</div>
        <div style="padding-left:3rem"><span class="var">info</span> = ydl.extract_info(url, download=<span class="flag">False</span>)</div>
        <div style="padding-left:3rem"><span class="var">return</span> info.get(<span class="str">"formats"</span>, [])</div>
        <div style="height:.5rem"></div>
        <div><span class="var">async def</span> <span style="color:var(--accent3)">download_format</span>(url: str, fmt_id: str, out: str):</div>
        <div style="padding-left:1.5rem"><span class="var">ydl_opts</span> = {</div>
        <div style="padding-left:3rem"><span class="str">"format"</span>: fmt_id,</div>
        <div style="padding-left:3rem"><span class="str">"outtmpl"</span>: out,</div>
        <div style="padding-left:3rem"><span class="str">"quiet"</span>: True,</div>
        <div style="padding-left:1.5rem">}</div>
        <div style="padding-left:1.5rem"><span class="var">with</span> yt_dlp.YoutubeDL(ydl_opts) <span class="var">as</span> ydl:</div>
        <div style="padding-left:3rem">ydl.download([url])</div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Download flow</div>
    <div class="flow">
      <div class="flow-step"><div class="step-num">1</div><div class="step-text">User sends an MX Player / MXPlay link to the bot</div></div>
      <div class="flow-step"><div class="step-num">2</div><div class="step-text">Bot calls <code>ott.dkbotzpro.in/mxplayer?url=...</code> to resolve the stream URL</div></div>
      <div class="flow-step"><div class="step-num">3</div><div class="step-text"><code>yt-dlp.extract_info(url, download=False)</code> fetches all available format metadata</div></div>
      <div class="flow-step"><div class="step-num">4</div><div class="step-text">Bot presents inline quality buttons — <code>1080p [1920x1080]</code>, <code>720p</code>, <code>480p</code>, etc.</div></div>
      <div class="flow-step"><div class="step-num">5</div><div class="step-text"><code>yt-dlp</code> downloads the chosen format with live progress hook → uploaded with speed &amp; ETA</div></div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">MongoDB collections</div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Collection</th><th>Purpose</th></tr></thead>
        <tbody>
          <tr><td><span class="tag tag-blue">users</span></td><td>User records, join date, download count</td></tr>
          <tr><td><span class="tag tag-green">downloads</span></td><td>Per-download log with chosen quality &amp; timestamp</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Dependencies</div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Package</th><th>Role</th><th>Tag</th></tr></thead>
        <tbody>
          <tr><td style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent2)">hydrogram</td><td>Telegram MTProto client</td><td><span class="tag tag-purple">client</span></td></tr>
          <tr><td style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent2)">TgCrypto</td><td>Speed boost for MTProto encryption</td><td><span class="tag tag-blue">crypto</span></td></tr>
          <tr><td style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent2)">motor</td><td>Async MongoDB driver</td><td><span class="tag tag-green">database</span></td></tr>
          <tr><td style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent2)">aiohttp</td><td>Async HTTP for API resolution calls</td><td><span class="tag tag-blue">http</span></td></tr>
          <tr><td style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent3);font-weight:700">yt-dlp</td><td>Stream resolution, format listing &amp; downloading</td><td><span class="tag tag-core">core engine</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="divider"></div>

  <div class="credits">
    <div class="credits-inner">
      <div>
        <div class="credits-title">Credits &amp; attribution</div>
        <p style="font-size:.82rem;color:var(--txt3);margin-top:.3rem">Built with contributions from the following developers</p>
      </div>
      <div class="credit-list">
        <div class="credit-chip">
          <div class="avatar avatar-dk">DK</div>
          <div>
            <div class="credit-name">dk</div>
            <div class="credit-role">API · dkbotzpro.in</div>
          </div>
        </div>
        <div class="credit-chip">
          <div class="avatar avatar-hy">Hy</div>
          <div>
            <div class="credit-name">hydrogram</div>
            <div class="credit-role">MTProto client</div>
          </div>
        </div>
        <div class="credit-chip">
          <div class="avatar avatar-an">AN</div>
          <div>
            <div class="credit-name">Anonymous</div>
            <div class="credit-role">contributor</div>
          </div>
        </div>
      </div>
      <p style="font-size:.72rem;color:var(--txt3);font-family:'JetBrains Mono',monospace;border-top:1px solid var(--border);padding-top:.85rem;margin-top:.25rem">
        DsrBotz MX Player Downloader Bot · For educational purposes only · Respect content rights
      </p>
    </div>
  </div>
</div>
