
from flask import Flask, request
from email.message import EmailMessage
import smtplib
import os
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    status_html = ""
    language = "bn"

    if request.method == "POST":
        language = request.form.get("language", "bn")
        if language not in ("bn", "en"):
            language = "bn"

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            msg = "সব ঘর পূরণ করুন।" if language == "bn" else "Please fill in all fields."
            status_html = f'<p class="error" role="alert">{msg}</p>'

        elif (
            len(name) > 100
            or len(email) > 254
            or len(message) > 5000
            or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
        ):
            msg = "তথ্য সঠিকভাবে লিখুন।" if language == "bn" else "Please enter valid information."
            status_html = f'<p class="error" role="alert">{msg}</p>'

        else:
            username = os.environ.get("MAIL_USERNAME", "")
            password = os.environ.get("MAIL_PASSWORD", "")
            recipient = "mdrifatsheikh470@gmail.com"

            if not username or not password:
                msg = (
                    "ইমেইল সেটআপ এখনো সম্পূর্ণ হয়নি।"
                    if language == "bn"
                    else "Email setup is not complete yet."
                )
                status_html = f'<p class="error" role="alert">{msg}</p>'
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
                    with smtplib.SMTP(
                        "smtp.gmail.com", 587, timeout=20
                    ) as server:
                        server.starttls()
                        server.login(username, password)
                        server.send_message(mail)

                    msg = (
                        "আপনার মেসেজ পাঠানো হয়েছে! ধন্যবাদ।"
                        if language == "bn"
                        else "Your message has been sent! Thank you."
                    )
                    status_html = f'<p class="success" role="status">{msg}</p>'

                except Exception:
                    app.logger.exception("Contact email delivery failed")
                    msg = (
                        "মেসেজ পাঠানো যায়নি। পরে আবার চেষ্টা করুন।"
                        if language == "bn"
                        else "Message could not be sent. Please try again later."
                    )
                    status_html = f'<p class="error" role="alert">{msg}</p>'

    page = r"""
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#050816">
<title>MD Rifat Sheikh | Official Website</title>

<style>
* { box-sizing: border-box; }

html {
    scroll-behavior: smooth;
    scroll-padding-top: 20px;
}

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

#page-loader {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    background: #050816;
    transition: opacity .5s ease, visibility .5s ease;
}

#page-loader.loaded {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.loader-ring {
    width: 58px;
    height: 58px;
    border: 4px solid rgba(56,189,248,.18);
    border-top-color: #38bdf8;
    border-right-color: #818cf8;
    border-radius: 50%;
    animation: spinLoader .8s linear infinite;
}

@keyframes spinLoader {
    to { transform: rotate(360deg); }
}

.loader-title {
    color: #7dd3fc;
    font-weight: bold;
    letter-spacing: 2px;
}

.page {
    width: 100%;
    max-width: 650px;
    margin: auto;
    animation: pageAppear .7s ease both;
}

@keyframes pageAppear {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.animated-logo {
    display: block;
    width: 220px;
    max-width: 80%;
    height: auto;
    margin: 12px auto 20px;
    animation: floatLogo 3s ease-in-out infinite;
    filter: drop-shadow(0 0 12px rgba(56,189,248,.25));
    transition: filter .3s ease;
}

.animated-logo:hover {
    filter: drop-shadow(0 0 24px #38bdf8);
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

.subtitle {
    color: #cbd5e1;
    line-height: 1.7;
}

.clock-card, .contact-card {
    max-width: 420px;
    margin: 28px auto;
    padding: 24px 18px;
    border: 1px solid rgba(56,189,248,.55);
    border-radius: 22px;
    background: rgba(10,20,45,.82);
    box-shadow: 0 0 25px rgba(56,189,248,.15);
    transition: transform .3s ease, box-shadow .3s ease;
}

.clock-card:hover, .contact-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 35px rgba(56,189,248,.22);
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
    transition: transform .25s ease, box-shadow .25s ease;
}

.welcome-button:hover, .send-button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 24px rgba(56,189,248,.35);
}

.welcome-button:active, .send-button:active {
    transform: scale(.97);
}

#language-toggle {
    margin: 8px auto 16px;
    border: 1px solid rgba(125,211,252,.5);
    box-shadow: 0 0 15px rgba(56,189,248,.15);
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
    transition: border-color .25s ease, box-shadow .25s ease;
}

.contact-form input:focus, .contact-form textarea:focus {
    outline: none;
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56,189,248,.15);
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
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 17px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-decoration: none;
    transition: transform .25s ease, box-shadow .25s ease;
}

.social-icon:hover {
    transform: translateY(-7px) scale(1.08);
    box-shadow: 0 8px 22px rgba(56,189,248,.25);
}

.facebook { background: #1877F2; }
.instagram {
    background: linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5);
}
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

#back-to-top {
    position: fixed;
    right: 18px;
    bottom: 20px;
    z-index: 100;
    width: 48px;
    height: 48px;
    border: 1px solid rgba(125,211,252,.6);
    border-radius: 16px;
    background: rgba(8,25,50,.92);
    color: #7dd3fc;
    font-size: 25px;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transform: translateY(12px);
    transition: opacity .3s ease, visibility .3s ease,
                transform .3s ease;
}

#back-to-top.visible {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateY(0);
}

#back-to-top:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 25px rgba(56,189,248,.4);
}

@media (max-width: 480px) {
    body { padding: 22px 12px; }
    .clock-card, .contact-card {
        padding: 20px 14px;
        border-radius: 18px;
    }
    .social-icons { gap: 18px 10px; }
    .social-item { width: 65px; }
    .social-icon {
        width: 52px;
        height: 52px;
        border-radius: 15px;
    }
    #back-to-top {
        right: 12px;
        bottom: 14px;
        width: 44px;
        height: 44px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
    }
}
</style>
</head>

<body>

<div id="page-loader" role="status">
    <div class="loader-ring"></div>
    <div class="loader-title">MD RIFAT SHEIKH</div>
    <div id="loading-text" style="color:#94a3b8;font-size:13px">লোড হচ্ছে...</div>
</div>

<main class="page">

<img src="/static/logo.png" alt="Rifat Logo" class="animated-logo">

<h1>MD Rifat Sheikh</h1>
<p class="subtitle" id="subtitle">আমার অফিসিয়াল ওয়েবসাইটে স্বাগতম ✨</p>

<button id="language-toggle" class="welcome-button"
        type="button" onclick="toggleLanguage()">
    🌐 বাংলা | English
</button>

<div class="clock-card">
    <div class="clock-title" id="clock-title">🕒 বাংলাদেশের সময়</div>
    <div id="live-clock">00:00:00</div>
    <div id="live-date">তারিখ লোড হচ্ছে...</div>
    <div class="time-zone" id="timezone-label">UTC +06:00 · ঢাকা, বাংলাদেশ</div>
</div>

<button class="welcome-button" id="welcome-button" type="button"
        onclick="showWelcome()">
    ✨ এখানে চাপ দাও
</button>

<section class="contact-card">
    <h2 id="contact-title">📩 যোগাযোগ করুন</h2>
    <p id="contact-intro">আমাকে কোনো মেসেজ পাঠাতে চাইলে নিচের ফর্মটি পূরণ করুন।</p>

    <!-- STATUS -->

    <form class="contact-form" method="POST" action="/">
        <input type="hidden" name="language" id="form-language" value="bn">

        <label for="name" id="name-label">আপনার নাম</label>
        <input id="name" name="name" type="text"
               maxlength="100" required autocomplete="name">

        <label for="email" id="email-label">আপনার ইমেইল</label>
        <input id="email" name="email" type="email"
               maxlength="254" required autocomplete="email">

        <label for="message" id="message-label">আপনার মেসেজ</label>
        <textarea id="message" name="message"
                  maxlength="5000" required></textarea>

        <button class="send-button" id="send-button" type="submit">
            📩 মেসেজ পাঠান
        </button>
    </form>
</section>

<section class="social-section">
    <h2 id="social-title">আমার সঙ্গে যোগাযোগ করুন 🌐</h2>

    <div class="social-icons">
        <div class="social-item">
            <a class="social-icon facebook"
               href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank" rel="noopener noreferrer"
               aria-label="Facebook">f</a>
            <div class="social-label">Facebook</div>
        </div>

        <div class="social-item">
            <a class="social-icon instagram"
               href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank" rel="noopener noreferrer"
               aria-label="Instagram">◎</a>
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
    <span id="footer-text">তৈরি করেছেন ❤️ MD Rifat Sheikh</span><br>
    © <span id="year"></span> <span id="rights-text">সর্বস্বত্ব সংরক্ষিত</span>
</footer>

</main>

<button id="back-to-top" type="button"
        aria-label="পাতার উপরে যান" title="Back to Top">↑</button>

<script>
let currentLanguage = "bn";

const translations = {
    bn: {
        subtitle: "আমার অফিসিয়াল ওয়েবসাইটে স্বাগতম ✨",
        clockTitle: "🕒 বাংলাদেশের সময়",
        dateLoading: "তারিখ লোড হচ্ছে...",
        timezone: "UTC +06:00 · ঢাকা, বাংলাদেশ",
        welcome: "✨ এখানে চাপ দাও",
        welcomeMessage: "আমার ওয়েবসাইটে স্বাগতম! ❤️",
        contactTitle: "📩 যোগাযোগ করুন",
        contactIntro: "আমাকে কোনো মেসেজ পাঠাতে চাইলে নিচের ফর্মটি পূরণ করুন।",
        name: "আপনার নাম",
        email: "আপনার ইমেইল",
        message: "আপনার মেসেজ",
        send: "📩 মেসেজ পাঠান",
        socialTitle: "আমার সঙ্গে যোগাযোগ করুন 🌐",
        footer: "তৈরি করেছেন ❤️ MD Rifat Sheikh",
        rights: "সর্বস্বত্ব সংরক্ষিত",
        loading: "লোড হচ্ছে...",
        top: "পাতার উপরে যান",
        languageButton: "🌐 বাংলা | English"
    },
    en: {
        subtitle: "Welcome to My Official Website ✨",
        clockTitle: "🕒 BANGLADESH TIME",
        dateLoading: "Loading date...",
        timezone: "UTC +06:00 · DHAKA, BANGLADESH",
        welcome: "✨ Click Here",
        welcomeMessage: "Welcome to my website! ❤️",
        contactTitle: "📩 Contact Me",
        contactIntro: "Fill out the form below to send me a message.",
        name: "Your Name",
        email: "Your Email",
        message: "Your Message",
        send: "📩 Send Message",
        socialTitle: "Connect With Me 🌐",
        footer: "Made with ❤️ by MD Rifat Sheikh",
        rights: "All Rights Reserved",
        loading: "Loading...",
        top: "Back to top",
        languageButton: "🌐 English | বাংলা"
    }
};

function applyLanguage() {
    const t = translations[currentLanguage];

    document.documentElement.lang = currentLanguage;
    document.getElementById("subtitle").textContent = t.subtitle;
    document.getElementById("clock-title").textContent = t.clockTitle;
    document.getElementById("timezone-label").textContent = t.timezone;
    document.getElementById("welcome-button").textContent = t.welcome;
    document.getElementById("contact-title").textContent = t.contactTitle;
    document.getElementById("contact-intro").textContent = t.contactIntro;
    document.getElementById("name-label").textContent = t.name;
    document.getElementById("email-label").textContent = t.email;
    document.getElementById("message-label").textContent = t.message;
    document.getElementById("send-button").textContent = t.send;
    document.getElementById("social-title").textContent = t.socialTitle;
    document.getElementById("footer-text").textContent = t.footer;
    document.getElementById("rights-text").textContent = t.rights;
    document.getElementById("loading-text").textContent = t.loading;
    document.getElementById("language-toggle").textContent = t.languageButton;
    document.getElementById("back-to-top").title = t.top;
    document.getElementById("back-to-top").setAttribute("aria-label", t.top);
    document.getElementById("form-language").value = currentLanguage;

    updateClock();
}

function toggleLanguage() {
    currentLanguage = currentLanguage === "bn" ? "en" : "bn";
    applyLanguage();
}

function showWelcome() {
    alert(translations[currentLanguage].welcomeMessage);
}

function updateClock() {
    const now = new Date();
    const dateLocale = currentLanguage === "bn" ? "bn-BD" : "en-GB";

    document.getElementById("live-clock").textContent =
        new Intl.DateTimeFormat("en-GB", {
            timeZone: "Asia/Dhaka",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }).format(now);

    document.getElementById("live-date").textContent =
        new Intl.DateTimeFormat(dateLocale, {
            timeZone: "Asia/Dhaka",
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        }).format(now);

    document.getElementById("year").textContent =
        new Intl.DateTimeFormat("en", {
            timeZone: "Asia/Dhaka",
            year: "numeric"
        }).format(now);
}

function hideLoader() {
    const loader = document.getElementById("page-loader");
    if (loader) {
        loader.classList.add("loaded");
        loader.setAttribute("aria-hidden", "true");
    }
}

window.addEventListener("load", hideLoader);

if (document.readyState === "complete") {
    hideLoader();
}

const topButton = document.getElementById("back-to-top");

function toggleTopButton() {
    topButton.classList.toggle("visible", window.scrollY > 250);
}

window.addEventListener("scroll", toggleTopButton, { passive: true });

topButton.addEventListener("click", function () {
    window.scrollTo({
        top: 0,
        behavior: window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches ? "auto" : "smooth"
    });
});

applyLanguage();
updateClock();
setInterval(updateClock, 1000);
</script>

</body>
</html>
"""
    return page.replace("<!-- STATUS -->", status_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
                        
