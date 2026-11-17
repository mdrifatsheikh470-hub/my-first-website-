
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
        <title>Rifat's Website</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                background: linear-gradient(
                    -45deg, #050816, #101827, #171044, #062b49
                );
                background-size: 400% 400%;
                animation: spaceBackground 14s ease infinite;
                color: white;
                text-align: center;
                padding: 40px 12px;
                font-family: Arial, sans-serif;
                margin: 0;
                min-height: 100vh;
                overflow-x: hidden;
                position: relative;
                isolation: isolate;
            }

            body::before {
                content: "";
                position: fixed;
                inset: 0;
                z-index: -1;
                pointer-events: none;
                background-image:
                    radial-gradient(2px 2px at 20% 30%, white 70%, transparent),
                    radial-gradient(2px 2px at 70% 60%, #38bdf8 70%, transparent),
                    radial-gradient(1px 1px at 40% 80%, white 70%, transparent),
                    radial-gradient(2px 2px at 85% 20%, #a78bfa 70%, transparent),
                    radial-gradient(1px 1px at 10% 70%, white 70%, transparent);
                background-size: 250px 250px;
                animation: starMove 18s linear infinite;
                opacity: 0.75;
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
                width: 220px;
                max-width: 85%;
                height: auto;
                margin-bottom: 15px;
                animation: floatLogo 3s ease-in-out infinite,
                           glowLogo 2s ease-in-out infinite alternate;
            }

            @keyframes floatLogo {
                0%, 100% { transform: translateY(0) scale(1); }
                50% { transform: translateY(-12px) scale(1.04); }
            }

            @keyframes glowLogo {
                from { filter: drop-shadow(0 0 5px #0284c7); }
                to { filter: drop-shadow(0 0 22px #38bdf8); }
            }

            h1 {
                color: #38bdf8;
            }

            .social-section {
                margin: 35px auto 20px;
            }

            .social-section h2 {
                font-size: 22px;
                margin-bottom: 20px;
                color: #e0f2fe;
            }

            .social-icons {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 16px;
                max-width: 420px;
                margin: 0 auto;
            }

            .social-icon {
                width: 62px;
                height: 62px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 18px;
                color: white;
                font-size: 30px;
                font-weight: bold;
                text-decoration: none;
                border: 1px solid rgba(255,255,255,0.18);
                box-shadow: 0 5px 18px rgba(0,0,0,0.25);
                transition: transform 0.25s, box-shadow 0.25s;
            }

            .social-icon:hover {
                transform: translateY(-7px) scale(1.08);
                box-shadow: 0 0 22px currentColor;
            }

            .facebook { background: #1877F2; }
            .instagram {
                background: linear-gradient(45deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
            }
            .youtube { background: #ff0033; }
            .tiktok { background: #111111; }
            .whatsapp { background: #128C7E; }

            .social-label {
                font-size: 12px;
                margin-top: 7px;
                color: #dbeafe;
            }

            .social-item {
                width: 76px;
            }

            .welcome-button {
                padding: 12px 20px;
                border: 0;
                border-radius: 8px;
                background: #38bdf8;
                color: #07111f;
                font-weight: bold;
                cursor: pointer;
            }

            .welcome-button:hover {
                box-shadow: 0 0 18px #38bdf8;
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
        <img src="/static/logo.png"
             alt="Rifat's Website Logo"
             class="animated-logo">

        <h1>MD Rifat Sheikh</h1>
        <p>এটি আমার ব্যক্তিগত ওয়েবসাইট।</p>
        <p>আমার ওয়েবসাইটে তোমাকে স্বাগতম!</p>

        <button class="welcome-button"
                onclick="alert('ওয়েবসাইট কাজ করছে!')">
            এখানে চাপ দাও
        </button>

        <section class="social-section">
            <h2>Connect With Me</h2>

            <div class="social-icons">

                <div class="social-item">
                    <a class="social-icon facebook"
                       href="https://www.facebook.com/share/1FwFV17jmB/"
                       target="_blank"
                       rel="noopener noreferrer"
                       aria-label="Facebook">f</a>
                    <div class="social-label">Facebook</div>
                </div>

                <div class="social-item">
                    <a class="social-icon instagram"
                       href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
                       target="_blank"
                       rel="noopener noreferrer"
                       aria-label="Instagram">◎</a>
                    <div class="social-label">Instagram</div>
                </div>

                <div class="social-item">
                    <a class="social-icon youtube"
                       href="#"
                       aria-label="YouTube">▶</a>
                    <div class="social-label">YouTube</div>
                </div>

                <div class="social-item">
                    <a class="social-icon tiktok"
                       href="#"
                       aria-label="TikTok">♪</a>
                    <div class="social-label">TikTok</div>
                </div>

                <div class="social-item">
                    <a class="social-icon whatsapp"
                       href="#"
                       aria-label="WhatsApp">✆</a>
                    <div class="social-label">WhatsApp</div>
                </div>

            </div>
        </section>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
