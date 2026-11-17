
import os
import smtplib
import random
import html
from email.message import EmailMessage
from flask import Flask, request

app = Flask(__name__)

EMAIL_TO = "mdrifatsheikh470@gmail.com"


@app.route("/", methods=["GET", "POST"])
def home():
    status_html = ""
    language = "bn"

    if request.method == "POST":
        language = request.form.get("language", "bn")
        if language not in ("bn", "en"):
            language = "bn"

        name = request.form.get("name", "").strip()
        sender_email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not sender_email or not message:
            status = (
                "সব ঘর পূরণ করুন।"
                if language == "bn"
                else "Please fill in all fields."
            )
            status_html = (
                '<div class="notice error">'
                + html.escape(status)
                + "</div>"
            )
        elif len(name) > 100 or len(sender_email) > 254 or len(message) > 5000:
            status = (
                "আপনার লেখা অনেক বড়। আবার চেষ্টা করুন।"
                if language == "bn"
                else "Your message is too long. Please try again."
            )
            status_html = (
                '<div class="notice error">'
                + html.escape(status)
                + "</div>"
            )
        elif "\n" in sender_email or "\r" in sender_email:
            status = (
                "সঠিক ইমেইল ঠিকানা দিন।"
                if language == "bn"
                else "Please enter a valid email address."
            )
            status_html = (
                '<div class="notice error">'
                + html.escape(status)
                + "</div>"
            )
        else:
            mail_user = os.environ.get("MAIL_USERNAME", "")
            mail_password = os.environ.get("MAIL_PASSWORD", "")

            if not mail_user or not mail_password:
                status = (
                    "ইমেইল সেটআপ সম্পূর্ণ হয়নি। পরে আবার চেষ্টা করুন।"
                    if language == "bn"
                    else "Email is not configured yet. Please try later."
                )
                status_html = (
                    '<div class="notice error">'
                    + html.escape(status)
                    + "</div>"
                )
            else:
                try:
                    email_message = EmailMessage()
                    email_message["Subject"] = "Website Contact Form"
                    email_message["From"] = mail_user
                    email_message["To"] = EMAIL_TO
                    email_message.set_content(
                        f"Name: {name}\n"
                        f"Email: {sender_email}\n\n"
                        f"Message:\n{message}"
                    )

                    with smtplib.SMTP_SSL(
                        "smtp.gmail.com", 465, timeout=20
                    ) as smtp:
                        smtp.login(mail_user, mail_password)
                        smtp.send_message(email_message)

                    status = (
                        "আপনার মেসেজ পাঠানো হয়েছে। ধন্যবাদ!"
                        if language == "bn"
                        else "Your message has been sent. Thank you!"
                    )
                    status_html = (
                        '<div class="notice success">'
                        + html.escape(status)
                        + "</div>"
                    )
                except Exception:
                    app.logger.exception("Contact form email failed")
                    status = (
                        "মেসেজ পাঠানো যায়নি। পরে আবার চেষ্টা করুন।"
                        if language == "bn"
                        else "Message could not be sent. Please try again."
                    )
                    status_html = (
                        '<div class="notice error">'
                        + html.escape(status)
                        + "</div>"
                    )

    page = r"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#070b1b">
<meta name="description" content="Official personal website of MD Rifat Sheikh.">
<title>MD Rifat Sheikh | Official Website</title>

<style>
:root {
    --bg: #070b1b;
    --panel: rgba(18, 27, 55, .75);
    --text: #f4f7ff;
    --muted: #b7c5e8;
    --cyan: #55e7ff;
    --purple: #a78bfa;
    --border: rgba(132, 177, 255, .22);
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
        radial-gradient(ellipse at 20% 15%, #172453 0%, transparent 42%),
        radial-gradient(ellipse at 85% 70%, #25154b 0%, transparent 38%),
        var(--bg);
    color: var(--text);
    font-family: Arial, "Noto Sans Bengali", sans-serif;
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
    top: 50%;
    left: 50%;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(68, 205, 255, .15),
        rgba(139, 92, 246, .08) 42%,
        transparent 72%
    );
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 1;
    opacity: 0;
    transition: opacity .25s;
}

#page {
    position: relative;
    z-index: 2;
}

