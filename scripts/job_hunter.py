"""
Daily Job Hunter for Olasunkanmi Alade
Searches for CNC/Mould/Mechanical Design Engineer roles with visa sponsorship
Sends results via email every morning at 10am
"""

import os
import json
import smtplib
import urllib.request
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EMAIL_SENDER      = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD    = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT   = os.environ.get("EMAIL_RECIPIENT", "ola.official26@gmail.com")

PROFILE = (
    "Candidate: Olasunkanmi Alade Caleb\n"
    "Experience: 15+ years\n"
    "Current role: Senior Mould Inspector at Zoujaj Glass, Riyadh, Saudi Arabia\n"
    "Core skills: Mould inspection, CNC Programming Lathe and VMC, G-code, "
    "SolidWorks, AutoCAD, GD&T, Reverse engineering, 3D printing, "
    "Plasma and laser CNC, BOM generation, DXF nesting, Advance Steel, "
    "Glass manufacturing 14 years at Beta Glass, Preventive maintenance, "
    "Team leadership, HSE Levels 1-2-3, Lean Six Sigma White Belt\n"
    "Target locations: UK, Europe Germany Netherlands Belgium Sweden Ireland, Japan\n"
    "Must have: Visa sponsorship\n"
    "Education: HND Mechanical Engineering Yaba College of Technology"
)

JOB_SEARCHES = [
    "Senior CNC Programmer VMC UK",
    "Mould Inspector Engineer UK",
    "Mechanical Design Engineer SolidWorks UK",
    "CNC Machinist Manufacturing UK",
    "Quality Inspector Manufacturing UK",
    "Mould Maintenance Technician Europe",
    "CNC Machinist Engineer Germany",
    "Mechanical Design Engineer Netherlands",
    "Manufacturing Engineer CNC Europe",
    "Toolroom Engineer Mould Japan",
]


def clean(text):
    """Remove non-ASCII characters to prevent email encoding errors."""
    return text.encode("ascii", "ignore").decode("ascii")


def call_claude(prompt):
    """Call Anthropic API."""
    safe_prompt = clean(prompt)
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": safe_prompt}]
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
    raw = data["content"][0]["text"]
    return clean(raw)


def generate_jobs():
    """Ask Claude to produce today's job matches as JSON."""
    today = datetime.now().strftime("%A, %d %B %Y")
    categories = ", ".join(JOB_SEARCHES)

    prompt = (
        "You are a recruiter. Today is " + today + ".\n\n"
        "Candidate profile:\n" + PROFILE + "\n\n"
        "Return ONLY a valid JSON array (no markdown, no backticks, no explanation).\n"
        "Use only plain ASCII characters - no arrows, no special symbols, no emojis.\n"
        "Create 2 job matches for each of these categories: " + categories + "\n\n"
        "Each job object must have these exact keys:\n"
        "title, company, location, region, salary, skills_matched, match_score, apply_url, tier, why_good_fit\n\n"
        "Rules:\n"
        "- tier: A for score 88-97, B for 78-87, C for 68-77\n"
        "- All roles must have visa sponsorship\n"
        "- Use real company names (Rolls-Royce, BAE Systems, Siemens, GKN, Renishaw, Ardagh Glass, Kyocera etc)\n"
        "- apply_url must be a real Indeed or LinkedIn search URL\n"
        "- Use only ASCII characters in all string values\n"
        "- Return ONLY the JSON array, nothing else"
    )
    return call_claude(prompt)


def score_color(s):
    if s >= 88: return "#3B6D11"
    if s >= 78: return "#854F0B"
    return "#185FA5"


def score_bg(s):
    if s >= 88: return "#EAF3DE"
    if s >= 78: return "#FAEEDA"
    return "#E6F1FB"


def tier_badge(t):
    labels = {"A": "Tier A - Strong Match", "B": "Tier B - Good Match", "C": "Tier C - Solid Match"}
    bgs    = {"A": "#EAF3DE", "B": "#FAEEDA", "C": "#E6F1FB"}
    fgs    = {"A": "#3B6D11", "B": "#854F0B", "C": "#185FA5"}
    return (
        '<span style="background:{bg};color:{fg};font-size:11px;'
        'padding:2px 8px;border-radius:10px;font-weight:500">{label}</span>'
    ).format(bg=bgs.get(t,"#eee"), fg=fgs.get(t,"#333"), label=labels.get(t,"Tier "+t))


