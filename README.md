# Radio Recorder – Render Worker + Panel WWW

## Instalacja lokalna

pip install -r requirements.txt
cp .env.example .env
python app.py

## Deploy na Render

1. Wrzuć projekt na GitHub.
2. Wejdź na https://render.com.
3. Kliknij **New → Background Worker**.
4. Wybierz repozytorium.
5. Ustaw zmienne środowiskowe:
   - STREAM_URL
   - RECORD_SECONDS
   - RECORD_TIME
   - KEEP_DAYS
   - MAX_RETRIES
6. Deploy.
7. Render automatycznie wykryje `render.yaml`
8. Utworzy dwa serwisy:
   - radio-recorder-worker
   - radio-recorder-web

Panel WWW:
- pokazuje nagrania
- pozwala pobierać pliki
- pokazuje logi

Nagrania w `OUTPUT_DIR`, logi w `radio.log`, stare pliki usuwane po `KEEP_DAYS`.