header {
    width: min(1100px, 92%);
    margin: auto;
    padding: 22px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
}

.brand {
    font-size: 17px;
    font-weight: 800;
    color: var(--cyan);
    letter-spacing: .5px;
}

.lang-btn, .main-btn, .submit-btn, #topBtn {
    border: 1px solid var(--border);
    color: var(--text);
    background: rgba(36, 48, 87, .8);
    border-radius: 12px;
    padding: 11px 16px;
    font-size: 14px;
    cursor: pointer;
    transition: .25s ease;
}

.lang-btn:hover, .main-btn:hover, .submit-btn:hover, #topBtn:hover {
    border-color: var(--cyan);
    box-shadow: 0 0 22px rgba(85, 231, 255, .2);
}

.hero {
    width: min(1000px, 92%);
    margin: 35px auto 25px;
    padding: 42px 20px;
    text-align: center;
}

.logo-frame {
    width: 150px;
    height: 150px;
    margin: 0 auto 24px;
    border-radius: 50%;
    padding: 4px;
    background: linear-gradient(135deg, var(--cyan), var(--purple), #4266ff);
    box-shadow: 0 0 35px rgba(85, 231, 255, .22);
    animation: floatLogo 4s ease-in-out infinite;
}

.logo-frame img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
    border-radius: 50%;
    background: #121a36;
}

@keyframes floatLogo {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

h1 {
    margin: 0;
    font-size: clamp(32px, 6vw, 58px);
    line-height: 1.2;
    font-weight: 900;
    letter-spacing: -.8px;
    background: linear-gradient(90deg, #fff, var(--cyan), #c4b5fd);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}

.subtitle {
    color: var(--muted);
    font-size: clamp(15px, 2.4vw, 19px);
    margin: 18px auto 12px;
    line-height: 1.8;
}

.typing {
    color: var(--cyan);
    min-height: 28px;
    margin: 8px 0 20px;
    font-size: 16px;
}

.clock-card {
    width: fit-content;
    max-width: 100%;
    margin: 22px auto;
    padding: 17px 24px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: rgba(11, 18, 41, .72);
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 35px rgba(0, 0, 0, .15);
}

.clock-label {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 8px;
}

#clock {
    color: var(--cyan);
    font-size: clamp(23px, 5vw, 34px);
    font-weight: 800;
    font-variant-numeric: tabular-nums;
}

#date {
    color: var(--muted);
    font-size: 14px;
    margin-top: 7px;
}

.section {
    width: min(850px, 92%);
    margin: 28px auto;
    padding: 25px;
    border: 1px solid var(--border);
    border-radius: 22px;
    background: var(--panel);
    backdrop-filter: blur(12px);
    box-shadow: 0 16px 50px rgba(0, 0, 0, .15);
}

.section h2 {
    margin: 0 0 18px;
    font-size: 23px;
    text-align: center;
}

.socials {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.social-link {
    min-width: 110px;
    padding: 13px 16px;
    text-decoration: none;
    text-align: center;
    color: white;
    border: 1px solid var(--border);
    border-radius: 13px;
    background: rgba(27, 39, 75, .85);
    font-size: 14px;
    font-weight: 700;
    transform-style: preserve-3d;
    transition: border-color .25s, box-shadow .25s, background .25s;
}

.social-link:hover {
    border-color: var(--cyan);
    background: rgba(41, 61, 109, .95);
    box-shadow: 0 12px 25px rgba(85, 231, 255, .16);
}

.social-link:focus-visible, button:focus-visible, input:focus-visible,
textarea:focus-visible {
    outline: 2px solid var(--cyan);
    outline-offset: 3px;
}

form {
    display: grid;
    gap: 13px;
}

input, textarea {
    width: 100%;
    padding: 14px 15px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(5, 10, 27, .75);
    color: white;
    font: inherit;
}

input::placeholder, textarea::placeholder {
    color: #9eacd0;
}

textarea {
    min-height: 130px;
    resize: vertical;
}

.submit-btn {
    background: linear-gradient(110deg, #2563eb, #7c3aed);
    border: none;
    font-weight: 800;
    padding: 14px;
}

.notice {
    padding: 12px 14px;
    border-radius: 12px;
    margin-bottom: 14px;
    text-align: center;
    line-height: 1.6;
}

.success {
    background: rgba(22, 163, 74, .16);
    border: 1px solid rgba(74, 222, 128, .45);
}

.error {
    background: rgba(220, 38, 38, .14);
    border: 1px solid rgba(248, 113, 113, .45);
}

footer {
    text-align: center;
    padding: 25px 15px 35px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.8;
}

#topBtn {
    position: fixed;
    z-index: 5;
    right: 18px;
    bottom: 18px;
    display: none;
    width: 46px;
    height: 46px;
    padding: 0;
    font-size: 21px;
    border-radius: 50%;
}

#loader {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #070b1b;
    transition: opacity .4s ease, visibility .4s ease;
}

#loader.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.loader-content {
    text-align: center;
    color: var(--cyan);
    font-weight: 700;
}