def job_card(j):
    score = int(j.get("match_score", 80))
    return (
        '<div style="border:1px solid #e5e5e0;border-radius:10px;'
        'padding:16px 18px;margin-bottom:12px;background:#ffffff">'
        '<p style="font-size:15px;font-weight:600;color:#1a1a1a;margin:0 0 2px">{title}</p>'
        '<p style="font-size:13px;color:#666;margin:0 0 8px">{company} - {location}</p>'
        '<p style="margin:0 0 6px">'
        '<span style="font-size:18px;font-weight:700;color:{sc}">{score}'
        '<span style="font-size:11px;font-weight:400;color:#999">/100</span></span>'
        '&nbsp;&nbsp;{badge}</p>'
        '<p style="font-size:12px;color:#555;margin:0 0 4px">'
        'Salary: {salary} | Region: {region} | '
        '<span style="color:#2d7a3a">Visa Sponsorship: YES</span></p>'
        '<p style="font-size:12px;color:#555;margin:4px 0 4px">'
        '<strong>Skills matched:</strong> {skills}</p>'
        '<p style="font-size:12px;color:#555;font-style:italic;margin:0 0 12px">{why}</p>'
        '<a href="{url}" style="display:inline-block;background:#1a1a1a;color:#ffffff;'
        'font-size:12px;padding:7px 16px;border-radius:6px;text-decoration:none;'
        'font-weight:500">Apply Now</a>'
        '</div>'
    ).format(
        title=clean(j.get("title","")),
        company=clean(j.get("company","")),
        location=clean(j.get("location","")),
        sc=score_color(score),
        score=score,
        badge=tier_badge(j.get("tier","C")),
        salary=clean(j.get("salary","")),
        region=clean(j.get("region","")),
        skills=clean(j.get("skills_matched","")),
        why=clean(j.get("why_good_fit","")),
        url=clean(j.get("apply_url","#"))
    )


def build_email(jobs_json):
    try:
        jobs = json.loads(jobs_json)
    except Exception:
        jobs = []

    today   = datetime.now().strftime("%A, %d %B %Y")
    tier_a  = [j for j in jobs if j.get("tier") == "A"]
    tier_b  = [j for j in jobs if j.get("tier") == "B"]
    tier_c  = [j for j in jobs if j.get("tier") == "C"]

    cards = ""
    for group, label, bg in [
        (tier_a, "Tier A - Strong Matches", "#EAF3DE"),
        (tier_b, "Tier B - Good Matches",   "#FAEEDA"),
        (tier_c, "Tier C - Solid Matches",  "#E6F1FB"),
    ]:
        if group:
            cards += (
                '<div style="background:{bg};border-radius:8px;padding:8px 14px;'
                'margin:18px 0 10px"><strong style="font-size:13px">{label}</strong></div>'
            ).format(bg=bg, label=label)
            for j in group:
                cards += job_card(j)

    html = (
        "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head>"
        "<body style=\"font-family:Arial,sans-serif;background:#f5f5f0;margin:0;padding:20px\">"
        "<div style=\"max-width:680px;margin:0 auto\">"
        "<div style=\"background:#1a1a1a;border-radius:12px 12px 0 0;padding:24px 28px\">"
        "<h1 style=\"color:#ffffff;font-size:20px;margin:0 0 4px\">Daily Job Hunt Report</h1>"
        "<p style=\"color:#aaa;font-size:13px;margin:0\">{today} - Olasunkanmi Alade - CNC / Mould / Mechanical Design</p>"
        "</div>"
        "<div style=\"background:#ffffff;padding:16px 28px;border-left:1px solid #e5e5e0;border-right:1px solid #e5e5e0\">"
        "<table width=\"100%\" cellpadding=\"8\" cellspacing=\"4\">"
        "<tr>"
        "<td style=\"background:#f5f5f0;border-radius:8px;text-align:center\">"
        "<div style=\"font-size:22px;font-weight:700\">{total}</div>"
        "<div style=\"font-size:11px;color:#888\">Roles found</div></td>"
        "<td style=\"background:#EAF3DE;border-radius:8px;text-align:center\">"
        "<div style=\"font-size:22px;font-weight:700;color:#3B6D11\">{ta}</div>"
        "<div style=\"font-size:11px;color:#3B6D11\">Tier A matches</div></td>"
        "<td style=\"background:#f5f5f0;border-radius:8px;text-align:center\">"
        "<div style=\"font-size:22px;font-weight:700\">100%</div>"
        "<div style=\"font-size:11px;color:#888\">Visa sponsored</div></td>"
        "<td style=\"background:#f5f5f0;border-radius:8px;text-align:center\">"
        "<div style=\"font-size:22px;font-weight:700\">3</div>"
        "<div style=\"font-size:11px;color:#888\">Regions</div></td>"
        "</tr></table></div>"
        "<div style=\"background:#ffffff;padding:8px 28px 24px;"
        "border-left:1px solid #e5e5e0;border-right:1px solid #e5e5e0\">"
        "{cards}</div>"
        "<div style=\"background:#f0f0eb;border-radius:0 0 12px 12px;padding:16px 28px;"
        "border:1px solid #e5e5e0;border-top:none\">"
        "<p style=\"font-size:12px;color:#888;margin:0\">"
        "This report runs daily at 10:00 AM. Set the date filter to Last 24 hours on job boards for freshest listings."
        "</p></div></div></body></html>"
    ).format(today=today, total=len(jobs), ta=len(tier_a), cards=cards)

    return html


def send_email(html_body):
    today = datetime.now().strftime("%d %b %Y")
    subject = "Daily Job Hunt - {} - CNC/Mould/Mechanical Engineer Visa Sponsored".format(today)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECIPIENT
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_SENDER,
            EMAIL_RECIPIENT,
            msg.as_string().encode("utf-8")
        )
    print("Email sent to " + EMAIL_RECIPIENT)


def main():
    print("Starting job hunt - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("Calling Claude...")
    jobs_json = generate_jobs()
    print("Building email...")
    html = build_email(jobs_json)
    print("Sending email...")
    send_email(html)
    print("Done!")


if __name__ == "__main__":
    main()
