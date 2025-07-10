# SE_Toolkit – Ethical Social‑Engineering Framework  🛡️⚔️

> **DISCLAIMER:** This project is **strictly for authorized red‑team engagements, security research, and educational use**.  
> Misuse of this software is illegal. Always obtain **written permission** before testing any target.

---

## 🗂️ Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [API Keys & Integrations](#api-keys--integrations)
5. [Usage Guide](#usage-guide)
6. [Screenshots](#screenshots)
7. [Future Scope](#future_scope)
8. [License](#license)

---

## 📖 Overview<a name="overview"></a>

**SE_Toolkit** is a **Linux‑only**, modular, future‑scopic social‑engineering framework written in **Python + Shell**.  
It supports real‑time credential harvesting, OSINT reconnaissance, multi‑channel delivery (email/SMS/Telegram/WhatsApp), AI‑generated payloads, encrypted logging, and Tor hidden‑service deployment.

---

## ✨ Features<a name="features"></a>

| Category            | Highlights                                                                                   |
|---------------------|----------------------------------------------------------------------------------------------|
| Recon & OSINT       | WHOIS / DNS / subdomain brute, Google dorking, social‑link extraction                        |
| Phishing Server     | Flask, mobile‑first templates, real‑time credential capture, Tor .onion support              |
| Delivery Channels   | SMTP email, Twilio SMS, Telegram bot, WhatsApp stub, Discord webhook                         |
| AI Generation       | OpenAI‑powered email/SMS/HTML content, deepfake voice stub (Resemble AI)                     |
| Logging & Analytics | Append‑only logs, AES‑256 encryption, log rotation, blockchain integrity stub                |
| Evasion             | User‑agent randomization, link obfuscation stub, timing jitter                               |
| Security            | Input sanitization, API keys in YAML, no persistence, clear legal warnings                   |

---

## ⚡ Quick Start<a name="quick-start"></a>

> Tested on **Parrot OS** / **Kali** / **Ubuntu 20.04+**

```bash
# 1. Clone
git clone git@github.com:imcoder44/SE_Tools_W_AI.git
cd SE_Tools_W_AI

# 2. Make scripts executable
chmod +x setup.sh recon.sh utils/logger.sh

# 3. Run setup (installs deps, creates venv, configures Tor)
sudo ./setup.sh

# 4. Activate virtual‑env for every new shell
source venv/bin/activate
````

---

## 🔑 API Keys & Integrations<a name="api-keys--integrations"></a>

| Service                   | How to obtain key / token                                                                                                            | Where to paste                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| **Twilio**                | 1. Sign up → [https://twilio.com/](https://twilio.com/)  2. Create Project → **Messaging** → copy *Account SID* & *Auth Token*       | `config/settings.yaml` → `twilio:` section        |
| **Telegram**              | 1. DM **@BotFather** 2. `/newbot` 3. Copy **HTTP API Token** 4. Get your chat‑id (`/getUpdates`)                                     | `telegram.bot_token` & `telegram.default_chat_id` |
| **OpenAI**                | 1. Login → [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) 2. **Create new secret key** | `openai.api_key`                                  |
| **Resemble**              | 1. Sign up → [https://app.resemble.ai/](https://app.resemble.ai/) 2. Settings → **API Token**                                        | `resembleai.api_key`                              |
| **SMTP**                  | Use any SMTP provider (Gmail App‑Password, Mailgun, etc.) – ensure less‑secure‑apps/App‑Password is allowed                          | `mailer.*` fields                                 |
| **Blockchain (optional)** | Infura: [https://infura.io/](https://infura.io/) → **Ethereum Mainnet** → Project ID                                                 | `blockchain.infura_key`                           |

> After editing **`config/settings.yaml`**, keep your real file out of Git:
>
> ```bash
> echo "config/settings.yaml" >> .gitignore
> cp config/settings.yaml config/settings_sample.yaml   # commit sample instead
> ```

---

## 🚀 Usage Guide<a name="usage-guide"></a>

### 1. Start the phishing server

```bash
source venv/bin/activate
python3 app.py
```

Browse to:

* HTTPS (self‑signed): `https://127.0.0.1:5000/?target=example.com`
* Tor: `http://<your‑onion>.onion/`

### 2. Recon your target

```bash
./recon.sh example.com
# Results saved in recon_data/
```

### 3. Generate AI phishing content & send email

```python
# Inside Python REPL
from modules.ai_content import generate_phishing_content
from modules.mailer import send_email

profile = {'name':'Alice', 'keywords':['payroll','vpn']}
body = generate_phishing_content(profile, 'email')
send_email('alice@example.com', 'Payroll Update Required', body)
```

### 4. Send Telegram lure

```python
from modules.mailer import send_telegram
send_telegram("⚠️ Urgent VPN password reset required: https://your‑onion", chat_id=None)
```

### 5. View & decrypt logs

```bash
# rotate + encrypt handled automatically – decrypt example:
./utils/logger.sh decrypt_log logs/events_20250701.log.enc 32_CHAR_RANDOM_KEY
```

---

## 📸 Screenshots<a name="screenshots"></a>

<img width="785" height="581" alt="Screenshot 2025-07-10 223223" src="https://github.com/user-attachments/assets/fc157055-bb45-49e0-a12b-2289d91981f3" />

---


## 🗺️ Future Scope<a name="future scope"></a>

* [ ] **Deepfake voice calls** (Resemble AI / ElevenLabs)
* [ ] **Discord & WhatsApp fully implemented**
* [ ] **Blockchain proof‑of‑log** (Ethereum smart‑contract)
* [ ] **Automated  LLM prompt‑crafting** per‑victim
* [ ] **Dark‑web SMTP relays** integration
* [ ] **Docker compose** deployment option

---

## 📜 License<a name="license"></a>

```
© 2025 imcoder44 – Released under the MIT License  
Use at your own risk.  
This software must **not** be used for unlawful activity.
```

````

---

### ✅ What to do next

1. Save the above content as `README.md` in your repo root.  
2. Add screenshot PNGs at `docs/img/app_run.png` and `docs/img/login_mobile.png` (or adjust paths).  
3. Commit & push:

```bash
git add README.md docs/img/*.png
git commit -m "Add detailed README and screenshots"
git push
````

Need help capturing screenshots or adding a license file? Just let me know!
