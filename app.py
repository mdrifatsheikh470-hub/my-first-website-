from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>আমার ওয়েবসাইট</title>
    </head>
    <body style="background:#101827;color:white;text-align:center;padding:50px 10px;font-family:sans-serif">
        <h1 style="color:#38bdf8">MD Rifat Sheikh</h1>
<p>এটি আমার ব্যক্তিগত ওয়েবসাইট।</p>
<p>আমার ওয়েবসাইটে তোমাকে স্বাগতম!</p>
     
       <button onclick="alert('ওয়েবসাইট কাজ করছে!')">
            এখানে চাপ দাও
        </button>
    </body>
    </
>
<

<a href="https://www.facebook.com/share/1FwFV17jmB/"
   target="_blank"
   rel="noopener noreferrer"
   style="display:inline-block;
          background:#1877F2;
          color:white;
          padding:14px 24px;
          border-radius:10px;
          text-decoration:none;
          font-family:sans-serif;
          font-weight:bold;
          margin:8px;">
    f  Visit My Facebook
</a>

>
<

<a href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
   target="_blank"
   rel="noopener noreferrer"
   style="display:inline-block;
          background:linear-gradient(45deg,#f09433,#dc2743,#bc1888);
          color:white;
          padding:14px 24px;
          border-radius:10px;
          text-decoration:none;
          font-family:sans-serif;
          font-weight:bold;
          margin:8px;">
    📸 Visit My Instagram
</a>

>
    """

app.run(host="127.0.0.1", port=5000)
