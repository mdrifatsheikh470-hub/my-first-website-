
import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, render_template_string

app = Flask(__name__)

EMAIL_TO = "mdrifatsheikh470@gmail.com"


@app.route("/", methods=["GET", "POST"])
def home():
    status_html = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            status_html = """
            <div class="notice error">
                অনুগ্রহ করে সব ঘর পূরণ করুন।
            </div>
            """
        else:
            mail_username = os.environ.get("MAIL_USERNAME")
            mail_password = os.environ.get("MAIL_PASSWORD")

            if not mail_username or not mail_password:
                status_html = """
                <div class="notice error">
                    ইমেইল সার্ভার এখন সেটআপ করা নেই।
                    অনুগ্রহ করে পরে আবার চেষ্টা করুন।
                </div>
                """
            else:
                try:
                    mail = EmailMessage()
                    mail["Subject"] = f"Website Message from {name}"
                    mail["From"] = mail_username
                    mail["To"] = EMAIL_TO
                    mail["Reply-To"] = email
                    mail.set_content(
                        f"নতুন ওয়েবসাইট মেসেজ\n\n"
                        f"নাম: {name}\n"
                        f"ইমেইল: {email}\n\n"
                        f"মেসেজ:\n{message}"
                    )

                    with smtplib.SMTP(
                        "smtp.gmail.com", 587, timeout=20
                    ) as server:
                        server.starttls()
                        server.login(mail_username, mail_password)
                        server.send_message(mail)

                    status_html = """
                    <div class="notice success">
                        আপনার মেসেজ পাঠানো হয়েছে। ধন্যবাদ! 💙
                    </div>
                    """
                except Exception:
                    app.logger.exception("Contact form email failed")
                    status_html = """
                    <div class="notice error">
                        মেসেজ পাঠানো যায়নি। অনুগ্রহ করে পরে চেষ্টা করুন।
                    </div>
                    """

    page = r"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#080d20">
<meta name="description" content="MD Rifat Sheikh-এর অফিসিয়াল ওয়েবসাইট।">
<title>MD Rifat Sheikh | Official Website</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --cyan: #55eaff;
    --purple: #a78bfa;
    --text: #f4f7ff;
    --muted: #c2cce5;
    --panel: rgba(255,255,255,0.075);
}

html {
    scroll-behavior: smooth;
}

