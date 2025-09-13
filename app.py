# app.py
from flask import Flask, jsonify, request, render_template_string
import random
import string

app = Flask(__name__)

# Function to make random password
def make_password(length=8):
    charValues = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(charValues) for _ in range(length))
    return password

# API route to generate password
@app.route("/generate-password")
def generate_password():
    length = request.args.get("len", default=8, type=int)
    pw = make_password(length)
    return jsonify({"password": pw})

# Frontend Route (serves HTML+CSS+JS)
@app.route("/")
def home():
    return render_template_string("""

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Smart Password Generator — Animated UI</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/sheryjs/dist/Shery.css">
  <style>
    :root{
      --bg:#0f1724;
      --card:#0b1220;
      --accent:#7c5cff;
      --muted:#9aa4b2;
      --glass: rgba(255,255,255,0.04);
      --glass-2: rgba(255,255,255,0.02);
    }
    *{box-sizing:border-box}
    html,body{height:100%;margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial;color:#e6eef8;background:linear-gradient(180deg,#071124 0%, #071b2b 100%);}
    .wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:36px;gap:28px;position:relative;overflow:hidden;}
    .bg-shape{position:absolute;width:420px;height:420px;border-radius:50%;background: linear-gradient(135deg, rgba(124,92,255,0.14), rgba(0,204,255,0.06));filter: blur(60px);left:-10%;top:-10%;transform:scale(1.1);pointer-events:none;}
    .bg-shape.two{right:-8%;left:auto;top:40%;transform:scale(0.8);}
    .card {width:100%;max-width:960px;background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border-radius:20px;padding:28px;display:flex;gap:20px;box-shadow: 0 10px 30px rgba(2,6,23,0.6);border: 1px solid rgba(255,255,255,0.03);backdrop-filter: blur(8px);align-items:center;justify-content:space-between;flex-wrap:wrap;}
    .left {flex:1 1 360px;min-width:260px;}
    .hero-title{font-size:1.9rem;line-height:1.02;color:white;font-weight:700;margin:0 0 10px 0;letter-spacing:-0.02em;}
    .hero-sub{color:var(--muted);margin:0 0 18px 0;}
    .controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;}
    .btn {cursor:pointer;background:linear-gradient(90deg,var(--accent), #1dd1a1);color:white;padding:12px 18px;border-radius:12px;font-weight:600;border:none;box-shadow: 0 6px 18px rgba(124,92,255,0.14);transition: transform .18s ease, box-shadow .18s ease;}
    .btn:active{ transform: translateY(2px); box-shadow: 0 4px 12px rgba(0,0,0,0.25); }
    .btn.secondary { background: transparent; border: 1px solid rgba(255,255,255,0.06); color:var(--muted); box-shadow:none; }
    .card-right{width:420px;max-width:100%;padding:20px;background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));border-radius:14px;border: 1px solid rgba(255,255,255,0.03);display:flex;flex-direction:column;gap:12px;align-items:center;justify-content:center;min-width:260px;}
    .pw-box{width:100%;background:var(--card);border-radius:12px;padding:18px;text-align:center;font-family: 'Courier New', Courier, monospace;font-size:1.35rem;letter-spacing:0.06em;color:#e9f0ff;box-shadow: inset 0 -6px 18px rgba(2,6,23,0.6);cursor:text;user-select: all;}
    .meta {display:flex;width:100%;gap:10px;justify-content:space-between;margin-top:8px;align-items:center;color:var(--muted);font-size:0.93rem;}
    .strength {height:8px;width:100%;background:rgba(255,255,255,0.04);border-radius:8px;overflow:hidden;}
    .strength > i {display:block;height:100%;width:10%;background:linear-gradient(90deg,#ff6b6b,#ffd166);transform-origin:left;transition:width .28s ease;}
    @media (max-width:760px){.card { padding:18px; gap:14px; }.hero-title{ font-size:1.4rem; }.card-right { order:-1; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bg-shape"></div>
    <div class="bg-shape two"></div>
    <div class="card" id="mainCard">
      <div class="left">
        <h1 class="hero-title">Instant Secure Passwords</h1>
        <p class="hero-sub">One-click generate strong, random passwords. Copy, customize length and preview strength.</p>
        <div class="controls">
          <button class="btn" id="generateBtn">Generate Password</button>
          <button class="btn secondary" id="regenBtn">Regenerate</button>
          <div style="display:flex;align-items:center;gap:8px;margin-left:auto;">
            <label style="color:var(--muted);font-size:.95rem">Length</label>
            <input id="lenRange" class="range" type="range" min="6" max="24" value="8" style="width:140px;">
            <div id="lenVal" style="min-width:30px;text-align:center;color:var(--muted)">8</div>
          </div>
        </div>
      </div>
      <div class="card-right" id="visualCard">
        <div class="pw-box" id="passwordBox" title="Click to copy">— click Generate —</div>
        <div class="meta">
          <div style="flex:1;">
            <div class="strength"><i id="strengthBar" style="width:10%"></i></div>
            <div style="font-size:.82rem;color:var(--muted);margin-top:6px;">Strength: <span id="strengthText">—</span></div>
          </div>
          <div class="copy"><div id="copyBtn" class="btn secondary" style="padding:8px 12px;">Copy</div></div>
        </div>
      </div>
    </div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://unpkg.com/sheryjs/dist/Shery.js"></script>
  <script>
    const generateBtn=document.getElementById('generateBtn');
    const regenBtn=document.getElementById('regenBtn');
    const passwordBox=document.getElementById('passwordBox');
    const copyBtn=document.getElementById('copyBtn');
    const lenRange=document.getElementById('lenRange');
    const lenVal=document.getElementById('lenVal');
    const strengthBar=document.getElementById('strengthBar');
    const strengthText=document.getElementById('strengthText');

    lenRange.addEventListener('input',()=>{lenVal.textContent=lenRange.value;});

    function estimateStrength(pw){
      let score=0;if(!pw)return{percent:10,label:'None'};
      if(pw.length>=8)score++;if(pw.length>=12)score++;
      if(/[a-z]/.test(pw)&&/[A-Z]/.test(pw))score++;
      if(/\d/.test(pw))score++;if(/[^A-Za-z0-9]/.test(pw))score++;
      const percent=Math.min(100,10+score*18);
      const labels=['Very Weak','Weak','Okay','Good','Strong','Excellent'];
      return{percent,label:labels[Math.min(labels.length-1,score)]};
    }

    async function fetchPassword(){
      const len=parseInt(lenRange.value,10)||8;
      const res=await fetch(`/generate-password?len=${len}`);
      const data=await res.json();
      showPassword(data.password);
    }

    function showPassword(pw){
      passwordBox.textContent=pw;
      const st=estimateStrength(pw);
      strengthBar.style.width=st.percent+'%';
      strengthText.textContent=st.label;
    }

    async function copyToClipboard(){
      try{await navigator.clipboard.writeText(passwordBox.textContent.trim());
        copyBtn.textContent='Copied ✅';setTimeout(()=>copyBtn.textContent='Copy',1200);}
      catch(e){alert('Copy failed');}
    }

    generateBtn.addEventListener('click',fetchPassword);
    regenBtn.addEventListener('click',fetchPassword);
    copyBtn.addEventListener('click',copyToClipboard);
    passwordBox.addEventListener('click',copyToClipboard);
  </script>
</body>
</html>

    """)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

