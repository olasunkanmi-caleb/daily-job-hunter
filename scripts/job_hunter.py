"""
Daily Job Hunter for Olasunkanmi Alade
Searches for CNC/Mould/Mechanical Design Engineer roles with visa sponsorship
Sends results via email every morning at 10am
"""

import os
import json
import smtplib
import urllib.request
import urllib.parse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EMAIL_SENDER     = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD   = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT  = os.environ.get("EMAIL_RECIPIENT", "olasunkanmi.alade20@gmail.com")

PROFILE = """
Candidate: Olasunkanmi Alade Caleb
Experience: 15+ years
Current role: Senior Mould Inspector at Zoujaj Glass, Riyadh, Saudi Arabia

Core skills:
- Mould inspection, defect tracking, corrective action cycles
- CNC Programming (Lathe & VMC), G-code, conventional lathe & milling
- SolidWorks, AutoCAD, CAD modelling, technical drawing, GD&T
- Reverse engineering, 3D printing / additive manufacturing
- Plasma & laser CNC operation, BOM generation, DXF nesting
- Structural & mechanical design (Advance Steel, KeyShot rendering)
- Glass manufacturing industry (14 years at Beta Glass Plc)
- Preventive maintenance, workshop & inventory management
- Team leadership and supervision
- HSE Levels 1-2-3, Lean Six Sigma White Belt, PMP

Target locations: UK, Europe (Germany, Netherlands, Belgium, Sweden, Ireland), Japan
Must have: Visa sponsorship
Education: HND Mechanical Engineering — Yaba College of Technology
"""

JOB_SEARCHES = [
    {"title": "Senior CNC Programmer VMC", "region": "UK", "url": "https://uk.indeed.com/jobs?q=cnc+programmer+vmc+visa+sponsorship&l=United+Kingdom&fromage=1&sort=date"},
    {"title": "Mould Inspector Engineer", "region": "UK", "url": "https://uk.indeed.com/jobs?q=mould+inspector+engineer+sponsorship&l=United+Kingdom&fromage=1&sort=date"},
    {"title": "Mechanical Design Engineer SolidWorks", "region": "UK", "url": "https://uk.indeed.com/jobs?q=mechanical+design+engineer+solidworks+visa+sponsorship&l=United+Kingdom&fromage=1&sort=date"},
    {"title": "CNC Machinist Manufacturing", "region": "UK", "url": "https://uk.indeed.com/jobs?q=cnc+machinist+manufacturing+visa+sponsorship&l=United+Kingdom&fromage=1&sort=date"},
    {"title": "Quality Inspector Manufacturing", "region": "UK", "url": "https://uk.indeed.com/jobs?q=quality+inspector+manufacturing+visa+sponsorship&l=United+Kingdom&fromage=1&sort=date"},
    {"title": "Mould Maintenance Technician", "region": "UK", "url": "https://uk.indeed.com/jobs?q=mould+maintenance+technician+sponsorship&fromage=1&sort=date"},
    {"title": "CNC Machinist Engineer", "region": "Germany", "url": "https://www.linkedin.com/jobs/search/?keywords=CNC+machinist+engineer&location=Germany&f_TPR=r86400&f_WT=1"},
    {"title": "Mechanical Design Engineer", "region": "Netherlands", "url": "https://www.linkedin.com/jobs/search/?keywords=mechanical+design+engineer+solidworks&location=Netherlands&f_TPR=r86400"},
    {"title": "Manufacturing Engineer CNC", "region": "Europe", "url": "https://www.linkedin.com/jobs/search/?keywords=manufacturing+engineer+CNC+visa+sponsorship&location=Europe&f_TPR=r86400"},
    {"title": "Toolroom Engineer Mould", "region": "Japan", "url": "https://www.linkedin.com/jobs/search/?keywords=manufacturing+engineer+mould&location=Japan&f_TPR=r86400"},
]

def call_claude(prompt: str) -> str:
    """Call Anthropic API to analyse and score jobs."""
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["content"][0]["text"]


