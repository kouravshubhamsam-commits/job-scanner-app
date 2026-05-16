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

        /* Custom dropdown arrow for select elements */
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

        /* Floating Autocomplete Box */
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
            <p>Validated Precision Engine for Tech Ecosystems</p>
        </header>

        <div class="search-glass">
            <form method="GET" action="/">
                <!-- Auto-suggest Skills Input -->
                <div class="input-group">
                    <label>What Skills?</label>
                    <div class="input-wrapper">
                        <i class="fa-solid fa-code"></i>
                        <input type="text" id="skill-input" name="skills" value="{{ skills }}" placeholder="Type skills (e.g. Selenium, QA)" autocomplete="off">
                    </div>
                    <div id="suggestions" class="suggestions-box"></div>
                </div>

                <!-- Validated Location Dropdown Menu -->
                <div class="input-group">
                    <label>Valid Locations Only</label>
                    <div class="input-wrapper select-wrapper">
                        <i class="fa-solid fa-location-dot"></i>
                        <select name="location">
                            <option value="India" {% if location == 'India' %}selected{% endif %}>All India</option>
                            <option value="Bengaluru" {% if location == 'Bengaluru' %}selected{% endif %}>Bengaluru / Bangalore</option>
                            <option value="Hyderabad" {% if location == 'Hyderabad' %}selected{% endif %}>Hyderabad</option>
                            <option value="Pune" {% if location == 'Pune' %}selected{% endif %}>Pune</option>
                            <option value="Mumbai" {% if location == 'Mumbai' %}selected{% endif %}>Mumbai</option>
                            <option value="Chennai" {% if location == 'Chennai' %}selected{% endif %}>Chennai</option>
                            <option value="Delhi" {% if location == 'Delhi' %}selected{% endif %}>Delhi NCR</option>
                            <option value="Remote" {% if location == 'Remote' %}selected{% endif %}>Remote (Global/India)</option>
                        </select>
                    </div>
                </div>

                <!-- Experience Filter Dropdown -->
                <div class="input-group">
                    <label>Experience Tier</label>
                    <div class="input-wrapper select-wrapper">
                        <i class="fa-solid fa-briefcase"></i>
                        <select name="experience">
                            <option value="all" {% if experience == 'all' %}selected{% endif %}>Any Experience</option>
                            <option value="entry" {% if experience == 'entry' %}selected{% endif %}>Entry Level / Junior</option>
                            <option value="mid" {% if experience == 'mid' %}selected{% endif %}>Mid-Level Professional</option>
                            <option value="senior" {% if experience == 'senior' %}selected{% endif %}>Senior / Lead / Architect</option>
                        </select>
                    </div>
                </div>

                <button type="submit"><i class="fa-solid fa-satellite-dish"></i> Scan</button>
            </form>
        </div>

        <div class="results-grid">
            {% if jobs %}
                {% for job in jobs %}
                    <div class="job-card">
                        <div class="job-info">
                            <h3>{{ job.title }}</h3>
                            <div class="job-tags">
                                <span><i class="fa-solid fa-building" style="color: #f43f5e;"></i> {{ job.company }}</span>
                                <span><i class="fa-solid fa-map-pin" style="color: #10b981;"></i> {{ job.location }}</span>
                                <span><i class="fa-solid fa-layer-group" style="color: #3b82f6;"></i> Match Tier: {{ experience|capitalize }}</span>
                            </div>
                        </div>
                        <a href="{{ job.url }}" target="_blank" class="apply-btn">View Listing <i class="fa-solid fa-chevron-right" style="font-size: 0.8rem; margin-left: 4px;"></i></a>
                    </div>
                {% endfor %}
            {% else %}
                <div class="status-box">
                    {% if has_searched %}
                        <i class="fa-regular fa-face-frown fa-3x" style="margin-bottom: 15px; color: #64748b;"></i>
                        <p>No listings matched your criteria on this cluster. Try clearing or broadening your search terms.</p>
                    {% else %}
                        <i class="fa-solid fa-wand-magic-sparkles fa-3x" style="margin-bottom: 15px; color: var(--accent-glow);"></i>
                        <p>Use the smart dropdown configurations above to initiate an optimized scan query.</p>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Frontend Autocomplete Engineering Hook -->
    <script>
        const validSkills = [
            "Selenium", "QA Automation", "Automation Engineer", "Software Testing",
            "Playwright", "Python", "Java", "JavaScript", "Cucumber", "TestNG",
            "API Testing", "Postman", "Cypress", "Manual Testing", "DevOps",
            "React", "Node.js", "SQL", "Jenkins", "Git", "Machine Learning"
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

        // Hide floating dropdown if clicked elsewhere
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
            # Routing queries using specific geo endpoints inside Adzuna core network parameters
            api_url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=c0827255&app_key=28b5b7ec6ec593e433db0cb005691077&what={skills}&where={location}&content-type=application/json"
            
            response = requests.get(api_url, timeout=12)
            if response.status_code == 200:
                raw_results = response.json().get('results', [])
                for item in raw_results:
                    title = item.get('title', 'Engineering Role').replace('<strong>', '').replace('</strong>', '')
                    title_lower = title.lower()
                    
                    # Experience Filtration Logic Mapping
                    skip_record = False
                    if experience == 'senior' and not any(x in title_lower for x in ['senior', 'sr', 'lead', 'architect', 'manager', 'principal']):
                        skip_record = True
                    elif experience == 'entry' and any(x in title_lower for x in ['senior', 'sr', 'lead', 'lead', 'architect', 'principal']):
                        skip_record = True
                        
                    if not skip_record:
                        jobs_matched.append({
                            "title": title,
                            "company": item.get('company', {}).get('display_name', 'Tech Enterprise'),
                            "location": item.get('location', {}).get('display_name', location),
                            "url": item.get('redirect_url')
                        })
        except Exception as e:
            print(f"Extraction Pipeline Failure: {e}")

    return render_template_string(
        HTML_TEMPLATE, 
        jobs=jobs_matched, 
        skills=skills, 
        location=location, 
        experience=experience, 
        has_searched=has_searched
    )
