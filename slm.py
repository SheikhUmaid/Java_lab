#!/usr/bin/env python3
"""
Ollama Web UI — A minimal local chat interface for Ollama.
Run: python ollama_ui.py
Then open: http://localhost:7860
"""

import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

OLLAMA_BASE = "http://localhost:11434"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Ollama Chat</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Syne:wght@400;700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:       #0d0f0e;
    --surface:  #141714;
    --border:   #252825;
    --accent:   #9bff6e;
    --accent2:  #4fffb0;
    --muted:    #4a4f49;
    --text:     #dde8da;
    --user-bg:  #1a2018;
    --ai-bg:    #111410;
    --danger:   #ff6b6b;
    --radius:   10px;
  }

  html, body { height: 100%; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }

  /* ── Header ── */
  header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    flex-shrink: 0;
  }

  .logo {
    width: 32px; height: 32px;
    background: var(--accent);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; line-height: 1;
  }

  header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text);
  }

  header h1 span { color: var(--accent); }

  .header-right {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  select {
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    outline: none;
    cursor: pointer;
    transition: border-color .15s;
  }
  select:hover, select:focus { border-color: var(--accent); }

  .status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--danger);
    transition: background .3s;
    flex-shrink: 0;
  }
  .status-dot.online { background: var(--accent); box-shadow: 0 0 6px var(--accent); }

  .status-label {
    font-size: 12px;
    color: var(--muted);
  }

  /* ── Main layout ── */
  main {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: hidden;
    max-width: 860px;
    width: 100%;
    margin: 0 auto;
    padding: 0 20px;
  }

  /* ── Messages ── */
  #messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px 0 12px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }

  .msg {
    display: flex;
    gap: 12px;
    animation: fadeUp .2s ease;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .msg-avatar {
    width: 28px; height: 28px;
    border-radius: 6px;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    margin-top: 2px;
  }

  .msg.user .msg-avatar  { background: #2a3a28; color: var(--accent); }
  .msg.ai   .msg-avatar  { background: #1e2a1c; color: var(--accent2); }

  .msg-body {
    flex: 1;
    min-width: 0;
  }

  .msg-role {
    font-size: 11px;
    font-weight: 500;
    color: var(--muted);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: .06em;
  }

  .msg.user .msg-role { color: var(--accent); }
  .msg.ai   .msg-role { color: var(--accent2); }

  .msg-text {
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--text);
  }

  /* inline code */
  .msg-text code {
    background: #1c221b;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 5px;
    font-family: 'DM Mono', monospace;
    font-size: 12.5px;
    color: var(--accent2);
  }

  /* code blocks */
  .msg-text pre {
    background: #0a0c0a;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    overflow-x: auto;
    margin: 8px 0;
  }

  .msg-text pre code {
    background: transparent;
    border: none;
    padding: 0;
    font-size: 13px;
    color: var(--accent2);
  }

  /* typing cursor */
  .cursor {
    display: inline-block;
    width: 7px; height: 15px;
    background: var(--accent);
    border-radius: 2px;
    margin-left: 2px;
    vertical-align: middle;
    animation: blink .7s step-end infinite;
  }
  @keyframes blink { 50% { opacity: 0; } }

  .empty-state {
    text-align: center;
    margin: auto;
    opacity: .45;
    user-select: none;
  }
  .empty-state .icon { font-size: 48px; margin-bottom: 12px; }
  .empty-state p { font-size: 13px; line-height: 1.8; color: var(--muted); }

  /* ── Input bar ── */
  .input-bar {
    padding: 14px 0 18px;
    flex-shrink: 0;
  }

  .input-wrap {
    display: flex;
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    transition: border-color .15s;
  }
  .input-wrap:focus-within { border-color: var(--accent); }

  textarea {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    resize: none;
    line-height: 1.55;
    max-height: 160px;
    min-height: 24px;
    overflow-y: auto;
    scrollbar-width: none;
  }

  .btn {
    background: var(--accent);
    border: none;
    border-radius: 8px;
    color: #0d0f0e;
    cursor: pointer;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 13px;
    padding: 0 16px;
    align-self: flex-end;
    height: 36px;
    transition: background .15s, transform .1s;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .btn:hover  { background: var(--accent2); }
  .btn:active { transform: scale(.97); }
  .btn:disabled { opacity: .4; cursor: not-allowed; }

  .btn-clear {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-weight: 400;
  }
  .btn-clear:hover { border-color: var(--danger); color: var(--danger); background: transparent; }

  .hint { font-size: 11px; color: var(--muted); margin-top: 6px; text-align: right; }

  /* scrollbar */
  #messages::-webkit-scrollbar { width: 4px; }
  #messages::-webkit-scrollbar-track { background: transparent; }
  #messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

  /* ── HTML Preview widget ── */
  .html-preview {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin: 8px 0;
  }

  .preview-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 12px;
    background: #0a0c0a;
    border-bottom: 1px solid var(--border);
  }

  .preview-label {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: .05em;
  }

  .preview-tabs { display: flex; gap: 4px; }

  .ptab {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 5px;
    color: var(--muted);
    cursor: pointer;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 3px 10px;
    transition: all .15s;
  }
  .ptab:hover  { border-color: var(--accent); color: var(--accent); }
  .ptab.active { background: var(--accent); border-color: var(--accent); color: #0d0f0e; }

  .preview-pane iframe {
    display: block;
    width: 100%;
    height: 360px;
    background: #fff;
    border: none;
  }

  .preview-pane pre {
    margin: 0;
    max-height: 360px;
    overflow: auto;
    background: #0a0c0a;
    padding: 14px 16px;
  }

  .preview-pane pre code {
    font-size: 12.5px;
    color: var(--accent2);
    white-space: pre;
  }

  .hidden { display: none !important; }
</style>
</head>
<body>

<header>
  <div class="logo">🦙</div>
  <h1>Ollama <span>Chat</span></h1>
  <div class="header-right">
    <div class="status-dot" id="statusDot"></div>
    <span class="status-label" id="statusLabel">connecting…</span>
    <select id="modelSelect"><option value="">— model —</option></select>
    <button class="btn btn-clear" onclick="clearChat()">Clear</button>
  </div>
</header>

<main>
  <div id="messages">
    <div class="empty-state" id="emptyState">
      <div class="icon">🦙</div>
      <p>Pick a model above, type a message,<br>and press Enter or Send.</p>
    </div>
  </div>

  <div class="input-bar">
    <div class="input-wrap">
      <textarea id="input" rows="1" placeholder="Message your local LLM…" autofocus></textarea>
      <button class="btn" id="sendBtn" onclick="sendMessage()">Send</button>
    </div>
    <div class="hint">Enter to send &nbsp;·&nbsp; Shift+Enter for newline</div>
  </div>
</main>

<script>
const messagesEl  = document.getElementById('messages');
const inputEl     = document.getElementById('input');
const sendBtn     = document.getElementById('sendBtn');
const modelSelect = document.getElementById('modelSelect');
const statusDot   = document.getElementById('statusDot');
const statusLabel = document.getElementById('statusLabel');

let history = [];   // [{role, content}]
let streaming = false;

/* ── Auto-resize textarea ── */
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = inputEl.scrollHeight + 'px';
});

inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

/* ── Load models ── */
async function loadModels() {
  try {
    const r = await fetch('/api/models');
    const d = await r.json();
    if (d.error) throw new Error(d.error);
    modelSelect.innerHTML = '';
    d.models.forEach(m => {
      const o = document.createElement('option');
      o.value = o.textContent = m;
      modelSelect.appendChild(o);
    });
    setOnline(true);
  } catch {
    setOnline(false);
    modelSelect.innerHTML = '<option value="">— unavailable —</option>';
  }
}

function setOnline(ok) {
  statusDot.className = 'status-dot' + (ok ? ' online' : '');
  statusLabel.textContent = ok ? 'online' : 'ollama offline';
}

/* ── Render helpers ── */
function escapeHtml(t) {
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// Detect a fenced HTML code block (```html ... ``` or standalone <!DOCTYPE/< html)
const HTML_FENCE_RE = /```(?:html|HTML)\s*([\s\S]*?)```/;

function extractHtmlBlock(text) {
  const m = text.match(HTML_FENCE_RE);
  if (m) return { before: text.slice(0, m.index).trim(), html: m[1].trim(), after: text.slice(m.index + m[0].length).trim() };
  return null;
}

function renderMarkdown(text) {
  // Code blocks — skip html (handled separately)
  text = text.replace(/```([\w]*)\n?([\s\S]*?)```/g, (full, lang, code) => {
    if (lang.toLowerCase() === 'html') return full; // left for extractHtmlBlock
    return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
  });
  text = text.replace(/`([^`]+)`/g, (_, c) => `<code>${escapeHtml(c)}</code>`);
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  return text;
}

let previewCount = 0;

function buildHtmlPreview(htmlSrc) {
  const id = ++previewCount;
  const div = document.createElement('div');
  div.className = 'html-preview';
  div.innerHTML = `
    <div class="preview-toolbar">
      <span class="preview-label">⟨/⟩ HTML Preview</span>
      <div class="preview-tabs">
        <button class="ptab active" data-id="${id}" data-tab="preview" onclick="switchTab(this)">Preview</button>
        <button class="ptab" data-id="${id}" data-tab="code" onclick="switchTab(this)">Code</button>
      </div>
    </div>
    <div class="preview-pane" id="pane-preview-${id}">
      <iframe id="iframe-${id}" sandbox="allow-scripts" frameborder="0"></iframe>
    </div>
    <div class="preview-pane hidden" id="pane-code-${id}">
      <pre><code id="code-${id}"></code></pre>
    </div>`;
  // Set iframe content and code block safely
  setTimeout(() => {
    const iframe = div.querySelector(`#iframe-${id}`);
    iframe.srcdoc = htmlSrc;
    div.querySelector(`#code-${id}`).textContent = htmlSrc;
  }, 0);
  return div;
}