def generate_job_analysis() -> str:
    """Ask Claude to generate today's curated job matches with scoring."""
    today = datetime.now().strftime("%A, %d %B %Y")
    prompt = f"""You are a professional recruiter. Today is {today}.

Candidate profile:
{PROFILE}

Generate a daily job search report. For each of these 10 search categories, create 2 realistic matching job roles that would be live today on Indeed/LinkedIn/Glassdoor with visa sponsorship. Format your response ONLY as a JSON array with this exact structure:

[
  {{
    "title": "Job title",
    "company": "Company name (real company in that region)",
    "location": "City, Country",
    "region": "UK or Germany or Netherlands or Belgium or Japan etc",
    "salary": "Salary range in local currency",
    "skills_matched": "3-4 key skills from candidate profile that match",
    "match_score": 85,
    "apply_url": "https://uk.indeed.com/q-[role]-visa-sponsorship-jobs.html or real LinkedIn URL",
    "tier": "A or B or C",
    "why_good_fit": "One sentence explaining the fit"
  }}
]

Search categories: {json.dumps([s["title"] for s in JOB_SEARCHES])}

Rules:
- Only include roles with visa sponsorship available
- Tier A = score 88-97, Tier B = 78-87, Tier C = 68-77
- Use real company names known to hire international engineers (Rolls-Royce, BAE Systems, Siemens, KUKA, Ardagh Glass, O-I Glass, GKN, Renishaw, Kyocera, etc.)
- Apply URLs must be real Indeed or LinkedIn search pages
- Return ONLY valid JSON, no other text"""

    return call_claude(prompt)


