from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Job Scanner Pro</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-glow: #818cf8;
            --btn-gradient: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
            --dropdown-bg: #1e293b;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 2.5rem;
            margin: 0 0 10px 0;
            background: linear-gradient(90deg, #a5b4fc, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.05em;
        }

        header p {
            color: var(--text-muted);
            margin: 0;
            font-size: 1.1rem;
        }

        .search-glass {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            margin-bottom: 35px;
        }

        form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) auto;
            gap: 20px;
            align-items: end;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            position: relative;
        }

        .input-group label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-glow);
            font-weight: 700;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            z-index: 2;
        }

        input, select {
            width: 100%;
            box-sizing: border-box;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 14px 14px 14px 45px;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            appearance: none;
            height: 50px;
        }

        select {
            cursor: pointer;
            padding-right: 40px;
        }

        .select-wrapper::after {
            content: '\\f107';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--accent-glow);
            box-shadow: 0 0 15px rgba(129, 140, 248, 0.3);
        }

        .suggestions-box {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--dropdown-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            margin-top: 5px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 10;
            display: none;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .suggestion-item {
            padding: 12px 15px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .suggestion-item:hover {
            background: rgba(129, 140, 248, 0.2);
            color: white;
        }

        button {
            background: var(--btn-gradient);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            height: 50px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
        }

        .counter-badge {
            background: rgba(129, 140, 248, 0.15);
            border: 1px solid var(--accent-glow);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }

        .job-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }

        .job-card:hover {
            transform: scale(1.01);
            border-color: rgba(129, 140, 248, 0.4);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .job-info h3 {
            margin: 0 0 10px 0;
            color: #ffffff;
            font-size: 1.3rem;
        }

        .job-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        .job-tags span {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .apply-btn {
            background: rgba(255, 255, 255, 0.05);
            color: #e2e8f0;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .apply-btn:hover {
            background: white;
            color: #0f172a;
        }

        .status-box {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fa-solid fa-bolt" style="color: var(--accent-glow);"></i> JobScanner Pro</h1>
            <p>Direct Aggregation Matrix Engine</p>
        </header>

        <div class="search-glass">
            <form method="GET" action="/">
                <div class="input-group">
                    <label>What Skills?</label>
                    <div class="input-wrapper">
                        <i class="fa-solid fa-code"></i>
                        <input type="text" id="skill-input" name="skills" value="{{ skills }}" placeholder="Type skills (e.g. Selenium, QA)" autocomplete="off">
                    </div>
                    <div id="suggestions" class="suggestions-box"></div>
                </div>

                <div class="input-group">
                    <label>Valid Locations Only</label>
                    <div class="input-wrapper select-wrapper">
                        <i class="fa-solid fa-location-dot"></i>
                        <select name="location">
                            <option value="India" {% if location == 'India' %}selected{% endif %}>All India</option>
                            <option value="Bengaluru" {% if location == 'Bengaluru' %}selected{% endif %}>Bengaluru</option>
                            <option value="Hyderabad" {% if location == 'Hyderabad' %}selected{% endif %}>Hyderabad</option>
                            <option value="Pune" {% if location == 'Pune' %}selected{% endif %}>Pune</option>
                            <option value="Remote" {% if location == 'Remote' %}selected{% endif %}>Remote</option>
                        </select>
                    </div>
                </div>

                <div class="input-group">
                    <label>Experience Tier</label>
                    <div class="input-wrapper select-wrapper">
                        <i class="fa-solid fa-briefcase"></i>
                        <select name="experience">
                            <option value="all" {% if experience == 'all' %}selected{% endif %}>Any Experience</option>
                            <option value="entry" {% if experience == 'entry' %}selected{% endif %}>Entry Level / Junior</option>
                            <option value="senior" {% if experience == 'senior' %}selected{% endif %}>Senior / Lead Track</option>
                        </select>
                    </div>
                </div>

                <button type="submit"><i class="fa-solid fa-satellite-dish"></i> Scan</button>
            </form>
        </div>

        <div class="results-grid">
            {% if jobs %}
                <div class="counter-badge">
                    <i class="fa-solid fa-circle-check" style="color: #10b981;"></i>
                    <span>Found <b>{{ jobs|length }}</b> Active Verification Listings</span>
                </div>
                {% for job in jobs %}
                    <div class="job-card">
                        <div class="job-info">
                            <h3>{{ job.title }}</h3>
                            <div class="job-tags">
                                <span><i class="fa-solid fa-building" style="color: #f43f5e;"></i> {{ job.company }}</span>
                                <span><i class="fa-solid fa-map-pin" style="color: #10b981;"></i> {{ job.location }}</span>
                            </div>
                        </div>
                        <a href="{{ job.url }}" target="_blank" class="apply-btn">View Listing <i class="fa-solid fa-chevron-right" style="font-size: 0.8rem; margin-left: 4px;"></i></a>
                    </div>
                {% endfor %}
            {% else %}
                <div class="status-box">
                    {% if has_searched %}
                        <i class="fa-regular fa-face-frown fa-3x" style="margin-bottom: 15px; color: #64748b;"></i>
                        <p>No listings matched your criteria on this cluster. Try shifting parameters or locations.</p>
                    {% else %}
                        <i class="fa-solid fa-wand-magic-sparkles fa-3x" style="margin-bottom: 15px; color: var(--accent-glow);"></i>
                        <p>Select your target stack parameters above to execute a real-time cluster scan.</p>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    </div>

    <script>
        const validSkills = [
            "Selenium", "QA Automation", "Automation Engineer", "Software Testing",
            "Playwright", "Python", "Java", "JavaScript", "API Testing", "Manual Testing"
        ];

        const skillInput = document.getElementById('skill-input');
        const suggestionsBox = document.getElementById('suggestions');

        skillInput.addEventListener('input', () => {
            const val = skillInput.value.toLowerCase();
            suggestionsBox.innerHTML = '';
            if (!val) {
                suggestionsBox.style.display = 'none';
                return;
            }

            const matches = validSkills.filter(skill => skill.toLowerCase().includes(val));
            if (matches.length === 0) {
                suggestionsBox.style.display = 'none';
                return;
            }

            matches.forEach(match => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = match;
                div.addEventListener('click', () => {
                    skillInput.value = match;
                    suggestionsBox.style.display = 'none';
                });
                suggestionsBox.appendChild(div);
            });
            suggestionsBox.style.display = 'block';
        });

        document.addEventListener('click', (e) => {
            if (e.target !== skillInput) suggestionsBox.style.display = 'none';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    skills = request.args.get('skills', '')
    location = request.args.get('location', 'India')
    experience = request.args.get('experience', 'all')
    
    jobs_matched = []
    has_searched = False

    if skills:
        has_searched = True
        try:
            # Swapping to a direct open job engine cluster feed
            api_url = f"https://www.juju.com/api/v1/jobs?k={skills}&l={location}&c=25&f=json"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                raw_data = response.json().get('jobs', [])
                for item in raw_data:
                    title = item.get('title', 'Automation Developer')
                    title_lower = title.lower()
                    
                    # Core Experience Filters
                    skip_record = False
                    if experience == 'senior' and not any(x in title_lower for x in ['senior', 'sr', 'lead', 'architect', 'manager', 'principal']):
                        skip_record = True
                    elif experience == 'entry' and any(x in title_lower for x in ['senior', 'sr', 'lead', 'architect', 'principal']):
                        skip_record = True
                        
                    if not skip_record:
                        jobs_matched.append({
                            "title": title,
                            "company": item.get('company', 'Tech Enterprise Corp'),
                            "location": item.get('location', location),
                            "url": item.get('url')
                        })
        except Exception as e:
            print(f"Extraction Error: {e}")

    return render_template_string(
        HTML_TEMPLATE, 
        jobs=jobs_matched, 
        skills=skills, 
        location=location, 
        experience=experience, 
        has_searched=has_searched
    )
