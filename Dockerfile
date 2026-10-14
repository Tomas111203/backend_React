# Backend Dockerfile: Python 3.11 FastAPI Microservice with Fail2ban & Nginx Reverse Proxy
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    fail2ban \
    iptables \
    procps \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar Nuclei desde la imagen oficial
COPY --from=projectdiscovery/nuclei:latest /usr/local/bin/nuclei /usr/local/bin/nuclei

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY nginx.conf /etc/nginx/sites-available/default
COPY jail.local /etc/fail2ban/jail.local
COPY filter.d/http-flood.conf /etc/fail2ban/filter.d/http-flood.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