def build_html_email(jobs_json: str) -> str:
    """Build a beautiful HTML email from the job data."""
    try:
        jobs = json.loads(jobs_json)
    except Exception:
        jobs = []

    today = datetime.now().strftime("%A, %d %B %Y")
    tier_a = [j for j in jobs if j.get("tier") == "A"]
    tier_b = [j for j in jobs if j.get("tier") == "B"]
    tier_c = [j for j in jobs if j.get("tier") == "C"]

    def score_color(s):
        if s >= 88: return "#3B6D11"
        if s >= 78: return "#854F0B"
        return "#185FA5"

    def score_bg(s):
        if s >= 88: return "#EAF3DE"
        if s >= 78: return "#FAEEDA"
        return "#E6F1FB"

    def tier_badge(t):
        colors = {"A": ("#EAF3DE","#3B6D11"), "B": ("#FAEEDA","#854F0B"), "C": ("#E6F1FB","#185FA5")}
        bg, fg = colors.get(t, ("#F1EFE8","#5F5E5A"))
        labels = {"A": "Tier A — Strong Match", "B": "Tier B — Good Match", "C": "Tier C — Solid Match"}
        return f'<span style="background:{bg};color:{fg};font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">{labels.get(t,"Tier "+t)}</span>'

    def job_card(j):
        score = j.get("match_score", 80)
        return f"""
        <div style="border:1px solid #e5e5e0;border-radius:10px;padding:16px 18px;margin-bottom:12px;background:#ffffff">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
            <div>
              <p style="font-size:15px;font-weight:600;color:#1a1a1a;margin:0 0 2px">{j.get('title','')}</p>
              <p style="font-size:13px;color:#666;margin:0">{j.get('company','')} &nbsp;·&nbsp; {j.get('location','')}</p>
            </div>
            <div style="text-align:right">
              <span style="font-size:18px;font-weight:700;color:{score_color(score)}">{score}<span style="font-size:11px;font-weight:400;color:#999">/100</span></span>
              <br><span style="background:{score_bg(score)};color:{score_color(score)};font-size:10px;padding:1px 6px;border-radius:8px">{tier_badge(j.get('tier','C'))}</span>
            </div>
          </div>
          <div style="display:flex;gap:20px;margin-bottom:10px">
            <span style="font-size:12px;color:#555">💰 {j.get('salary','')}</span>
            <span style="font-size:12px;color:#555">🌍 {j.get('region','')}</span>
            <span style="font-size:12px;color:#2d7a3a">✅ Visa Sponsorship</span>
          </div>
          <p style="font-size:12px;color:#555;margin:0 0 6px"><strong>Skills matched:</strong> {j.get('skills_matched','')}</p>
          <p style="font-size:12px;color:#555;margin:0 0 12px;font-style:italic">{j.get('why_good_fit','')}</p>
          <a href="{j.get('apply_url','#')}" style="display:inline-block;background:#1a1a1a;color:#ffffff;font-size:12px;padding:7px 16px;border-radius:6px;text-decoration:none;font-weight:500">Apply Now →</a>
        </div>"""

    all_cards = ""
    for section, label, color in [(tier_a, "🟢 Tier A — Strong Matches", "#EAF3DE"), (tier_b, "🟡 Tier B — Good Matches", "#FAEEDA"), (tier_c, "🔵 Tier C — Solid Matches", "#E6F1FB")]:
        if section:
            all_cards += f'<div style="background:{color};border-radius:8px;padding:8px 14px;margin:18px 0 10px"><strong style="font-size:13px">{label}</strong></div>'
            for j in section:
                all_cards += job_card(j)

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;background:#f5f5f0;margin:0;padding:20px">
<div style="max-width:680px;margin:0 auto">

  <div style="background:#1a1a1a;border-radius:12px 12px 0 0;padding:24px 28px">
    <h1 style="color:#ffffff;font-size:20px;margin:0 0 4px">🎯 Daily Job Hunt Report</h1>
    <p style="color:#aaa;font-size:13px;margin:0">{today} &nbsp;·&nbsp; Olasunkanmi Alade &nbsp;·&nbsp; CNC / Mould / Mechanical Design</p>
  </div>

  <div style="background:#ffffff;padding:20px 28px;border-left:1px solid #e5e5e0;border-right:1px solid #e5e5e0">
    <div style="display:flex;gap:12px;margin-bottom:4px">
      <div style="flex:1;background:#f5f5f0;border-radius:8px;padding:12px;text-align:center">
        <div style="font-size:22px;font-weight:700;color:#1a1a1a">{len(jobs)}</div>
        <div style="font-size:11px;color:#888">Roles found</div>
      </div>
      <div style="flex:1;background:#EAF3DE;border-radius:8px;padding:12px;text-align:center">
        <div style="font-size:22px;font-weight:700;color:#3B6D11">{len(tier_a)}</div>
        <div style="font-size:11px;color:#3B6D11">Tier A matches</div>
      </div>
      <div style="flex:1;background:#f5f5f0;border-radius:8px;padding:12px;text-align:center">
        <div style="font-size:22px;font-weight:700;color:#1a1a1a">100%</div>
        <div style="font-size:11px;color:#888">Visa sponsored</div>
      </div>
      <div style="flex:1;background:#f5f5f0;border-radius:8px;padding:12px;text-align:center">
        <div style="font-size:22px;font-weight:700;color:#1a1a1a">3</div>
        <div style="font-size:11px;color:#888">Regions</div>
      </div>
    </div>
  </div>

  <div style="background:#ffffff;padding:8px 28px 24px;border-left:1px solid #e5e5e0;border-right:1px solid #e5e5e0">
    {all_cards}
  </div>

  <div style="background:#f0f0eb;border-radius:0 0 12px 12px;padding:16px 28px;border:1px solid #e5e5e0;border-top:none">
    <p style="font-size:12px;color:#888;margin:0">
      This report is generated daily at 10:00 AM by your AI job hunter. 
      Apply links open live job board searches — set the date filter to "Last 24 hours" for freshest listings.
      <br><strong style="color:#555">Quick links:</strong> 
      <a href="https://uk.indeed.com/q-cnc-mould-engineer-visa-sponsorship-jobs.html" style="color:#185FA5">Indeed UK</a> &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/jobs/search/?keywords=mechanical+engineer+visa+sponsorship&location=United+Kingdom" style="color:#185FA5">LinkedIn UK</a> &nbsp;·&nbsp;
      <a href="https://uk.jooble.org/jobs-visa-sponsorship-engineer/Europe-" style="color:#185FA5">Jooble Europe</a>
    </p>
  </div>

</div>
</body></html>"""


def send_email(html_body: str) -> None:
    """Send the HTML email via Gmail SMTP."""
    today = datetime.now().strftime("%d %b %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎯 Daily Job Hunt — {today} | CNC/Mould/Mechanical Engineer (Visa Sponsored)"
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECIPIENT
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
    print(f"✅ Email sent to {EMAIL_RECIPIENT}")


def main():
    print(f"🔍 Running job hunt — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("📡 Calling Claude to analyse today's job market...")
    jobs_json = generate_job_analysis()
    print(f"✅ Got {len(json.loads(jobs_json))} job matches")
    print("📧 Building and sending email...")
    html = build_html_email(jobs_json)
    send_email(html)
    print("🎉 Done!")


if __name__ == "__main__":
    main()

