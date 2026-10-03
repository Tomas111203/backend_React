# LDAP Fail2ban Proxy Container (HTTP & LDAP TLS Protection)
FROM nginx:alpine
RUN apk add --no-cache fail2ban iptables

COPY nginx.conf /etc/nginx/nginx.conf
COPY jail.local /etc/fail2ban/jail.local
COPY filter.d/http-flood.conf /etc/fail2ban/filter.d/http-flood.conf
COPY filter.d/ldap-tls.conf /etc/fail2ban/filter.d/ldap-tls.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080 389 636
ENTRYPOINT ["/entrypoint.sh"]