.spinner {
    width: 45px;
    height: 45px;
    margin: 0 auto 16px;
    border: 3px solid rgba(85, 231, 255, .18);
    border-top-color: var(--cyan);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@media (hover: hover) and (pointer: fine) {
    .tilt-card {
        transition: transform .18s ease, box-shadow .25s ease;
        transform-style: preserve-3d;
    }
}

@media (max-width: 600px) {
    header {
        padding: 16px 0;
    }

    .brand {
        font-size: 14px;
    }

    .lang-btn {
        padding: 9px 11px;
        font-size: 12px;
    }

    .hero {
        margin-top: 12px;
        padding: 28px 8px;
    }

    .logo-frame {
        width: 125px;
        height: 125px;
    }

    .section {
        padding: 20px 15px;
        margin: 20px auto;
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
        scroll-behavior: auto !important;
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
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
    <button class="lang-btn" id="languageBtn" type="button"
            onclick="toggleLanguage()">🌐 বাংলা | English</button>
</header>

<main>
    <section class="hero">
        <div class="logo-frame">
            <img src="/static/logo.png" alt="MD Rifat Sheikh Logo"
                 onerror="this.style.display='none'">
        </div>

        <h1>MD Rifat Sheikh</h1>
        <p class="subtitle" id="subtitle">
            আমার ব্যক্তিগত ওয়েবসাইটে আপনাকে স্বাগতম
        </p>
        <div class="typing" id="typingText">Welcome to my universe ✨</div>

        <div class="clock-card tilt-card">
            <div class="clock-label" id="clockLabel">বাংলাদেশের বর্তমান সময়</div>
            <div id="clock">--:--:--</div>
            <div id="date">তারিখ লোড হচ্ছে...</div>
        </div>

        <a class="social-link" href="#social" id="exploreBtn"
           style="display:inline-block; margin-top:10px;">
           আমার সোশ্যাল মিডিয়া ↓
        </a>
    </section>

    <section class="section tilt-card" id="social">
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

    <section class="section tilt-card" id="contact">
        <h2 id="contactTitle">📩 আমার সঙ্গে যোগাযোগ করুন</h2>

        <!-- STATUS -->

        <form method="POST" action="/">
            <input type="hidden" name="language" id="formLanguage" value="bn">

            <input type="text" name="name" id="nameInput"
                   placeholder="আপনার নাম" maxlength="100" required>

            <input type="email" name="email" id="emailInput"
                   placeholder="আপনার ইমেইল" maxlength="254" required>

            <textarea name="message" id="messageInput"
                      placeholder="আপনার মেসেজ লিখুন..."
                      maxlength="5000" required></textarea>

            <button type="submit" class="submit-btn" id="sendBtn">
                মেসেজ পাঠান ✉️
            </button>
        </form>
    </section>
</main>

<footer>
    <div id="footerText">তৈরি করা হয়েছে ❤️ MD Rifat Sheikh-এর জন্য</div>
    <div id="footerDate">© <span id="year"></span> MD Rifat Sheikh. All rights reserved.</div>
</footer>
</div>

<button id="topBtn" type="button" title="উপরে যান"
        aria-label="Back to top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>

<script>
(() => {
    const canvas = document.getElementById("spaceCanvas");
    const ctx = canvas.getContext("2d");
    const glow = document.getElementById("mouseGlow");
    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    let width = 0, height = 0, dpr = 1;
    let particles = [];
    let frame = null;
    let lastTime = 0;

    function makeParticles() {
        const count = Math.min(
            150,
            Math.max(45, Math.floor(width * height / 7500))
        );

        particles = Array.from({length: count}, () => ({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.5 + .35,
            speed: Math.random() * .24 + .06,
            drift: (Math.random() - .5) * .22,
            alpha: Math.random() * .65 + .2,
            phase: Math.random() * Math.PI * 2
        }));
    }

    function resize() {
        dpr = Math.min(window.devicePixelRatio || 1, 2);
        width = window.innerWidth;
        height = window.innerHeight;

        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        canvas.style.width = width + "px";
        canvas.style.height = height + "px";

        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        makeParticles();
        draw(0, true);
    }

    function draw(time, still = false) {
        ctx.clearRect(0, 0, width, height);

        for (const p of particles) {
            if (!reduceMotion && !still) {
                p.y -= p.speed;
                p.x += p.drift;
                p.phase += .018;

                if (p.y < -4) {
                    p.y = height + 4;
                    p.x = Math.random() * width;
                }
                if (p.x < -4) p.x = width + 4;
                if (p.x > width + 4) p.x = -4;
            }

            const twinkle = reduceMotion
                ? 1
                : .65 + Math.sin(p.phase) * .35;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(192,220,255,${p.alpha * twinkle})`;
            ctx.fill();

            // Tiny soft space glow on selected stars
            if (p.radius > 1.15) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius * 3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(100,170,255,${p.alpha * .09})`;
                ctx.fill();
            }
        }

        if (!reduceMotion && !document.hidden) {
            frame = requestAnimationFrame(draw);
        }
    }

    function startAnimation() {
        if (!reduceMotion && !document.hidden && frame === null) {
            frame = requestAnimationFrame(draw);
        }
    }

    function stopAnimation() {
        if (frame !== null) {
            cancelAnimationFrame(frame);
            frame = null;
        }
    }

    window.addEventListener("resize", () => {
        resize();
    }, {passive:true});

    window.addEventListener("pointermove", event => {
        if (event.pointerType === "touch") return;
        glow.style.left = event.clientX + "px";
        glow.style.top = event.clientY + "px";
        glow.style.opacity = "1";
    }, {passive:true});

    document.addEventListener("pointerout", event => {
        if (!event.relatedTarget) glow.style.opacity = "0";
    });

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            stopAnimation();
        } else {
            startAnimation();
        }
    });

    resize();
    if (reduceMotion) {
        stopAnimation();
    } else {
        startAnimation();
    }

    // Subtle 3D tilt for cards on mouse devices
    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches
        && !reduceMotion) {
        document.querySelectorAll(".tilt-card, .social-link").forEach(card => {
            card.addEventListener("pointermove", event => {
                const rect = card.getBoundingClientRect();
                const x = (event.clientX - rect.left) / rect.width;
                const y = (event.clientY - rect.top) / rect.height;
                const rotateY = (x - .5) * 7;
                const rotateX = (.5 - y) * 7;

                card.style.transform =
                    `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)`;
            });

        
