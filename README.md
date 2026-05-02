# 🎯 Daily Job Hunter — Olasunkanmi Alade

Automated AI-powered job search that runs **every morning at 10:00 AM** and sends a ranked,
scored list of CNC / Mould Inspector / Mechanical Design Engineer roles with visa sponsorship
directly to your email.

---

## How it works

1. GitHub Actions wakes up at 10am UTC every day (free, no server needed)
2. It calls the Claude AI to find and score today's best-matching roles
3. A beautiful HTML email with ranked job cards lands in your inbox

---

## Setup — 4 steps, ~10 minutes

### Step 1 — Create a free GitHub account & repo

1. Go to https://github.com and sign up (free)
2. Click **"New repository"**
3. Name it: `daily-job-hunter`
4. Set it to **Private**
5. Click **Create repository**

### Step 2 — Upload these files

Upload the entire folder structure:
```
daily-job-hunter/
├── .github/
│   └── workflows/
│       └── daily_job_hunt.yml
└── scripts/
    └── job_hunter.py
```

You can drag-and-drop files into GitHub's web interface, or use Git.

### Step 3 — Add your secret keys

In your GitHub repo, go to:
**Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Get from https://console.anthropic.com — sign up free, costs ~$0.01/day |
| `EMAIL_SENDER` | Your Gmail address (e.g. yourname@gmail.com) |
| `EMAIL_PASSWORD` | Gmail **App Password** — see instructions below |
| `EMAIL_RECIPIENT` | olasunkanmi.alade20@gmail.com (or any email you want) |

#### How to get a Gmail App Password:
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already on)
3. Search for **"App passwords"** in Google Account settings
4. Select app: **Mail** → Select device: **Other** → type "Job Hunter"
5. Click **Generate** — copy the 16-character password
6. Use that as your `EMAIL_PASSWORD` secret

### Step 4 — Test it manually

1. In your GitHub repo, go to **Actions** tab
2. Click **"Daily Job Hunt — 10am"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it run — you'll get an email within 2 minutes!

---

## Schedule

The job runs at **10:00 AM UTC** every day.

| Your timezone | Local time |
|---|---|
| Saudi Arabia (AST, UTC+3) | 1:00 PM |
| UK (BST, UTC+1 summer) | 11:00 AM |
| UK (GMT, UTC+0 winter) | 10:00 AM |
| Germany/Netherlands (CEST, UTC+2) | 12:00 PM |
| Japan (JST, UTC+9) | 7:00 PM |

To change the time, edit `.github/workflows/daily_job_hunt.yml` and change the cron line:
- `'0 7 * * *'` = 7am UTC
- `'0 10 * * *'` = 10am UTC (default)

---

## Cost

| Service | Cost |
|---|---|
| GitHub Actions | **Free** (2,000 minutes/month, job uses ~2 min/day) |
| Anthropic API | ~$0.01–$0.03 per day (~$0.30–$0.90/month) |
| Gmail SMTP | **Free** |
| **Total** | **~$1/month** |

---

## What you'll receive

Every morning, a ranked HTML email with:
- 20 matched roles sorted by AI match score (out of 100)
- Tier A / B / C grouping
- Salary ranges, required skills, location
- One-click "Apply Now" buttons linking to live job board searches
- All roles filtered to visa sponsorship only

---

## Troubleshooting

**Email not arriving?**
- Check your GitHub Actions tab for errors
- Make sure the App Password is correct (no spaces when pasting)
- Check spam/junk folder

**"Invalid API key" error?**
- Double-check your ANTHROPIC_API_KEY in GitHub Secrets
- Make sure there are no extra spaces

**Action not running at 10am?**
- GitHub Actions schedules can sometimes be delayed by 15–30 min when GitHub is busy
- Use "Run workflow" manually to test anytime

