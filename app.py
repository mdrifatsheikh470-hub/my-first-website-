
from flask import Flask, request
from email.message import EmailMessage
import smtplib
import os
import re
import html

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    status_html = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            status_html = '<p class="error">সব ঘর পূরণ করুন।</p>'

        elif (
            len(name) > 100
            or len(email) > 254
            or len(message) > 5000
            or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
        ):
            status_html = '<p class="error">তথ্য সঠিকভাবে লিখুন।</p>'

        else:
            username = os.environ.get("MAIL_USERNAME", "")
            password = os.environ.get("MAIL_PASSWORD", "")
            recipient = "mdrifatsheikh470@gmail.com"

            if not username or not password:
                status_html = (
                    '<p class="error">ইমেইল সেটআপ এখনো সম্পূর্ণ হয়নি।</p>'
                )
            else:
                mail = EmailMessage()
                mail["Subject"] = "New Website Contact Message"
                mail["From"] = username
                mail["To"] = recipient
                mail["Reply-To"] = email
                mail.set_content(
                    "A visitor sent a message from your website.\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{message}"
                )

                try:
                    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
                        server.starttls()
                        server.login(username, password)
                        server.send_message(mail)

                    status_html = (
                        '<p class="success">'
                        'আপনার মেসেজ পাঠানো হয়েছে! ধন্যবাদ।'
                        '</p>'
                    )

                except Exception:
                    app.logger.exception("Contact email delivery failed")
                    status_html = (
                        '<p class="error">'
                        'মেসেজ পাঠানো যায়নি। পরে আবার চেষ্টা করুন।'
                        '</p>'
                    )

    page = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#050816">
<title>MD Rifat Sheikh | Official Website</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    padding: 30px 14px;
    color: white;
    text-align: center;
    font-family: Arial, sans-serif;
    background: linear-gradient(-45deg,#050816,#101827,#171044,#062b49);
    background-size: 400% 400%;
    animation: backgroundMove 14s ease infinite;
}

