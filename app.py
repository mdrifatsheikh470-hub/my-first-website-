
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
    background: linear-gradient(
        -45deg,
        #050816,
        #101827,
        #171044,
        #062b49
    );
    background-size: 400% 400%;
    animation: spaceBackground 14s ease infinite;
    color: white;
    text-align: center;
    padding: 40px 10px;
    font-family: sans-serif;
    margin: 0;
    min-height: 100vh;
    box-sizing: border-box;
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
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes starMove {
    from { transform: translateY(0); }
    to   { transform: translateY(-250px); }
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
    