function switchTab(btn) {
  const id  = btn.dataset.id;
  const tab = btn.dataset.tab;
  btn.closest('.html-preview').querySelectorAll('.ptab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  ['preview','code'].forEach(t => {
    const p = document.getElementById(`pane-${t}-${id}`);
    if (p) p.classList.toggle('hidden', t !== tab);
  });
}

function renderFinalMessage(aiBox, accumulated) {
  const parsed = extractHtmlBlock(accumulated);
  if (parsed) {
    aiBox.innerHTML = '';
    if (parsed.before) {
      const pre = document.createElement('div');
      pre.innerHTML = renderMarkdown(parsed.before);
      aiBox.appendChild(pre);
    }
    aiBox.appendChild(buildHtmlPreview(parsed.html));
    if (parsed.after) {
      const post = document.createElement('div');
      post.innerHTML = renderMarkdown(parsed.after);
      aiBox.appendChild(post);
    }
  } else {
    aiBox.innerHTML = renderMarkdown(accumulated);
  }
}

function addMessage(role, content) {
  document.getElementById('emptyState')?.remove();
  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;
  wrap.innerHTML = `
    <div class="msg-avatar">${role === 'user' ? 'U' : 'AI'}</div>
    <div class="msg-body">
      <div class="msg-role">${role === 'user' ? 'You' : modelSelect.value || 'Assistant'}</div>
      <div class="msg-text"></div>
    </div>`;
  messagesEl.appendChild(wrap);
  const box = wrap.querySelector('.msg-text');
  if (content) renderFinalMessage(box, content);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return box;
}

