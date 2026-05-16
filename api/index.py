from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Job Scanner</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background: #f4f6f9; color: #2d3748; margin: 0; padding: 40px 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h1 { color: #1a365d; text-align: center; margin-bottom: 30px; }
        form { display: flex; gap: 10px; margin-bottom: 30px; }
        input { flex: 1; padding: 12px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 1rem; }
        button { background: #3182ce; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #2b6cb0; }
        .job-card { padding: 20px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
        .job-card:last-child { border-bottom: none; }
        .apply-btn { background: #e2e8f0; color: #4a5568; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 0.9rem; font-weight: 600; transition: all 0.2s; }
        .apply-btn:hover { background: #3182ce; color: white; }
        .no-results { text-align: center; color: #718096; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Universal Job Scanner</h1>
        <form method="GET" action="/">
            <input type="text" name="skills" value="{{ skills }}" placeholder="Skills (e.g. QA, Selenium, Python)">
            <input type="text" name="location" value="{{ location }}" placeholder="Location (e.g. Remote, India)">
            <button type="submit">Scan Jobs</button>
        </form>
        <div>
            {% if jobs %}
                {% for job in jobs %}
                    <div class="job-card">
                        <div>
                            <h3 style="margin: 0 0 5px 0; color: #2b6cb0;">{{ job.title }}</h3>
                            <small style="color: #718096;">🏢 {{ job.company_name }} | 📍 {{ job.location }}</small>
                        </div>
                        <a href="{{ job.url }}" target="_blank" class="apply-btn">Apply ↗</a>
                    </div>
                {% endfor %}
            {% else %}
                <div class="no-results">
                    <p>Enter your search criteria above to scan live public job listings.</p>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    skills = request.args.get('skills', '')
    location = request.args.get('location', '')
    jobs_matched = []

    if skills or location:
        try:
            response = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=10)
            if response.status_code == 200:
                for job in response.json().get('data', []):
                    title = job.get('title', '').lower()
                    loc = job.get('location', '').lower()
                    desc = job.get('description', '').lower()
                    
                    match_skills = not skills or (skills.lower() in title or skills.lower() in desc)
                    match_location = not location or (location.lower() in loc)
                    
                    if match_skills and match_location:
                        jobs_matched.append({
                            "title": job.get('title'),
                            "company_name": job.get('company_name'),
                            "location": job.get('location'),
                            "url": job.get('url')
                        })
        except Exception as e:
            print(f"Extraction Error: {e}")

    return render_template_string(HTML_TEMPLATE, jobs=jobs_matched, skills=skills, location=location)