@keyframes backgroundMove {
    0%,100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.page {
    position: relative;
    width: 100%;
    max-width: 650px;
    margin: auto;
}

.animated-logo {
    width: 220px;
    max-width: 80%;
    height: auto;
    margin: 12px auto 20px;
    animation: floatLogo 3s ease-in-out infinite;
}

@keyframes floatLogo {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

h1 {
    color: #7dd3fc;
    font-size: clamp(27px,7vw,40px);
    text-shadow: 0 0 18px #0284c7;
}

.subtitle { color: #cbd5e1; }

.clock-card, .contact-card {
    max-width: 420px;
    margin: 28px auto;
    padding: 24px 18px;
    border: 1px solid rgba(56,189,248,.55);
    border-radius: 22px;
    background: rgba(10,20,45,.82);
    box-shadow: 0 0 25px rgba(56,189,248,.15);
}

.clock-title {
    color: #7dd3fc;
    font-size: 13px;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

#live-clock {
    font-size: clamp(34px,9vw,48px);
    font-weight: bold;
    font-variant-numeric: tabular-nums;
    text-shadow: 0 0 18px #38bdf8;
}

#live-date {
    color: #cbd5e1;
    margin-top: 12px;
    line-height: 1.7;
}

.time-zone {
    color: #7dd3fc;
    font-size: 11px;
    margin-top: 10px;
}

.welcome-button, .send-button {
    display: inline-block;
    padding: 13px 22px;
    border: 0;
    border-radius: 11px;
    background: linear-gradient(135deg,#38bdf8,#818cf8);
    color: #07111f;
    font-weight: bold;
    cursor: pointer;
}

.contact-card h2, .social-section h2 {
    color: #e0f2fe;
    margin-top: 0;
}

.contact-card p {
    color: #cbd5e1;
    line-height: 1.6;
}

.contact-form { text-align: left; }

.contact-form label {
    display: block;
    margin: 15px 0 7px;
    color: #e0f2fe;
    font-size: 14px;
}

.contact-form input, .contact-form textarea {
    display: block;
    width: 100%;
    padding: 13px;
    border: 1px solid #334155;
    border-radius: 10px;
    background: #0b1225;
    color: white;
    font: inherit;
}

.contact-form input:focus, .contact-form textarea:focus {
    outline: 2px solid #38bdf8;
    border-color: transparent;
}

.contact-form textarea {
    min-height: 130px;
    resize: vertical;
}

.send-button {
    width: 100%;
    margin-top: 20px;
    font-size: 15px;
}

.success {
    color: #86efac !important;
    background: rgba(22,163,74,.12);
    padding: 12px;
    border-radius: 10px;
}

.error {
    color: #fca5a5 !important;
    background: rgba(220,38,38,.12);
    padding: 12px;
    border-radius: 10px;
}

.social-section { margin: 38px auto 28px; }

.social-icons {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 18px 14px;
    margin: 20px auto;
}

.social-item { width: 72px; }

.social-icon {
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    border-radius: 17px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-decoration: none;
    transition: transform .2s;
}

.social-icon:hover { transform: translateY(-5px); }

.facebook { background: #1877F2; }
.instagram { background: linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5); }
.youtube { background: #ff0033; }
.tiktok { background: #111; }
.whatsapp { background: #128C7E; }

.social-label {
    color: #dbeafe;
    font-size: 12px;
    margin-top: 8px;
}

.footer {
    margin-top: 30px;
    padding: 20px 5px;
    border-top: 1px solid #334155;
    color: #94a3b8;
    font-size: 12px;
    line-height: 1.8;
}
</style>
</head>

<body>
<main class="page">

<img src="/static/logo.png" alt="Rifat Logo" class="animated-logo">

<h1>MD Rifat Sheikh</h1>
<p class="subtitle">Welcome to My Official Website ✨</p>

<div class="clock-card">
    <div class="clock-title">🕒 BANGLADESH TIME</div>
    <div id="live-clock">00:00:00</div>
    <div id="live-date">তারিখ লোড হচ্ছে...</div>
    <div class="time-zone">UTC +06:00 · DHAKA, BANGLADESH</div>
</div>

<button class="welcome-button"
onclick="alert('আমার ওয়েবসাইটে স্বাগতম! ❤️')">
✨ এখানে চাপ দাও
</button>

<section class="contact-card">
    <h2>📩 Contact Me</h2>
    <p>আমাকে কোনো মেসেজ পাঠাতে চাইলে নিচের ফর্মটি পূরণ করুন।</p>

    <!-- STATUS -->

    <form class="contact-form" method="POST" action="/">
        <label for="name">আপনার নাম</label>
        <input id="name" name="name" type="text"
               maxlength="100" required autocomplete="name">

        <label for="email">আপনার ইমেইল</label>
        <input id="email" name="email" type="email"
               maxlength="254" required autocomplete="email">

        <label for="message">আপনার মেসেজ</label>
        <textarea id="message" name="message"
                  maxlength="5000" required></textarea>

        <button class="send-button" type="submit">
            📩 মেসেজ পাঠান
        </button>
    </form>
</section>

<section class="social-section">
    <h2>Connect With Me 🌐</h2>

    <div class="social-icons">
        <div class="social-item">
            <a class="social-icon facebook"
               href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank" rel="noopener noreferrer">f</a>
            <div class="social-label">Facebook</div>
        </div>

        <div class="social-item">
            <a class="social-icon instagram"
               href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank" rel="noopener noreferrer">◎</a>
            <div class="social-label">Instagram</div>
        </div>

        <div class="social-item">
            <a class="social-icon youtube" href="#"
               aria-label="YouTube">▶</a>
            <div class="social-label">YouTube</div>
        </div>

        <div class="social-item">
            <a class="social-icon tiktok" href="#"
               aria-label="TikTok">♪</a>
            <div class="social-label">TikTok</div>
        </div>

        <div class="social-item">
            <a class="social-icon whatsapp" href="#"
               aria-label="WhatsApp">✆</a>
            <div class="social-label">WhatsApp</div>
        </div>
    </div>
</section>

<footer class="footer">
    Made with ❤️ by MD Rifat Sheikh<br>
    © <span id="year"></span> All Rights Reserved
</footer>

</main>

<script>
function updateClock() {
    const now = new Date();

    document.getElementById('live-clock').textContent =
        new Intl.DateTimeFormat('en-GB', {
            timeZone: 'Asia/Dhaka',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        }).format(now);

    document.getElementById('live-date').textContent =
        new Intl.DateTimeFormat('bn-BD', {
            timeZone: 'Asia/Dhaka',
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(now);

    document.getElementById('year').textContent =
        new Intl.DateTimeFormat('en', {
            timeZone: 'Asia/Dhaka',
            year: 'numeric'
        }).format(now);
}
updateClock();
setInterval(updateClock, 1000);
</script>
</body>
</html>
"""
    return page.replace("<!-- STATUS -->", status_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
