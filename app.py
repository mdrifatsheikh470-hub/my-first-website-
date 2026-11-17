
import os
import re
import html
import smtplib
from email.message import EmailMessage
from flask import Flask, request

app = Flask(__name__)

EMAIL_TO = "mdrifatsheikh470@gmail.com"


@app.route("/", methods=["GET", "POST"])
def home():
    language = request.form.get("language", "bn")
    if language not in ("bn", "en"):
        language = "bn"

    status_html = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sender = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not sender or not message:
            error = (
                "সব ঘর পূরণ করুন।" if language == "bn"
                else "Please fill in all fields."
            )
            status_html = (
                '<div class="notice error">' + html.escape(error) + "</div>"
            )

        elif (
            len(name) > 100
            or len(sender) > 254
            or len(message) > 5000
            or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender)
        ):
            error = (
                "সঠিক তথ্য দিয়ে আবার চেষ্টা করুন।" if language == "bn"
                else "Please check your information and try again."
            )
            status_html = (
                '<div class="notice error">' + html.escape(error) + "</div>"
            )

        else:
            username = os.environ.get("MAIL_USERNAME", "")
            password = os.environ.get("MAIL_PASSWORD", "")

            if not username or not password:
                error = (
                    "ইমেইল সেটআপ করা হয়নি। পরে আবার চেষ্টা করুন।"
                    if language == "bn"
                    else "Email is not configured. Please try later."
                )
                status_html = (
                    '<div class="notice error">'
                    + html.escape(error) + "</div>"
                )
            else:
                try:
                    email = EmailMessage()
                    email["Subject"] = "Website Contact Form"
                    email["From"] = username
                    email["To"] = EMAIL_TO
                    email["Reply-To"] = sender
                    email.set_content(
                        f"Name: {name}\n"
                        f"Email: {sender}\n\n"
                        f"Message:\n{message}"
                    )

                    with smtplib.SMTP_SSL(
                        "smtp.gmail.com", 465, timeout=20
                    ) as smtp:
                        smtp.login(username, password)
                        smtp.send_message(email)

                    success = (
                        "মেসেজ পাঠানো হয়েছে। ধন্যবাদ!"
                        if language == "bn"
                        else "Your message has been sent. Thank you!"
                    )
                    status_html = (
                        '<div class="notice success">'
                        + html.escape(success) + "</div>"
                    )

                except Exception:
                    app.logger.exception("Contact email failed")
                    error = (
                        "মেসেজ পাঠানো যায়নি। পরে আবার চেষ্টা করুন।"
                        if language == "bn"
                        else "Message failed. Please try again later."
                    )
                    status_html = (
                        '<div class="notice error">'
                        + html.escape(error) + "</div>"
                    )

    page = r'''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#070b1b">
<meta name="description" content="MD Rifat Sheikh personal website">
<title>MD Rifat Sheikh | Official Website</title>

<style>
:root {
    --bg: #070b1b;
    --panel: rgba(18, 27, 55, .82);
    --text: #f4f7ff;
    --muted: #b7c5e8;
    --cyan: #55e7ff;
    --purple: #a78bfa;
    --border: rgba(132, 177, 255, .25);
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    min-height: 100vh;
    overflow-x: hidden;
    background:
        radial-gradient(ellipse at 15% 15%, #172453, transparent 45%),
        radial-gradient(ellipse at 85% 75%, #25154b, transparent 40%),
        var(--bg);
    color: var(--text);
    font-family: Arial, sans-serif;
}

#spaceCanvas {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}

#mouseGlow {
    position: fixed;
    width: 300px;
    height: 300px;
    left: 50%;
    top: 50%;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    background: radial-gradient(
        circle,
        rgba(85, 231, 255, .16),
        rgba(167, 139, 250, .07) 42%,
        transparent 72%
    );
    pointer-events: none;
    z-index: 1;
    opacity: 0;
}

#page {
    position: relative;
    z-index: 2;
}

header {
    width: min(1050px, 92%);
    margin: auto;
    padding: 22px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
}

.brand {
    color: var(--cyan);
    font-weight: 800;
    letter-spacing: .5px;
}

button, .social-link {
    font: inherit;
}

button {
    cursor: pointer;
}

.lang-btn, .main-btn, .submit-btn, #topBtn {
    color: var(--text);
    background: rgba(36, 48, 87, .85);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 11px 15px;
    transition: box-shadow .2s, border-color .2s;
}

.lang-btn:hover, .main-btn:hover, .submit-btn:hover {
    border-color: var(--cyan);
    box-shadow: 0 0 20px rgba(85, 231, 255, .2);
}

.hero {
    width: min(950px, 92%);
    margin: 25px auto;
    padding: 35px 12px;
    text-align: center;
}

.logo-frame {
    width: 145px;
    height: 145px;
    margin: 0 auto 24px;
    border-radius: 50%;
    padding: 4px;
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    box-shadow: 0 0 32px rgba(85, 231, 255, .25);
    animation: floatLogo 4s ease-in-out infinite;
}

.logo-frame img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    background: #121a36;
}

@keyframes floatLogo {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
}

h1 {
    margin: 0;
    font-size: clamp(32px, 7vw, 56px);
    line-height: 1.2;
    background: linear-gradient(90deg, #fff, var(--cyan), #c4b5fd);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}

.subtitle {
    color: var(--muted);
    line-height: 1.8;
    font-size: 17px;
    margin: 17px 0 10px;
}

#typingText {
    color: var(--cyan);
    min-height: 25px;
    margin: 12px 0 20px;
}

.card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 15px 45px rgba(0, 0, 0, .18);
}

.clock-card {
    display: inline-block;
    max-width: 100%;
    padding: 18px 25px;
    margin: 15px auto;
}

.clock-label {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 8px;
}

#clock {
    color: var(--cyan);
    font-size: clamp(25px, 5vw, 34px);
    font-weight: bold;
    font-variant-numeric: tabular-nums;
}

#date {
    color: var(--muted);
    font-size: 14px;
    margin-top: 8px;
}

.section {
    width: min(850px, 92%);
    margin: 25px auto;
    padding: 25px;
}

.section h2 {
    margin: 0 0 20px;
    text-align: center;
    font-size: 23px;
}

.socials {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
}

.social-link {
    display: inline-block;
    min-width: 110px;
    padding: 13px 16px;
    border-radius: 12px;
    border: 1px solid var(--border);
    color: white;
    background: rgba(27, 39, 75, .85);
    text-decoration: none;
    text-align: center;
    font-size: 14px;
    font-weight: bold;
    transition: transform .2s, box-shadow .2s, border-color .2s;
}

.social-link:hover {
    border-color: var(--cyan);
    box-shadow: 0 10px 25px rgba(85, 231, 255, .18);
}

form {
    display: grid;
    gap: 13px;
}

input, textarea {
    width: 100%;
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: rgba(5, 10, 27, .85);
    color: white;
    font: inherit;
}

input::placeholder, textarea::placeholder {
    color: #aab8d8;
}

textarea {
    min-height: 125px;
    resize: vertical;
}

.submit-btn {
    background: linear-gradient(110deg, #2563eb, #7c3aed);
    border: none;
    font-weight: bold;
    padding: 14px;
}

.notice {
    margin-bottom: 15px;
    padding: 13px;
    border-radius: 12px;
    line-height: 1.6;
    text-align: center;
}

.success {
    background: rgba(22, 163, 74, .16);
    border: 1px solid rgba(74, 222, 128, .45);
}

.error {
    background: rgba(220, 38, 38, .15);
    border: 1px solid rgba(248, 113, 113, .45);
}

footer {
    padding: 25px 12px 35px;
    color: var(--muted);
    text-align: center;
    font-size: 13px;
    line-height: 1.9;
}

#topBtn {
    display: none;
    position: fixed;
    z-index: 5;
    right: 18px;
    bottom: 18px;
    width: 46px;
    height: 46px;
    padding: 0;
    border-radius: 50%;
    font-size: 22px;
}

#loader {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #070b1b;
    transition: opacity .3s, visibility .3s;
}

#loader.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.loader-content {
    color: var(--cyan);
    text-align: center;
}

.spinner {
    width: 44px;
    height: 44px;
    margin: 0 auto 15px;
    border: 3px solid rgba(85, 231, 255, .2);
    border-top-color: var(--cyan);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

button:focus-visible, a:focus-visible,
input:focus-visible, textarea:focus-visible {
    outline: 2px solid var(--cyan);
    outline-offset: 3px;
}

@media (hover: hover) and (pointer: fine) {
    .tilt {
        transition: transform .18s ease, box-shadow .2s ease;
        transform-style: preserve-3d;
    }
}

@media (max-width: 600px) {
    header {
        padding: 16px 0;
    }

    .brand {
        font-size: 13px;
    }

    .lang-btn {
        font-size: 12px;
        padding: 9px;
    }

    .hero {
        margin-top: 10px;
        padding: 25px 5px;
    }

    .logo-frame {
        width: 120px;
        height: 120px;
    }

    .section {
        padding: 20px 14px;
    }

    .social-link {
        flex: 1 1 38%;
        min-width: 0;
    }

    #mouseGlow {
        display: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
    }
}
</style>
</head>

<body>
<canvas id="spaceCanvas" aria-hidden="true"></canvas>
<div id="mouseGlow" aria-hidden="true"></div>

<div id="loader">
    <div class="loader-content">
        <div class="spinner"></div>
        <div id="loadingText">ওয়েবসাইট লোড হচ্ছে...</div>
    </div>
</div>

<div id="page">
<header>
    <div class="brand">✦ MD RIFAT SHEIKH</div>
    <button class="lang-btn" id="languageBtn" type="button">
        🌐 বাংলা | English
    </button>
</header>

<main>
    <section class="hero">
        <div class="logo-frame">
            <img src="/static/logo.png" alt="MD Rifat Sheikh Logo">
        </div>

        <h1>MD Rifat Sheikh</h1>
        <p class="subtitle" id="subtitle">
            আমার ব্যক্তিগত ওয়েবসাইটে আপনাকে স্বাগতম
        </p>
        <div id="typingText">Welcome to my universe ✨</div>

        <div class="card clock-card tilt">
            <div class="clock-label" id="clockLabel">
                বাংলাদেশের বর্তমান সময়
            </div>
            <div id="clock">--:--:--</div>
            <div id="date">তারিখ লোড হচ্ছে...</div>
        </div>

        <p>
            <a class="social-link" href="#social" id="exploreBtn">
                আমার সোশ্যাল মিডিয়া ↓
            </a>
        </p>
    </section>

    <section class="section card tilt" id="social">
        <h2 id="socialTitle">🌐 আমার সোশ্যাল মিডিয়া</h2>
        <div class="socials">
            <a class="social-link"
               href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank" rel="noopener noreferrer">📘 Facebook</a>

            <a class="social-link"
               href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank" rel="noopener noreferrer">📸 Instagram</a>

            <a class="social-link"
               href="https://www.youtube.com/"
               target="_blank" rel="noopener noreferrer">▶ YouTube</a>

            <a class="social-link"
               href="https://www.tiktok.com/"
               target="_blank" rel="noopener noreferrer">♪ TikTok</a>

            <a class="social-link"
               href="https://www.whatsapp.com/"
               target="_blank" rel="noopener noreferrer">💬 WhatsApp</a>
        </div>
    </section>

    <section class="section card tilt" id="contact">
        <h2 id="contactTitle">📩 আমার সঙ্গে যোগাযোগ করুন</h2>

        <!-- STATUS -->

        <form method="POST" action="/">
            <input type="hidden" name="language" id="formLanguage" value="bn">

            <input type="text" name="name" id="nameInput"
                   maxlength="100" placeholder="আপনার নাম" required>

            <input type="email" name="email" id="emailInput"
                   maxlength="254" placeholder="আপনার ইমেইল" required>

            <textarea name="message" id="messageInput"
                      maxlength="5000" placeholder="আপনার মেসেজ লিখুন..."
                      required></textarea>

            <button type="submit" class="submit-btn" id="sendBtn">
                মেসেজ পাঠান ✉️
            </button>
        </form>
    </section>
</main>

<footer>
    <div id="footerText">তৈরি করা হয়েছে ❤️ MD Rifat Sheikh-এর জন্য</div>
    <div>© <span id="year"></span> MD Rifat Sheikh. All rights reserved.</div>
</footer>
</div>

<button id="topBtn" type="button" aria-label="Back to top"
        title="উপরে যান">↑</button>

<script>
(function () {
    "use strict";

    const canvas = document.getElementById("spaceCanvas");
    const ctx = canvas.getContext("2d");
    const glow = document.getElementById("mouseGlow");
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    let width = 0;
    let height = 0;
    let particles = [];
    let animationFrame = null;

    function resizeCanvas() {
        width = window.innerWidth;
        height = window.innerHeight;

        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        canvas.style.width = width + "px";
        canvas.style.height = height + "px";
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const count = Math.min(
            140,
            Math.max(40, Math.floor(width * height / 8000))
        );

        particles = Array.from({ length: count }, function () {
            return {
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5 + 0.4,
                speed: Math.random() * 0.3 + 0.06,
                alpha: Math.random() * 0.6 + 0.25,
                phase: Math.random() * Math.PI * 2
            };
        });

        drawStars(true);
    }

    function drawStars(staticFrame) {
        ctx.clearRect(0, 0, width, height);

        particles.forEach(function (p) {
            if (!staticFrame && !reducedMotion) {
                p.y -= p.speed;
                p.phase += 0.02;

                if (p.y < -3) {
                    p.y = height + 3;
                    p.x = Math.random() * width;
                }
            }

            const twinkle = reducedMotion
                ? 1
                : 0.7 + Math.sin(p.phase) * 0.3;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle =
                "rgba(195,220,255," + (p.alpha * twinkle) + ")";
            ctx.fill();
        });

        if (!staticFrame && !reducedMotion && !document.hidden) {
            animationFrame = requestAnimationFrame(function () {
                animationFrame = null;
                drawStars(false);
            });
        }
    }

    function stopStars() {
        if (animationFrame !== null) {
            cancelAnimationFrame(animationFrame);
            animationFrame = null;
        }
    }

    function startStars() {
        if (!reducedMotion && !document.hidden && animationFrame === null) {
            animationFrame = requestAnimationFrame(function () {
                animationFrame = null;
                drawStars(false);
            });
        }
    }

    window.addEventListener("resize", resizeCanvas, { passive: true });

    window.addEventListener("pointermove", function (event) {
        if (event.pointerType === "touch") return;
        glow.style.left = event.clientX + "px";
        glow.style.top = event.clientY + "px";
        glow.style.opacity = "1";
    }, { passive: true });

    document.addEventListener("pointerleave", function () {
        glow.style.opacity = "0";
    });

    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            stopStars();
        } else {
            startStars();
        }
    });

    resizeCanvas();
    startStars();

    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches
        && !reducedMotion) {
        document.querySelectorAll(".tilt, .social-link").forEach(
            function (card) {
                card.addEventListener("pointermove", function (event) {
                    const rect = card.getBoundingClientRect();
                    const x = (event.clientX - rect.left) / rect.width;
                    const y = (event.clientY - rect.top) / rect.height;
                    const rx = (0.5 - y) * 6;
                    const ry = (x - 0.5) * 6;

                    card.style.transform =
                        "perspective(800px) rotateX(" + rx +
                        "deg) rotateY(" + ry + "deg) translateY(-3px)";
                });

                card.addEventListener("pointerleave", function () {
                    card.style.transform = "";
                });
            }
        );
    }
})();

let currentLanguage = "__INITIAL_LANGUAGE__";

const translations = {
    bn: {
        subtitle: "আমার ব্যক্তিগত ওয়েবসাইটে আপনাকে স্বাগতম",
        typing: [
            "Welcome to my universe ✨",
            "স্বাগতম আমার ওয়েবসাইটে 🌌"
        ],
        clock: "বাংলাদেশের বর্তমান সময়",
        explore: "আমার সোশ্যাল মিডিয়া ↓",
        social: "🌐 আমার সোশ্যাল মিডিয়া",
        contact: "📩 আমার সঙ্গে যোগাযোগ করুন",
        name: "আপনার নাম",
        email: "আপনার ইমেইল",
        message: "আপনার মেসেজ লিখুন...",
        send: "মেসেজ পাঠান ✉️",
        footer: "তৈরি করা হয়েছে ❤️ MD Rifat Sheikh-এর জন্য",
        loading: "ওয়েবসাইট লোড হচ্ছে..."
    },
    en: {
        subtitle: "Welcome to my personal website",
        typing: [
            "Welcome to my universe ✨",
            "Explore my digital space 🌌"
        ],
        clock: "Current Bangladesh Time",
        explore: "Explore My Social Media ↓",
        social: "🌐 My Social Media",
        contact: "📩 Contact Me",
        name: "Your name",
        email: "Your email",
        message: "Write your message...",
        send: "Send Message ✉️",
        footer: "Made with ❤️ for MD Rifat Sheikh",
        loading: "Loading website..."
    }
};

function
