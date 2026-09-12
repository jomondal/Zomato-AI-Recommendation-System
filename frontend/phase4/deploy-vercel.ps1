# One-command Vercel production deploy for the dashboard.
# API calls are proxied via vercel.json to Render — no VITE_API_URL needed.
# Usage:
#   1. npx vercel login
#   2. .\deploy-vercel.ps1

npx vercel deploy --prod --yes
