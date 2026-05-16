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
          :root { --bg: #f4f6f9; --card: #ffffff; --text: #2d3748; --primary: #3182ce; }
          body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 40px 20px; }
          .container { max-width: 1000px; margin: 0 auto; }
          h1 { text-align: center; color: #1a365d; margin-bottom: 30px; }
          .search-form { background: var(--card); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) auto; gap: 15px; align-items: end; margin-bottom: 40px; }
          .form-group { display: flex; flex-direction: column; gap: 5px; }
          label { font-size: 0.85rem; font-weight: 600; color: #4a5568; text-transform: uppercase; }
          input { padding: 12px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 1rem; }
          button { background: var(--primary); color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: background 0.2s; height: 48px; }
          button:hover { background: #2b6cb0; }
          .job-card { background: var(--card); padding: 25px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; border-left: 5px solid var(--primary); display: flex; justify-content: space-between; align-items: center; }
          .job-details h2 { margin: 0 0 8px 0; font-size: 1.25rem; color: #2b6cb0; }
          .job-meta { display: flex; gap: 15px; font-size: 0.9rem; color: #718096; }
          .job-meta span { display: flex; align-items: center; gap: 5px; }
          .apply-btn { display: inline-block; background: #e2e8f0; color: #4a5568; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; transition: all 0.2s; }
          .apply-btn:hover { background: var(--primary); color: white; }
          .no-results { text-align: center; color: #718096; padding: 40px; background: white; border-radius: 10px; }
      </style>
  </head>
  <body>
      <div class="container">
          <h1><i class="fa-solid fa-satellite-dish"></i> Universal Job Scanner</h1>
          
          <form class="search-form" method="GET" action="/">
              <div class="form-group">
                  <label>Skills / Role</label>
                  <input type="text" name="skills" value="{{ skills }}" placeholder="e.g. Python, QA, React">
              </div>
              <div class="form-group">
                  <label>Location</label>
                  <input type="text" name="location" value="{{ location }}" placeholder="e.g. Remote, Berlin">
              </div>
              <button type="submit"><i class="fa-solid fa-magnifying-glass"></i> Scan Jobs</button>
          </form>

          <div class="results-container">
              {% if jobs %}
                  {% for job in jobs %}
                      <div class="job-card">
                          <div class="job-details">
                               <h2>{{ job.title }}</h2>
                               <div class="job-meta">
                                   <span><i class="fa-solid fa-building"></i> {{ job.company_name }}</span>
                                   <span><i class="fa-solid fa-location-dot"></i> {{ job.location }}</span>
                                   {% if job.remote %}
                                       <span><i class="fa-solid fa-house-laptop"></i> Remote Friendly</span>
                                   {% endif %}
                               </div>
                          </div>
                          <div>
                               <a href="{{ job.url }}" target="_blank" class="apply-btn">Apply <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
                          </div>
                      </div>
                  {% endfor %}
              {% else %}
                  <div class="no-results">
                       <i class="fa-regular fa-folder-open fa-3x" style="margin-bottom: 15px; color: #cbd5e0;"></i>
                       <p>No job listings found. Try searching for skills or location criteria above.</p>
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
              api_url = "https://www.arbeitnow.com/api/job-board-api"
              response = requests.get(api_url, timeout=10)
              if response.status_code == 200:
                  all_jobs = response.json().get('data', [])
                  for job in all_jobs:
                      title_clean = job.get('title', '').lower()
                      loc_clean = job.get('location', '').lower()
                      desc_clean = job.get('description', '').lower()
                      
                      match_skills = not skills or (skills.lower() in title_clean or skills.lower() in desc_clean)
                      match_location = not location or (location.lower() in loc_clean)
                      
                      if match_skills and match_location:
                           jobs_matched.append({
                               "title": job.get('title'),
                               "company_name": job.get('company_name'),
                               "location": job.get('location'),
                               "remote": job.get('remote', False),
                               "url": job.get('url')
                           })
          except Exception as e:
              print(f"API Error: {e}")

      return render_template_string(HTML_TEMPLATE, jobs=jobs_matched, skills=skills, location=location)

  if __name__ == '__main__':
      app.run(debug=True)
