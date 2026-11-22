import os
import re
import hmac
import secrets
import sqlite3
import smtplib

from functools import wraps
from pathlib import Path
from email.message import EmailMessage

from flask import (
    Flask, request, redirect, url_for, session,
    render_template_string, abort
)
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Set SECRET_KEY in Render Environment Variables.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# On Render, set DB_PATH=/var/data/users.db
DB_PATH = os.environ.get("DB_PATH", "users.db")

EMAIL_TO = "mdrifatsheikh470@gmail.com"


# ---------------- DATABASE ----------------

def get_db():
    path = Path(DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(str(path), timeout=15)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


init_db()


# ---------------- SECURITY ----------------

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def verify_csrf():
    supplied = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")

    if (
        not supplied
        or not expected
        or not hmac.compare_digest(supplied, expected)
    ):
        abort(400, description="Invalid form token. Please reload the page.")

    return True


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next="dashboard"))
        return view(*args, **kwargs)
    return wrapped


def page(title, content, **context):
    return render_template_string(
        BASE_TEMPLATE,
        title=title,
        content=content,
        csrf_token=csrf_token(),
        username=session.get("username"),
        **context
    )


# ---------------- SHARED DESIGN ----------------

BASE_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#080d20">
<title>{{ title }} | MD Rifat Sheikh</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    padding: 20px;
    color: #f4f7ff;
    font-family: Arial, sans-serif;
    background:
        radial-gradient(ellipse at top left, #192b59, transparent 50%),
        radial-gradient(ellipse at bottom right, #30174c, transparent 50%),
        #080d20;
}

a { color: #55eaff; }

.nav {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin: 8px auto 25px;
}

.nav a {
    text-decoration: none;
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    background: rgba(255,255,255,.08);
}

.nav a:hover { background: rgba(85,234,255,.18); }

.wrap {
    width: min(760px, 100%);
    margin: 0 auto;
}

.panel {
    padding: 28px;
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 22px;
    background: rgba(255,255,255,.07);
    box-shadow: 0 20px 65px rgba(0,0,0,.25);
    backdrop-filter: blur(12px);
    overflow-wrap: anywhere;
}

h1, h2 {
    text-align: center;
    color: #55eaff;
}

h1 { font-size: clamp(26px, 5vw, 38px); }

p { line-height: 1.7; }

form { display: grid; gap: 14px; }

label { font-size: 14px; color: #d4def4; }

input, textarea {
    width: 100%;
    padding: 14px;
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 12px;
    background: rgba(0,0,0,.22);
    color: white;
    font: inherit;
}

input:focus, textarea:focus {
    outline: 2px solid #55eaff;
    outline-offset: 1px;
}

button, .button {
    display: inline-block;
    padding: 13px 18px;
    border: 0;
    border-radius: 12px;
    color: #071323;
    background: linear-gradient(90deg, #55eaff, #a78bfa);
    font-weight: bold;
    font-size: 15px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
}

button:hover, .button:hover { filter: brightness(1.1); }

.notice {
    padding: 12px;
    border-radius: 10px;
    line-height: 1.6;
    margin: 12px 0;
}

.error {
    color: #ffc1c1;
    background: rgba(255,70,70,.12);
}

.success {
    color: #b7ffcf;
    background: rgba(40,200,100,.12);
}

.muted { color: #c2cce5; }

.center { text-align: center; }

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-top: 20px;
}

.tile {
    padding: 18px;
    border-radius: 14px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.1);
}

.hero { text-align: center; }

.logo {
    width: 125px;
    height: 125px;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid #55eaff;
    box-shadow: 0 0 25px rgba(85,234,255,.3);
}

.typing {
    min-height: 32px;
    color: #55eaff;
    font-size: 21px;
    font-weight: bold;
}

.cursor { animation: blink .7s infinite; }

@keyframes blink { 50% { opacity: 0; } }

footer {
    margin: 28px 0 10px;
    text-align: center;
    font-size: 13px;
    color: #c2cce5;
}

@media (max-width: 480px) {
    body { padding: 12px; }
    .panel { padding: 20px 15px; }
    .nav { gap: 8px; }
    .nav a { padding: 9px 10px; font-size: 13px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
    }
}
</style>
</head>

<body>
<nav class="nav">
    <a href="{{ url_for('home') }}">Home</a>

    {% if username %}
        <a href="{{ url_for('dashboard') }}">Dashboard</a>
        <a href="{{ url_for('logout') }}">Logout</a>
    {% else %}
        <a href="{{ url_for('login') }}">Login</a>
        <a href="{{ url_for('signup') }}">Sign Up</a>
    {% endif %}
</nav>

<main class="wrap">
    <section class="panel">
        {{ content | safe }}
    </section>
</main>

<footer>© 2026 MD Rifat Sheikh · Bangladesh 🇧🇩</footer>
</body>
</html>
"""


# ---------------- HOME PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def home():
    status = ""

    if request.method == "POST":
        verify_csrf()

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if (
            not name or not email or not message
            or len(name) > 100
            or len(email) > 254
            or len(message) > 5000
            or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
        ):
            status = '<div class="notice error">Please check your form details.</div>'
        else:
            mail_user = os.environ.get("MAIL_USERNAME")
            mail_pass = os.environ.get("MAIL_PASSWORD")

            if not mail_user or not mail_pass:
                status = '<div class="notice error">Email service is not configured yet.</div>'
            else:
                try:
                    mail = EmailMessage()
                    mail["Subject"] = f"Website message from {name}"
                    mail["From"] = mail_user
                    mail["To"] = EMAIL_TO
                    mail["Reply-To"] = email
                    mail.set_content(
                        f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                    )

                    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
                        server.starttls()
                        server.login(mail_user, mail_pass)
                        server.send_message(mail)

                    status = '<div class="notice success">Message sent successfully!</div>'
                except Exception:
                    app.logger.exception("Contact email failed")
                    status = '<div class="notice error">Message could not be sent. Please try later.</div>'

    content = """
    <div class="hero">
        <img class="logo" src="/static/logo.png" alt="MD Rifat Sheikh"
             onerror="this.style.display='none'">

        <h1>MD Rifat Sheikh</h1>
        <p class="typing"><span id="typed">Content Creator</span><span class="cursor"> |</span></p>
        <p class="muted" id="welcome">Welcome to my official website ✨</p>

        <div class="tile">
            <p class="muted" id="clock-label">Bangladesh current time</p>
            <h2 id="clock">--:--:--</h2>
            <p id="date"></p>
        </div>
    </div>

    <h2>🌐 My Social Media</h2>
    <div class="grid">
        <a class="button" href="https://www.facebook.com/share/1FwFV17jmB/"
           target="_blank" rel="noopener noreferrer">Facebook</a>

        <a class="button" href="https://www.instagram.com/happy2538832?vrfl=MWg0YzRsd3lzZ3Fibw=="
           target="_blank" rel="noopener noreferrer">Instagram</a>

        <a class="button" href="https://www.youtube.com/"
           target="_blank" rel="noopener noreferrer">YouTube</a>

        <a class="button" href="https://www.tiktok.com/"
           target="_blank" rel="noopener noreferrer">TikTok</a>

        <a class="button" href="https://www.whatsapp.com/"
           target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </div>

    <h2>📩 Contact Me</h2>
    """ + status + """
    <form method="POST" action="/">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

        <label for="contact-name">Your name</label>
        <input id="contact-name" name="name" maxlength="100" required>

        <label for="contact-email">Your email</label>
        <input id="contact-email" name="email" type="email" maxlength="254" required>

        <label for="contact-message">Your message</label>
        <textarea id="contact-message" name="message" maxlength="5000"
                  rows="5" required></textarea>

        <button type="submit">Send Message ✉️</button>
    </form>

    <p class="center muted">Create an account to access your personal dashboard.</p>

    <p class="center">
        <a class="button" href="/signup">Create Account</a>
        <a class="button" href="/login">Login</a>
    </p>

    <script>
    const words = [
        "Content Creator",
        "Welcome to My Website",
        "Dream Big, Work Hard",
        "MD Rifat Sheikh"
    ];
    let wi = 0, ci = 0, deleting = false;

    function typeLoop() {
        const el = document.getElementById("typed");
        if (!el) return;

        const word = words[wi];
        el.textContent = word.substring(0, ci);

        let delay = deleting ? 45 : 90;

        if (!deleting && ci < word.length) {
            ci++;
        } else if (!deleting) {
            deleting = true;
            delay = 1400;
        } else if (ci > 0) {
            ci--;
        } else {
            deleting = false;
            wi = (wi + 1) % words.length;
        }

        setTimeout(typeLoop, delay);
    }
    typeLoop();

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

        document.getElementById("date").textContent =
            new Intl.DateTimeFormat("en-GB", {
                timeZone: "Asia/Dhaka",
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric"
            }).format(now);
    }

    updateClock();
    setInterval(updateClock, 1000);
    </script>
    """

    return page("Home", content)


# ---------------- SIGN UP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = ""

    if request.method == "POST":
        verify_csrf()

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username):
            error = "Username must be 3–30 characters: letters, numbers, or underscore."
        elif len(password) < 10 or len(password) > 128:
            error = "Password must be 10–128 characters long."
        elif password != confirm:
            error = "Passwords do not match."
        else:
            password_hash = generate_password_hash(password, method="scrypt")

            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, password_hash)
                    )

                return redirect(url_for("login", created="1"))

            except sqlite3.IntegrityError:
                error = "That username is already taken. Choose another."

            except Exception:
                app.logger.exception("Account creation failed")
                error = "Account could not be created. Please try again."

    content = """
    <h1>Create Account</h1>
    <p class="center muted">Join MD Rifat Sheikh's website.</p>
    """ + (f'<div class="notice error">{error}</div>' if error else "") + """
    <form method="POST" action="/signup">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

        <label for="username">Username</label>
        <input id="username" name="username" autocomplete="username"
               minlength="3" maxlength="30"
               pattern="[A-Za-z0-9_]{3,30}"
               title="Use 3–30 letters, numbers, or underscores."
               required>

        <label for="password">Password (at least 10 characters)</label>
        <input id="password" name="password" type="password"
               autocomplete="new-password" minlength="10"
               maxlength="128" required>

        <label for="confirm_password">Confirm password</label>
        <input id="confirm_password" name="confirm_password"
               type="password" autocomplete="new-password"
               minlength="10" maxlength="128" required>

        <button type="submit">Sign Up</button>
    </form>

    <p class="center">Already registered? <a href="/login">Login</a></p>
    """

    return page("Sign Up", content)


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = ""
    success = (
        '<div class="notice success">Account created. You can log in now.</div>'
        if request.args.get("created") == "1" else ""
    )

    if request.method == "POST":
        verify_csrf()

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        try:
            with get_db() as db:
                user = db.execute(
                    "SELECT id, username, password_hash FROM users "
                    "WHERE username = ? COLLATE NOCASE",
                    (username,)
                ).fetchone()

            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["csrf_token"] = secrets.token_urlsafe(32)

                return redirect(url_for("dashboard"))

            error = "Incorrect username or password."

        except Exception:
            app.logger.exception("Login failed")
            error = "Login is temporarily unavailable. Please try again."

    content = """
    <h1>Login</h1>
    <p class="center muted">Sign in with your username and password.</p>
    """ + success + (f'<div class="notice error">{error}</div>' if error else "") + """
    <form method="POST" action="/login">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

        <label for="username">Username</label>
        <input id="username" name="username" autocomplete="username"
               maxlength="30" required>

        <label for="password">Password</label>
        <input id="password" name="password" type="password"
               autocomplete="current-password"
               maxlength="128" required>

        <button type="submit">Login 🔐</button>
    </form>

    <p class="center">Don't have an account? <a href="/signup">Sign Up</a></p>
    """

    return page("Login", content)


# ---------------- PRIVATE DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():
    # Always retrieve the account from the database.
    with get_db() as db:
        user = db.execute(
            "SELECT username, created_at FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

    if user is None:
        session.clear()
        return redirect(url_for("login"))

    content = """
    <h1>Welcome, {{ account.username }}! 🎉</h1>
    <p class="center muted">You are successfully logged in.</p>

    <div class="grid">
        <div class="tile">
            <h2>👤 Account</h2>
            <p>Username: <strong>{{ account.username }}</strong></p>
        </div>

        <div class="tile">
            <h2>🔐 Security</h2>
            <p>Your password is stored as a secure hash, not as plain text.</p>
        </div>
    </div>

    <p class="center" style="margin-top:25px">
        <a class="button" href="/">Visit Home Page</a>
    </p>

    <form method="POST" action="/logout" style="margin-top:20px">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
        <button type="submit">Logout</button>
    </form>
    """

    return page("Dashboard", content, account=user)


# ---------------- LOGOUT ----------------

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect(url_for("login"))

        content = """
        <h1>Logout</h1>
        <p class="center">Are you sure you want to log out?</p>

        <form method="POST" action="/logout">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <button type="submit">Confirm Logout</button>
        </form>
        """
        return page("Logout", content)

    verify_csrf()
    session.clear()
    return redirect(url_for("home"))


# ---------------- ERROR HANDLERS ----------------

@app.errorhandler(400)
def bad_request(error):
    return page(
        "Request Error",
        '<h1>Request Error</h1>'
        '<p class="center">Your form expired or was invalid. '
        '<a href="/">Return home</a> and try again.</p>'
    ), 400


@app.errorhandler(404)
def not_found(error):
    return page(
        "Not Found",
        '<h1>Page Not Found</h1>'
        '<p class="center"><a href="/">Return Home</a></p>'
    ), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
    
