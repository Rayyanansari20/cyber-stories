from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage (demo only)
stories = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/stories', methods=["GET", "POST"])
def story_page():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            stories.append({"title": title, "content": content})
        return redirect(url_for("story_page"))
    return render_template("stories.html", stories=stories)

@app.route('/checker', methods=["GET", "POST"])
def checker():
    result = None
    if request.method == "POST":
        user_input = request.form.get("input_text")
        if "@" in user_input and not user_input.endswith(".com"):
            result = "⚠️ Suspicious email format"
        elif "http" in user_input and "login" in user_input.lower():
            result = "⚠️ Possible phishing link"
        else:
            result = "✅ Looks safe (but always double-check)"
    return render_template("checker.html", result=result)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
