
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
            body {
                background: #101827;
                color: white;
                text-align: center;
                padding: 40px 10px;
                font-family: sans-serif;
                margin: 0;
            }

            .animated-logo {
                width: 220px;
                max-width: 85%;
                height: auto;
                margin-bottom: 20px;
                animation: floatLogo 3s ease-in-out infinite,
                           glowLogo 2s ease-in-out infinite alternate;
            }

            @keyframes floatLogo {
                0%, 100% {
                    transform: translateY(0) scale(1);
                }
                50% {
                    transform: translateY(-12px) scale(1.04);
                }
            }

            @keyframes glowLogo {
                from {
                    filter: drop-shadow(0 0 5px #0284c7);
                }
                to {
                    filter: drop-shadow(0 0 22px #38bdf8);
                }
            }

            h1 {
                color: #38bdf8;
            }

            button {
                padding: 12px 20px;
                border: 0;
                border-radius: 8px;
                cursor: pointer;
            }

            .social-link {
                display: inline-block;
                color: white;
                padding: 14px 24px;
                border-radius: 10px;
                text-decoration: none;
                margin: 8px;
            }

            .facebook {
                background: #1877F2;
            }

            .instagram {
                background: #dc2743;
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

        <button onclick="alert('ওয়েবসাইট কাজ করছে!')">
            এখানে চাপ দাও
        </button>

        <p>
            <a class="social-link facebook"
               href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank"
               rel="noopener noreferrer">
                Visit My Facebook
            </a>
        </p>

        <p>
            <a class="social-link instagram"
               href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank"
               rel="noopener noreferrer">
                Visit My Instagram
            </a>
        </p>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