body {
    min-height: 100vh;
    overflow-x: hidden;
    color: var(--text);
    background:
        radial-gradient(ellipse at top left, #192b59 0%, transparent 45%),
        radial-gradient(ellipse at bottom right, #30174c 0%, transparent 45%),
        #080d20;
    font-family: Arial, "Noto Sans Bengali", sans-serif;
    text-align: center;
}

#space-canvas {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}

.mouse-glow {
    position: fixed;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: rgba(85,234,255,0.08);
    filter: blur(45px);
    pointer-events: none;
    z-index: 0;
    transform: translate(-50%, -50%);
}

.content {
    position: relative;
    z-index: 1;
    width: min(920px, 92%);
    margin: 0 auto;
    padding: 35px 0 28px;
}

.topbar {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.language-btn {
    padding: 10px 16px;
    color: white;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 25px;
    cursor: pointer;
    transition: 0.25s;
}

.language-btn:hover {
    background: rgba(85,234,255,0.2);
    transform: translateY(-2px);
}

.hero {
    padding: 30px 20px;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 28px;
    background: rgba(255,255,255,0.045);
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 70px rgba(0,0,0,0.25);
    animation: fadeUp 0.9s ease both;
}

.logo {
    width: 145px;
    height: 145px;
    max-width: 45vw;
    max-height: 45vw;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid var(--cyan);
    box-shadow: 0 0 25px rgba(85,234,255,0.35);
    margin-bottom: 20px;
    animation: logoGlow 3s ease-in-out infinite alternate;
}

h1 {
    font-size: clamp(28px, 6vw, 46px);
    font-weight: 800;
    overflow-wrap: anywhere;
    background: linear-gradient(90deg, #ffffff, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.typing-line {
    min-height: 38px;
    margin: 10px auto;
    color: var(--cyan);
    font-size: clamp(17px, 4.5vw, 23px);
    font-weight: 700;
    text-shadow: 0 0 14px rgba(56,189,248,0.65);
    overflow-wrap: anywhere;
}

.typing-cursor {
    display: inline-block;
    margin-left: 3px;
    color: white;
    animation: typingBlink 0.7s steps(1) infinite;
}

.subtitle {
    margin-top: 12px;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.8;
}

.clock-box {
    margin: 22px auto 0;
    padding: 15px;
    max-width: 360px;
    border-radius: 18px;
    background: rgba(85,234,255,0.07);
    border: 1px solid rgba(85,234,255,0.17);
}

.clock-label {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 6px;
}

#clock {
    color: var(--cyan);
    font-size: clamp(23px, 5vw, 32px);
    font-weight: bold;
    letter-spacing: 1px;
}

#date {
    margin-top: 6px;
    color: var(--muted);
    font-size: 14px;
}

.section {
    margin-top: 28px;
    padding: 25px 20px;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    background: var(--panel);
    backdrop-filter: blur(10px);
    animation: fadeUp 1s ease both;
}

.section h2 {
    font-size: 24px;
    margin-bottom: 18px;
    color: var(--cyan);
}

.social-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 13px;
}

.social-card {
    min-width: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    min-height: 65px;
    padding: 14px 8px;
    text-decoration: none;
    color: white;
    font-weight: bold;
    border-radius: 16px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    transition: transform 0.25s, background 0.25s, border-color 0.25s;
    overflow-wrap: anywhere;
}

.social-card:hover {
    transform: translateY(-5px);
    background: rgba(85,234,255,0.13);
    border-color: var(--cyan);
}

.social-icon {
    font-size: 22px;
}

.facebook { color: #82aaff; }
.instagram { color: #ff9acb; }
.youtube { color: #ff7777; }
.tiktok { color: #7df7ed; }
.whatsapp { color: #76f0a1; }

.contact-form {
    display: grid;
    gap: 13px;
}

.contact-form input,
.contact-form textarea {
    width: 100%;
    padding: 14px 15px;
    color: white;
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    outline: none;
    font: inherit;
}

.contact-form input:focus,
.contact-form textarea:focus {
    border-color: var(--cyan);
    box-shadow: 0 0 0 3px rgba(85,234,255,0.08);
}

.contact-form input::placeholder,
.contact-form textarea::placeholder {
    color: #aebbd5;
}

.contact-form textarea {
    min-height: 125px;
    resize: vertical;
}

.submit-btn {
    padding: 14px 20px;
    color: #071323;
    background: linear-gradient(90deg, var(--cyan), var(--purple));
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.2s, filter 0.2s;
}

.submit-btn:hover {
    transform: translateY(-2px);
    filter: brightness(1.1);
}

.notice {
    margin: 0 auto 15px;
    padding: 13px;
    border-radius: 12px;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

.success {
    color: #b7ffcf;
    background: rgba(40,200,100,0.12);
    border: 1px solid rgba(40,200,100,0.3);
}

.error {
    color: #ffc1c1;
    background: rgba(255,70,70,0.1);
    border: 1px solid rgba(255,70,70,0.3);
}

footer {
    padding: 28px 10px 10px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.8;
}

#back-to-top {
    position: fixed;
    right: 18px;
    bottom: 18px;
    width: 46px;
    height: 46px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50%;
    background: rgba(85,234,255,0.2);
    color: white;
    font-size: 22px;
    cursor: pointer;
    z-index: 5;
    display: none;
    backdrop-filter: blur(8px);
}

#back-to-top.visible {
    display: block;
}

#loader {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #080d20;
    transition: opacity 0.45s, visibility 0.45s;
}

#loader.hidden {
    opacity: 0;
    visibility: hidden;
}

.loader-ring {
    width: 55px;
    height: 55px;
    border: 4px solid rgba(255,255,255,0.12);
    border-top-color: var(--cyan);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@keyframes typingBlink {
    50% { opacity: 0; }
}

@keyframes logoGlow {
    from { box-shadow: 0 0 15px rgba(85,234,255,0.25); }
    to { box-shadow: 0 0 32px rgba(167,139,250,0.5); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
    .content {
        width: 94%;
        padding-top: 18px;
    }

    .hero {
        padding: 25px 13px;
        border-radius: 22px;
    }

    .section {
        padding: 22px 13px;
    }

    .social-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .social-card {
        font-size: 14px;
        min-height: 58px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
</head>

<body>
<div id="loader" aria-label="Loading">
    <div class="loader-ring"></div>
</div>

<canvas id="space-canvas"></canvas>
<div class="mouse-glow" id="mouse-glow"></div>

<main class="content">
    <div class="topbar">
        <button class="language-btn" id="language-btn"
                type="button" onclick="toggleLanguage()">
            English
        </button>
    </div>

    <section class="hero">
        <img class="logo" src="/static/logo.png"
             alt="MD Rifat Sheikh Logo"
             onerror="this.style.display='none'">

        <h1>MD Rifat Sheikh</h1>

        <p class="typing-line" aria-live="polite">
            <span id="typing-text">কনটেন্ট ক্রিয়েটর</span><span class="typing-cursor">|</span>
        </p>

        <p class="subtitle" id="subtitle">
            আমার অফিসিয়াল ওয়েবসাইটে স্বাগতম ✨
        </p>

        <div class="clock-box">
            <div class="clock-label" id="clock-label">
                বাংলাদেশের বর্তমান সময়
            </div>
            <div id="clock">--:--:--</div>
            <div id="date">তারিখ লোড হচ্ছে...</div>
        </div>
    </section>

    <section class="section">
        <h2 id="social-heading">🌐 আমার সোশ্যাল মিডিয়া</h2>

        <div class="social-grid">
            <a class="social-card" href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank" rel="noopener noreferrer">
                <span class="social-icon facebook">f</span>
                <span>Facebook</span>
            </a>

            <a class="social-card" href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank" rel="noopener noreferrer">
                <span class="social-icon instagram">◎</span>
                <span>Instagram</span>
            </a>

            <a class="social-card" href="https://www.youtube.com/"
               target="_blank" rel="noopener noreferrer">
                <span class="social-icon youtube">▶</span>
                <span>YouTube</span>
            </a>

            <a class="social-card" href="https://www.tiktok.com/"
               target="_blank" rel="noopener noreferrer">
                <span class="social-icon tiktok">♪</span>
                <span>TikTok</span>
            </a>

            <a class="social-card" href="https://www.whatsapp.com/"
               target="_blank" rel="noopener noreferrer">
                <span class="social-icon whatsapp">☏</span>
                <span>WhatsApp</span>
            </a>
        </div>
    </section>

    <section class="section">
        <h2 id="contact-heading">📩 যোগাযোগ করুন</h2>

        <!-- STATUS -->

        <form class="contact-form" method="POST" action="/">
            <input type="text" name="name" id="contact-name"
                   placeholder="আপনার নাম" maxlength="100" required>

            <input type="email" name="email" id="contact-email"
                   placeholder="আপনার ইমেইল" maxlength="254" required>

            <textarea name="message" id="contact-message"
                      placeholder="আপনার মেসেজ লিখুন..."
                      maxlength="5000" required></textarea>

            <button class="submit-btn" id="submit-btn" type="submit">
                মেসেজ পাঠান ✉️
            </button>
        </form>
    </section>

    <footer>
        <p id="footer-text">© 2026 MD Rifat Sheikh. সর্বস্বত্ব সংরক্ষিত।</p>
        <p>Made with ❤️ in Bangladesh 🇧🇩</p>
    </footer>
</main>

<button id="back-to-top" type="button"
        aria-label="Back to top" title="Back to top">↑</button>

<script>
let currentLanguage = "bn";

/* Typing Animation */
const typingWords = {
    bn: [
        "কনটেন্ট ক্রিয়েটর",
        "আমার ওয়েবসাইটে স্বাগতম",
        "স্বপ্ন দেখি, এগিয়ে যাই",
        "MD Rifat Sheikh"
    ],
    en: [
        "Content Creator",
        "Welcome to My Website",
        "Dream Big, Work Hard",
        "MD Rifat Sheikh"
    ]
};

let typingWordIndex = 0;
let typingCharIndex = 0;
let isDeleting = false;
let typingTimer = null;

function runTypingAnimation() {
    const element = document.getElementById("typing-text");
    if (!element) return;

    const words = typingWords[currentLanguage];
    const word = words[typingWordIndex];

    element.textContent = word.substring(0, typingCharIndex);

    let delay = isDeleting ? 45 : 90;

    if (!isDeleting) {
        typingCharIndex++;

        if (typingCharIndex > word.length) {
            typingCharIndex = word.length;
            isDeleting = true;
            delay = 1400;
        }
    } else {
        typingCharIndex--;

        if (typingCharIndex < 0) {
            typingCharIndex = 0;
            isDeleting = false;
            typingWordIndex = (typingWordIndex + 1) % words.length;
        }
    }

    typingTimer = setTimeout(runTypingAnimation, delay);
}

function restartTypingAnimation() {
    clearTimeout(typingTimer);
    typingWordIndex = 0;
    typingCharIndex = 0;
    isDeleting = false;

    const element = document.getElementById("typing-text");
    if (element) element.textContent = "";

    runTypingAnimation();
}

/* Bengali and English translations */
const translations = {
    bn: {
        button: "English",
        subtitle: "আমার অফিসিয়াল ওয়েবসাইটে স্বাগতম ✨",
        clock: "বাংলাদেশের বর্তমান সময়",
        dateLoading: "তারিখ লোড হচ্ছে...",
        social: "🌐 আমার সোশ্যাল মিডিয়া",
        contact: "📩 যোগাযোগ করুন",
        name: "আপনার নাম",
        email: "আপনার ইমেইল",
        message: "আপনার মেসেজ লিখুন...",
        send: "মেসেজ পাঠান ✉️",
        footer: "© 2026 MD Rifat Sheikh. সর্বস্বত্ব সংরক্ষিত।"
    },
    en: {
        button: "বাংলা",
        subtitle: "Welcome to my official website ✨",
        clock: "Current Bangladesh Time",
        dateLoading: "Loading date...",
        social: "🌐 My Social Media",
        contact: "📩 Contact Me",
        name: "Your name",
        email: "Your email",
        message: "Write your message...",
        send: "Send Message ✉️",
        footer: "© 2026 MD Rifat Sheikh. All rights reserved."
    }
};

function applyLanguage() {
    const t = translations[currentLanguage];

    document.documentElement.lang = currentLanguage;
    document.getElementById("language-btn").textContent = t.button;
    document.getElementById("subtitle").textContent = t.subtitle;
    document.getElementById("clock-label").textContent = t.clock;
    document.getElementById("social-heading").textContent = t.social;
    document.getElementById("contact-heading").textContent = t.contact;
    document.getElementById("contact-name").placeholder = t.name;
    document.getElementById("contact-email").placeholder = t.email;
    document.getElementById("contact-message").placeholder = t.message;
    document.getElementById("submit-btn").textContent = t.send;
    document.getElementById("footer-text").textContent = t.footer;

    restartTypingAnimation();
    updateClock();
}

function toggleLanguage() {
    currentLanguage = currentLanguage === "bn" ? "en" : "bn";
    applyLanguage();
}

/* Bangladesh live clock and date */
function updateClock() {
    const now = new Date();

    document.getElementById("clock").textContent =
        new Intl.DateTimeFormat("en-GB", {
            timeZone: "Asia/Dhaka",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true
        }).format(now);

    const locale = currentLanguage === "bn" ? "bn-BD" : "en-GB";

    document.getElementById("date").textContent =
        new Intl.DateTimeFormat(locale, {
            timeZone: "Asia/Dhaka",
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        }).format(now);
}

/* Welcome message */
function showWelcome() {
    console.log("Welcome to MD Rifat Sheikh's website!");
}

/* Loading screen */
window.addEventListener("load", function () {
    setTimeout(function () {
        document.getElementById("loader").classList.add("hidden");
    }, 350);
});

/* Back to top button */
const backToTop = document.getElementById("back-to-top");

window.addEventListener("scroll", function () {
    if (window.scrollY > 300) {
        backToTop.classList.add("visible");
    } else {
        backToTop.classList.remove("visible");
    }
});

backToTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

/* Mouse glow */
const glow = document.getElementById("mouse-glow");

if (window.matchMedia("(pointer: fine)").matches) {
    window.addEventListener("mousemove", function (event) {
        glow.style.left = event.clientX + "px";
        glow.style.top = event.clientY + "px";
    });
} else {
    glow.style.display = "none";
}

/* Animated star particles */
const canvas = document.getElementById("space-canvas");
const ctx = canvas.getContext("2d");
let stars = [];
let canvasWidth = 0;
let canvasHeight = 0;

function resizeCanvas() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);

    canvasWidth = window.innerWidth;
    canvasHeight = window.innerHeight;

    canvas.width = canvasWidth * ratio;
    canvas.height = canvasHeight * ratio;
    canvas.style.width = canvasWidth + "px";
    canvas.style.height = canvasHeight + "px";

    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    const count = Math.min(
        100,
        Math.max(35, Math.floor(canvasWidth / 12))
    );

    stars 
