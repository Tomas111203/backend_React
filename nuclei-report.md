tomas@LAPTOP-JK5OEQ3H:/mnt/c/Users/tomas/OneDrive/Escritorio/UAA/Noveno Semestre/Ciberseguridad/React,ldap_JWT/videogames-ldap-jwt-lab$ docker compose -f backend/docker-compose.yml --profile scan run --rm nuclei   -target http://videogames-api:8000   -o /reports/phpldapadmin-report.txt

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[INF] nuclei-templates are not installed, installing...
[INF] Successfully installed nuclei-templates at /root/nuclei-templates
[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.0 (latest)
[INF] New templates added in latest release: 295
[INF] Templates loaded for current scan: 11144
[INF] Executing 11144 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 2724 (Reduced 2588 Requests)
[INF] Using Interactsh Server: oast.site
[swagger-api] [http] [info] http://videogames-api:8000/docs [paths="/docs"]
[waf-detect:nginxgeneric] [http] [info] http://videogames-api:8000
[INF] Skipped videogames-api:9780 from target list as found unresponsive permanently: cause="port closed or filtered" address=videogames-api:9780 chain="connection refused; got err while executing http://videogames-api:9780/api/v1/user_assets/nfc"
[redoc-api-docs] [http] [info] http://videogames-api:8000/redoc
[http-missing-security-headers:x-content-type-options] [http] [info] http://videogames-api:8000
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:strict-transport-security] [http] [info] http://videogames-api:8000
[http-missing-security-headers:content-security-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:permissions-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://videogames-api:8000
[http-missing-security-headers:referrer-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://videogames-api:8000
[http-missing-security-headers:x-frame-options] [http] [info] http://videogames-api:8000
[options-method] [http] [info] http://videogames-api:8000 ["GET"]
[missing-sri] [http] [info] http://videogames-api:8000/ ["https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap"]
[openapi] [http] [info] http://videogames-api:8000/openapi.json
[INF] Skipped videogames-api:4040 from target list as found unresponsive permanently: cause="port closed or filtered" address=videogames-api:4040 chain="connection refused; got err while executing http://videogames-api:4040/jobs/"
[tech-detect:nginx] [http] [info] http://videogames-api:8000
[tech-detect:google-font-api] [http] [info] http://videogames-api:8000
[INF] Skipped videogames-api:5814 from target list as found unresponsive permanently: Get "https://videogames-api:5814/autopass": cause="port closed or filtered" address=videogames-api:5814 chain="connection refused"
[INF] Scan completed in 2m. 18 matches found.
[INF] HTTP connections: 13840 total, 4451 new, 9389 reused (67.8%)