/* ── Send ── */
async function sendMessage() {
  if (streaming) return;
  const text = inputEl.value.trim();
  if (!text) return;
  const model = modelSelect.value;
  if (!model) { alert('Please select a model first.'); return; }

  inputEl.value = '';
  inputEl.style.height = 'auto';
  streaming = true;
  sendBtn.disabled = true;

  addMessage('user', text);
  history.push({ role: 'user', content: text });

  const aiBox = addMessage('ai', '');
  const cursor = document.createElement('span');
  cursor.className = 'cursor';
  aiBox.appendChild(cursor);

  let accumulated = '';
  // Batch rendering: accumulate tokens, flush via rAF
  let pending = '';
  let rafId = null;

  function flush() {
    rafId = null;
    if (!pending) return;
    accumulated += pending;
    pending = '';
    // During streaming show plain pre-wrap text for speed — no heavy regex on every frame
    aiBox.textContent = accumulated;
    aiBox.appendChild(cursor);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, messages: history })
    });

    if (!resp.ok) throw new Error(await resp.text());

    const reader = resp.body.getReader();
    const dec = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let nl;
      while ((nl = buf.indexOf('\n')) !== -1) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue;
        try {
          const obj = JSON.parse(line);
          if (obj.token) {
            pending += obj.token;
            if (!rafId) rafId = requestAnimationFrame(flush);
          }
          if (obj.done) break;
        } catch {}
      }
    }
    if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
    accumulated += pending;

  } catch (err) {
    accumulated = `⚠ Error: ${err.message}`;
    aiBox.innerHTML = `<span style="color:var(--danger)">${escapeHtml(accumulated)}</span>`;
    cursor.remove();
    history.push({ role: 'assistant', content: accumulated });
    streaming = false;
    sendBtn.disabled = false;
    inputEl.focus();
    return;
  }

  cursor.remove();
  // Full markdown + HTML preview render on completion
  renderFinalMessage(aiBox, accumulated);
  history.push({ role: 'assistant', content: accumulated });
  streaming = false;
  sendBtn.disabled = false;
  inputEl.focus();
}

