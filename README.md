# 📘 Radio Recorder (Docker + Oracle Cloud VPS)

Radio Recorder to aplikacja, która automatycznie nagrywa strumień MP3 (np. *Chant Grégorien* z Radio Esperance), zapisuje nagrania na serwerze, rotuje stare pliki i udostępnia panel WWW do pobierania nagrań oraz przeglądania logów.

Projekt działa w Dockerze i jest zoptymalizowany pod darmowy VPS Oracle Cloud Free Tier.

## 🧱 Struktura projektu

radio-recorder/  
│  
├── worker/  
│   ├── app.py  
│   ├── requirements.txt  
│   ├── .env  
│   └── Dockerfile  
│  
├── web/  
│   ├── server.py  
│   ├── requirements.txt  
│   ├── templates/  
│   │   └── index.html  
│   └── Dockerfile  
│  
├── nginx/  
│   ├── default.conf  
│   └── Dockerfile  
│  
└── docker-compose.yml  

## ⚙️ Instalacja na Oracle Cloud VPS

### 1. Połącz się z serwerem

ssh ubuntu@PUBLICZNY_ADRES_VPS

### 2. Zainstaluj Docker + Compose

sudo apt update  
sudo apt install -y docker.io docker-compose  
sudo systemctl enable docker  
sudo systemctl start docker  

### 3. Wgraj projekt

git clone https://github.com/USER/radio-recorder.git  
cd radio-recorder  

### 4. Uruchom kontenery

sudo docker-compose up -d  

docker ps  

## 🎧 Worker – nagrywanie radia

Worker nagrywa strumień MP3 bez transkodowania (`-c copy`), dzięki czemu:

- nie obciąża CPU,
- nie traci jakości,
- działa stabilnie.

### Konfiguracja w `worker/.env`:

STREAM_URL=https://radio-esperance.stream/chant-gregorien.mp3  
RECORD_SECONDS=3600  
OUTPUT_DIR=./recordings  
RECORD_TIME=08:00  
KEEP_DAYS=7  
MAX_RETRIES=3

## 🌐 Panel WWW

Panel działa na porcie 80 (przez Nginx):

http://PUBLICZNY_ADRES_VPS

Funkcje:

- lista nagrań,
- pobieranie plików,
- podgląd logów.

## 🧩 docker-compose.yml

Uruchamia trzy serwisy:

- `worker` – nagrywanie,
- `web` – panel WWW,
- `nginx` – reverse proxy.

Współdzielone wolumeny:

- `recordings`
- `logs`

## 🔐 Firewall w Oracle Cloud

Networking → VCN → Security Lists → Ingress Rules

Porty:

- 80/TCP – Panel WWW  
- 8000/TCP – test bez nginx

## 🔁 Restartowanie i logi

Restart kontenerów:  

sudo docker-compose restart  

Logi worker:  

docker logs -f radio_worker  

Logi panelu:

docker logs -f radio_web

## 🎉 Podsumowanie

Projekt:

- działa 24/7 na darmowym VPS Oracle,
- nagrywa strumień MP3 bez transkodowania,
- ma panel WWW,
- działa w Dockerze,
- restartuje się automatycznie,
- jest łatwy do rozwijania.
