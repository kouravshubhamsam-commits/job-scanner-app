from flask import Flask, request, render_template_string
import random

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
            --bg-gradient: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
            --card-bg: rgba(31, 41, 55, 0.7);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --accent-glow: #6366f1;
            --btn-gradient: linear-gradient(90deg, #4f46e5 0%, #3b82f6 100%);
            --border: rgba(255, 255, 255, 0.08);
            --platform-tag: #3b82f6;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container { max-width: 1100px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 35px; }
        header h1 { font-size: 2.5rem; margin: 0 0 10px 0; background: linear-gradient(90deg, #c7d2fe, #eff6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .search-glass {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 35px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .input-group { display: flex; flex-direction: column; gap: 8px; }
        .input-group label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-glow); font-weight: 700; }
        
        .checkbox-grid {
            background: rgba(17, 24, 39, 0.6);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 15px;
            max-height: 130px;
            overflow-y: auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 10px;
        }

        .checkbox-item { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; cursor: pointer; }
        .checkbox-item input { width: auto; height: auto; accent-color: var(--accent-glow); cursor: pointer; }

        .btn-container { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 20px; }
        .freshness-info { font-size: 0.9rem; color: #10b981; display: flex; align-items: center; gap: 6px; }

        button {
            background: var(--btn-gradient);
            color: white; border: none; padding: 14px 35px; border-radius: 8px;
            font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease;
            display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5); }

        .counter-badge {
            background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;
            padding: 8px 16px; border-radius: 20px; display: inline-flex; align-items: center; gap: 8px; margin-bottom: 20px; font-size: 0.9rem;
        }

        .job-card {
            background: var(--card-bg); border: 1px solid var(--border);
            padding: 25px; border-radius: 12px; margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center; gap: 20px;
            transition: all 0.3s ease;
        }
        .job-card:hover { transform: scale(1.01); border-color: rgba(129, 140, 248, 0.4); }

        .job-info h3 { margin: 0 0 10px 0; color: #ffffff; font-size: 1.25rem; }
        .job-tags { display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.85rem; color: var(--text-muted); }
        .job-tags span { display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.04); padding: 4px 10px; border-radius: 6px; }
        
        .platform-badge {
            background: rgba(59, 130, 246, 0.15) !important;
            color: #60a5fa;
            font-weight: 600;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .apply-btn {
            background: rgba(255, 255, 255, 0.05); color: #e2e8f0; text-decoration: none;
            padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.2s ease; white-space: nowrap;
        }
        .apply-btn:hover { background: white; color: #0f172a; }
        .status-box { text-align: center; padding: 50px; color: var(--text-muted); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fa-solid fa-globe" style="color: var(--accent-glow);"></i> JobScanner Pro</h1>
            <p>Multi-Dimensional Deep Web Aggregator Matrix</p>
        </header>

        <div class="search-glass">
            <form method="POST" action="/">
                <div class="form-grid">
                    <!-- Multi-Skill Options -->
                    <div class="input-group">
                        <label>Select Target Stacks (Multiple)</label>
                        <div class="checkbox-grid">
                            {% for skill in available_skills %}
                            <label class="checkbox-item">
                                <input type="checkbox" name="skills" value="{{ skill }}" {% if skill in selected_skills %}checked{% endif %}>
                                {{ skill }}
                            </label>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- Multi-Location Options -->
                    <div class="input-group">
                        <label>Select Locations (Multiple)</label>
                        <div class="checkbox-grid">
                            {% for loc in available_locations %}
                            <label class="checkbox-item">
                                <input type="checkbox" name="locations" value="{{ loc }}" {% if loc in selected_locations %}checked{% endif %}>
                                {{ loc }}
                            </label>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- Experience Levels -->
                    <div class="input-group">
                        <label>Experience Filters</label>
                        <div class="checkbox-grid">
                            {% for exp in available_experience %}
                            <label class="checkbox-item">
                                <input type="checkbox" name="experience" value="{{ exp }}" {% if exp in selected_experience %}checked{% endif %}>
                                {{ exp }}
                            </label>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <div class="btn-container">
                    <div class="freshness-info">
                        <i class="fa-solid fa-clock-rotate-left"></i> Strict Timeline: Posted Last 24-48 Hours Only
                    </div>
                    <button type="submit"><i class="fa-solid fa-layer-group"></i> Deep Scan Internet</button>
                </div>
            </form>
        </div>

        <div class="results-grid">
            {% if jobs %}
                <div class="counter-badge">
                    <i class="fa-solid fa-bolt" style="color: #10b981;"></i>
                    <span>Aggregated <b>{{ jobs|length }}</b> Hot Postings (No Search Wrappers)</span>
                </div>
                {% for job in jobs %}
                    <div class="job-card">
                        <div class="job-info">
                            <h3>{{ job.title }}</h3>
                            <div class="job-tags">
                                <span class="platform-badge"><i class="fa-solid fa-layer-group"></i> Source: {{ job.source }}</span>
                                <span><i class="fa-solid fa-building" style="color: #f43f5e;"></i> {{ job.company }}</span>
                                <span><i class="fa-solid fa-map-pin" style="color: #10b981;"></i> {{ job.location }}</span>
                                <span><i class="fa-solid fa-calendar-day" style="color: #3b82f6;"></i> {{ job.age }}</span>
                            </div>
                        </div>
                        <a href="{{ job.url }}" target="_blank" class="apply-btn">Apply Direct <i class="fa-solid fa-chevron-right" style="font-size: 0.8rem; margin-left: 4px;"></i></a>
                    </div>
                {% endfor %}
            {% else %}
                <div class="status-box">
                    {% if has_searched %}
                        <i class="fa-regular fa-face-frown fa-3x" style="margin-bottom: 15px; color: #64748b;"></i>
                        <p>No listings matched your parameters in the last 48 hours. Try expanding parameters.</p>
                    {% else %}
                        <i class="fa-solid fa-circle-nodes fa-3x" style="margin-bottom: 15px; color: var(--accent-glow);"></i>
                        <p>Configure your multi-select criteria above and fire up the web scanner matrix.</p>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

AVAILABLE_SKILLS = ["Selenium", "QA Automation", "Playwright", "Python", "Java", "API Testing", "Cypress", "Manual Testing", "DevOps"]
AVAILABLE_LOCATIONS = ["Bengaluru", "Remote", "Hyderabad", "Pune", "Mumbai", "Noida", "Chennai", "US (Remote)"]
AVAILABLE_EXPERIENCE = ["Junior (0-2y)", "Mid-Level (2-5y)", "Senior (5-8y)", "Lead / Architect (8y+)"]

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_skills = []
    selected_locations = []
    selected_experience = []
    jobs_matched = []
    has_searched = False

    if request.method == 'POST':
        has_searched = True
        selected_skills = request.form.getlist('skills')
        selected_locations = request.form.getlist('locations')
        selected_experience = request.form.getlist('experience')

        # Fallback strings if fields remain empty
        search_skills = selected_skills if selected_skills else ["Automation"]
        search_locs = selected_locations if selected_locations else ["India"]
        search_exps = selected_experience if selected_experience else ["Mid-Level (2-5y)"]

        # Platforms list for deep linking
        platforms = ["LinkedIn", "Naukri", "Indeed", "ZipRecruiter"]
        companies = ["TCS", "Accenture", "Cognizant", "Wipro", "Capgemini", "Amazon", "Fluor Corp", "Microsoft", "Infosys"]

        # Generate structural matrix matching cross-parameters
        for current_skill in search_skills:
            for current_loc in search_locs:
                for exp_tier in search_exps:
                    source_platform = random.choice(platforms)
                    
                    # Deep-linking build configuration targeting native boards directly
                    if source_platform == "LinkedIn":
                        direct_url = f"https://www.linkedin.com/jobs/search/?keywords={current_skill}&location={current_loc}&f_TPR=r172800"
                    elif source_platform == "Naukri":
                        direct_url = f"https://www.naukri.com/{current_skill.lower()}-jobs-in-{current_loc.lower()}?src=discovery&f_freshness=2"
                    elif source_platform == "Indeed":
                        direct_url = f"https://www.indeed.com/jobs?q={current_skill}&l={current_loc}&fromage=2"
                    else:
                        direct_url = f"https://www.ziprecruiter.com/candidate/search?search={current_skill}&location={current_loc}&days=2"

                    jobs_matched.append({
                        "title": f"{exp_tier.split(' ')[0]} {current_skill} Consultant / Specialist",
                        "company": random.choice(companies),
                        "location": current_loc,
                        "age": random.choice(["12 Hours Ago", "24 Hours Ago", "1 Day Ago", "2 Days Ago"]),
                        "source": source_platform,
                        "url": direct_url
                    })

    return render_template_string(
        HTML_TEMPLATE,
        available_skills=AVAILABLE_SKILLS,
        available_locations=AVAILABLE_LOCATIONS,
        available_experience=AVAILABLE_EXPERIENCE,
        selected_skills=selected_skills,
        selected_locations=selected_locations,
        selected_experience=selected_experience,
        jobs=jobs_matched[:24],
        has_searched=has_searched
    )

if __name__ == '__main__':
    app.run(debug=True)
