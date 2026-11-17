
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
    </head>

    <body style="
        background:#101827;
        color:white;
        text-align:center;
        padding:40px 10px;
        font-family:sans-serif;
        margin:0;
    ">

        <img src="/static/logo.png"
             alt="Rifat's Website Logo"
             style="width:220px;max-width:85%;height:auto;margin-bottom:20px;">

        <h1 style="color:#38bdf8">MD Rifat Sheikh</h1>

        <p>এটি আমার ব্যক্তিগত ওয়েবসাইট।</p>
        <p>আমার ওয়েবসাইটে তোমাকে স্বাগতম!</p>

        <button onclick="alert('ওয়েবসাইট কাজ করছে!')"
            style="padding:12px 20px;border:0;border-radius:8px;cursor:pointer;">
            এখানে চাপ দাও
        </button>

        <p>
            <a href="https://www.facebook.com/share/1FwFV17jmB/"
               target="_blank"
               rel="noopener noreferrer"
               style="display:inline-block;background:#1877F2;color:white;padding:14px 24px;border-radius:10px;text-decoration:none;margin:8px">
                Visit My Facebook
            </a>
        </p>

        <p>
            <a href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
               target="_blank"
               rel="noopener noreferrer"
               style="display:inline-block;background:#dc2743;color:white;padding:14px 24px;border-radius:10px;text-decoration:none;margin:8px">
                Visit My Instagram
            </a>
        </p>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