function clearChat() {
  history = [];
  messagesEl.innerHTML = `
    <div class="empty-state" id="emptyState">
      <div class="icon">🦙</div>
      <p>Pick a model above, type a message,<br>and press Enter or Send.</p>
    </div>`;
}

loadModels();
setInterval(loadModels, 15000);
</script>
</body>
</html>
"""


# ── HTTP handler ───────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):  # silence default logs
        pass

    # ── routing ──
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self._send(200, 'text/html; charset=utf-8', HTML.encode())
        elif self.path == '/api/models':
            self._models()
        else:
            self._send(404, 'text/plain', b'Not found')

    def do_POST(self):
        if self.path == '/api/chat':
            self._chat()
        else:
            self._send(404, 'text/plain', b'Not found')

    # ── helpers ──
    def _send(self, code, ct, body):
        self.send_response(code)
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self._send(code, 'application/json', body)

    def _read_body(self):
        n = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(n)

    # ── /api/models ──
    def _models(self):
        try:
            with urllib.request.urlopen(f'{OLLAMA_BASE}/api/tags', timeout=4) as r:
                data = json.loads(r.read())
            names = sorted(m['name'] for m in data.get('models', []))
            self._json(200, {'models': names})
        except Exception as e:
            self._json(503, {'error': str(e)})

    # ── /api/chat  (streaming) ──
    def _chat(self):
        try:
            payload = json.loads(self._read_body())
            model    = payload['model']
            messages = payload['messages']
        except Exception as e:
            self._json(400, {'error': str(e)})
            return

        body = json.dumps({
            'model':    model,
            'messages': messages,
            'stream':   True,
        }).encode()

        try:
            req = urllib.request.Request(
                f'{OLLAMA_BASE}/api/chat',
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-ndjson')
            self.send_header('Transfer-Encoding', 'chunked')
            self.end_headers()

            with urllib.request.urlopen(req, timeout=120) as resp:
                for raw_line in resp:
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    token = ''
                    done  = obj.get('done', False)

                    # /api/chat response shape
                    msg = obj.get('message', {})
                    token = msg.get('content', '')

                    out = json.dumps({'token': token, 'done': done}) + '\n'
                    self.wfile.write(out.encode())
                    self.wfile.flush()

                    if done:
                        break

        except BrokenPipeError:
            pass
        except Exception as e:
            err = json.dumps({'token': f'\n[Error: {e}]', 'done': True}) + '\n'
            try:
                self.wfile.write(err.encode())
            except Exception:
                pass
def main():
    port = 3333
    
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f"""
  🦙  Ollama Web UI
  ─────────────────────────────────────
  Local:   http://localhost:{port}
  Ollama:  {OLLAMA_BASE}

  Make sure Ollama is running:  ollama serve
  Pull a model first if needed: ollama pull llama3

  Press Ctrl+C to stop.
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Stopped.')


if __name__ == '__main__':
    main()