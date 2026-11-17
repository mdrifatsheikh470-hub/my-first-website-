
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#050816">
    <title>MD Rifat Sheikh | Official Website</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;
            overflow-x: hidden;
            padding: 35px 15px;
            text-align: center;
            color: white;
            font-family: Arial, sans-serif;
            background: linear-gradient(
                -45deg,
                #050816,
                #101827,
                #171044,
                #062b49
            );
            background-size: 400% 400%;
            animation: spaceBackground 14s ease infinite;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background-image:
                radial-gradient(2px 2px at 20% 30%, white 70%, transparent),
                radial-gradient(2px 2px at 70% 60%, #38bdf8 70%, transparent),
                radial-gradient(1px 1px at 40% 80%, white 70%, transparent),
                radial-gradient(2px 2px at 85% 20%, #a78bfa 70%, transparent),
                radial-gradient(1px 1px at 10% 70%, white 70%, transparent);
            background-size: 250px 250px;
            animation: starMove 18s linear infinite;
        }

        .page {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 650px;
            margin: 0 auto;
        }

        @keyframes spaceBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes starMove {
            from { transform: translateY(0); }
            to { transform: translateY(-250px); }
        }

        .animated-logo {
            display: block;
            width: 220px;
            max-width: 75%;
            height: auto;
            margin: 10px auto 22px;
            border-radius: 20px;
            animation:
                floatLogo 3s ease-in-out infinite,
                glowLogo 2s ease-in-out infinite alternate;
        }

        @keyframes floatLogo {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        @keyframes glowLogo {
            from { filter: drop-shadow(0 0 5px #0284c7); }
            to { filter: drop-shadow(0 0 22px #38bdf8); }
        }

        h1 {
            color: #7dd3fc;
            font-size: clamp(27px, 7vw, 40px);
            margin: 10px 0;
            text-shadow: 0 0 18px rgba(56, 189, 248, 0.65);
        }

        .subtitle {
            color: #cbd5e1;
            font-size: 15px;
            margin: 12px 0 25px;
        }

        /* LIVE CLOCK */

        .clock-card {
            width: 100%;
            max-width: 380px;
            margin: 25px auto;
            padding: 25px 15px;
            border: 1px solid rgba(56, 189, 248, 0.65);
            border-radius: 22px;
            background: rgba(10, 20, 45, 0.78);
            box-shadow: 0 0 28px rgba(56, 189, 248, 0.17);
            backdrop-filter: blur(10px);
        }

        .clock-title {
            color: #7dd3fc;
            font-size: 13px;
            letter-spacing: 3px;
            margin-bottom: 14px;
        }

        #live-clock {
            color: #ffffff;
            font-size: clamp(34px, 9vw, 48px);
            font-weight: bold;
            font-variant-numeric: tabular-nums;
            text-shadow: 0 0 18px #38bdf8;
            white-space: nowrap;
        }

        #live-date {
            color: #cbd5e1;
            font-size: 15px;
            margin-top: 12px;
            line-height: 1.7;
        }

        .time-zone {
            color: #7dd3fc;
            font-size: 11px;
            margin-top: 10px;
            letter-spacing: 1px;
        }

        /* WELCOME BUTTON */

        .welcome-button {
            display: inline-block;
            margin: 12px auto;
            padding: 14px 25px;
            border: 1px solid #7dd3fc;
            border-radius: 12px;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            color: #07111f;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.25s, box-shadow 0.25s;
        }

        .welcome-button:hover {
            transform: translateY(-4px);
            box-shadow: 0 0 24px rgba(56, 189, 248, 0.65);
        }

        /* SOCIAL MEDIA */

        .social-section {
            margin: 38px auto 28px;
        }

        .social-section h2 {
            color: #e0f2fe;
            font-size: 23px;
            margin-bottom: 22px;
        }

        .social-icons {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 18px 14px;
            max-width: 450px;
            margin: 0 auto;
        }

        .social-item {
            width: 72px;
        }

        .social-icon {
            width: 60px;
            height: 60px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
            border-radius: 18px;
            color: white;
            font-size: 29px;
            font-weight: bold;
            text-decoration: none;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 5px 18px rgba(0, 0, 0, 0.25);
            transition: transform 0.25s, box-shadow 0.25s;
        }

        .social-icon:hover {
            transform: translateY(-6px) scale(1.07);
            box-shadow: 0 0 22px currentColor;
        }

        .facebook { background: #1877F2; }

        .instagram {
            background: linear-gradient(
                45deg,
                #feda75,
                #fa7e1e,
                #d62976,
                #962fbf,
                #4f5bd5
            );
        }

        .youtube { background: #ff0033; }
        .tiktok { background: #111111; }
        .whatsapp { background: #128C7E; }

        .social-label {
            font-size: 12px;
            margin-top: 9px;
            color: #dbeafe;
        }

        .footer {
            margin-top: 35px;
            padding: 20px 5px;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.8;
        }

        @media (max-width: 380px) {
            body { padding: 25px 10px; }
            .social-icons { gap: 16px 8px; }
            .social-item { width: 65px; }
            .social-icon { width: 55px; height: 55px; }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>

<body>
    <main class="page">

        <img
            src="/static/logo.png"
            alt="MD Rifat Sheikh Logo"
            class="animated-logo"
        >

        <h1>MD Rifat Sheikh</h1>
        <p class="subtitle">Welcome to My Official Website ✨</p>

        <div class="clock-card">
            <div class="clock-title">🕒 BANGLADESH TIME</div>
            <div id="live-clock">00:00:00</div>
            <div id="live-date">তারিখ লোড হচ্ছে...</div>
            <div class="time-zone">UTC +06:00 · DHAKA, BANGLADESH</div>
        </div>

        <button
            class="welcome-button"
            onclick="alert('আমার ওয়েবসাইটে স্বাগতম! ❤️')"
        >
            ✨ এখানে চাপ দাও
        </button>

        <section class="social-section">
            <h2>Connect With Me 🌐</h2>

            <div class="social-icons">

                <div class="social-item">
                    <a
                        class="social-icon facebook"
                        href="https://www.facebook.com/share/1FwFV17jmB/"
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label="Facebook"
                    >f</a>
                    <div class="social-label">Facebook</div>
                </div>

                <div class="social-item">
                    <a
                        class="social-icon instagram"
                        href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label="Instagram"
                    >◎</a>
                    <div class="social-label">Instagram</div>
                </div>

                <div class="social-item">
                    <a
                        class="social-icon youtube"
                        href="#"
                        aria-label="YouTube"
                    >▶</a>
                    <div class="social-label">YouTube</div>
                </div>

                <div class="social-item">
                    <a
                        class="social-icon tiktok"
                        href="#"
                        aria-label="TikTok"
                    >♪</a>
                    <div class="social-label">TikTok</div>
                </div>

                <div class="social-item">
                    <a
                        class="social-icon whatsapp"
                        href="#"
                        aria-label="WhatsApp"
                    >✆</a>
                    <div class="social-label">WhatsApp</div>
                </div>

            </div>
        </section>

        <footer class="footer">
            <p>Made with ❤️ by MD Rifat Sheikh</p>
            <p>© <span id="year"></span> All Rights Reserved</p>
        </footer>

    </main>

    <script>
        function updateClock() {
            const now = new Date();

            const time = new Intl.DateTimeFormat('en-GB', {
                timeZone: 'Asia/Dhaka',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }).format(now);

            const date = new Intl.DateTimeFormat('bn-BD', {
                timeZone: 'Asia/Dhaka',
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(now);

            document.getElementById('live-clock').textContent = time;
            document.getElementById('live-date').textContent = date;

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
