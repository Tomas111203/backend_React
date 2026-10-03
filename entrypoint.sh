#!/bin/sh
# entrypoint.sh — Backend (python:3.11-slim) with Nginx reverse proxy and optional Fail2ban.
#
# Fail2ban requires the host kernel to support iptables (Linux with NET_ADMIN).
# On Docker Desktop for Windows / macOS the kernel capability may not be fully
# available, so we treat a Fail2ban startup failure as non-fatal: Nginx and
# Uvicorn still start and serve the API; Fail2ban just won't be protecting it.

set -e

# ── 1. Nginx log files ────────────────────────────────────────────────────────
mkdir -p /var/log/nginx
rm -f /var/log/nginx/access.log /var/log/nginx/error.log
touch /var/log/nginx/access.log /var/log/nginx/error.log
chmod 644 /var/log/nginx/access.log /var/log/nginx/error.log

# ── 2. Fail2ban (best-effort) ─────────────────────────────────────────────────
mkdir -p /var/run/fail2ban
rm -f /var/run/fail2ban/fail2ban.sock /var/run/fail2ban/fail2ban.pid

if fail2ban-server \
       -b \
       -s /var/run/fail2ban/fail2ban.sock \
       -p /var/run/fail2ban/fail2ban.pid; then
  echo "[entrypoint] Fail2ban started successfully."
else
  echo "[entrypoint] WARNING: Fail2ban could not start (iptables/kernel unavailable?). Nginx will run unprotected."
fi

# ── 3. Stream access log to docker logs ───────────────────────────────────────
tail -f /var/log/nginx/access.log &

# ── 4. Uvicorn FastAPI microservice on loopback (behind Nginx) ────────────────
uvicorn app.main:app --host 127.0.0.1 --port 8001 &

# ── 5. Nginx reverse proxy (foreground, PID 1) ────────────────────────────────
exec nginx -g "daemon off;"
