# Radio Recorder – Wdrożenie na Serv00.com

Ten dokument opisuje krok po kroku, jak skonfigurować i uruchomić aplikację **Radio Recorder** na darmowym hostingu **Serv00.com**.

---

## 🛠️ 1. Wstępna konfiguracja w Panelu Serv00

Przed zalogowaniem się na SSH wykonaj poniższe czynności w panelu zarządzania Serv00 (`panelX.serv00.com`):

1. **Włączenie procesów w tle:**
   * Przejdź do: **Additional services** $\rightarrow$ **Run background processes**.
   * Zmień status na **Enabled** (zapobiegnie to zabijaniu aplikacji po wylogowaniu z SSH).

2. **Rezerwacja portu TCP:**
   * Przejdź do: **Toolbox** $\rightarrow$ **Port reservation**.
   * Wygeneruj nowy port TCP (zapisz go, np. `12345`). Alternatywnie w konsoli SSH:
     ```bash
     devil port add tcp
     ```

3. **Konfiguracja strony WWW (Reverse Proxy):**
   * Przejdź do: **WWW websites** $\rightarrow$ **Add new website**.
   * **Domain:** Podaj swoją domenę/subdomenę w Serv00 (np. `twojanazwa.serv00.net`).
   * **Website type:** Wybierz **Proxy**.
   * **Proxy redirect:** Wpisz `http://127.0.0.1:TWOJ_PORT` (zamień `TWOJ_PORT` na wygenerowany port, np. `http://127.0.0.1:12345`).

---

## 📂 2. Pobranie i przygotowanie kodu (SSH)

Zaloguj się na serwer przez SSH (`ssh login@panelX.serv00.com`):

```bash
# 1. Pobierz repozytorium
git clone https://github.com/kamil600/radio-recorder.git
cd radio-recorder

# 2. (Opcjonalnie) Usuń zbędne pliki Dockerowe
rm -rf docker-compose.yml nginx/ web/Dockerfile worker/Dockerfile

# 3. Utwórz folder na nagrania (jeśli nie istnieje)
mkdir -p recordings
```

---

## 📦 3. Instalacja zależności

Skonfiguruj wspólne środowisko wirtualne Pythona dla panelu WWW (`web`) oraz Workera (`worker`):

```bash
# Utworzenie i aktywacja środowiska wirtualnego
python3 -m venv venv
source venv/bin/activate

# Aktualizacja pip oraz instalacja pakietów z obu części projektu + Gunicorn
pip install --upgrade pip
pip install -r web/requirements.txt -r worker/requirements.txt gunicorn
```

> **Uwaga:** Upewnij się, że narzędzie `ffmpeg` jest dostępne w systemie, uruchamiając komendę `ffmpeg -version`. Na Serv00 jest ono zainstalowane domyślnie.

---

## ⚙️ 4. Konfiguracja zmiennych środowiskowych

Upewnij się, że plik konfiguracji workera `worker/.env` zawiera prawidłowe ścieżki i ustawienia:

```bash
# Utwórz plik .env jeśli nie istnieje
cp worker/.env.example worker/.env 2>/dev/null || touch worker/.env
```

Edytuj plik `worker/.env` (np. za pomocą `nano worker/.env`) i dostosuj ścieżki zapisu nagrań, aby wskazywały na względny katalog lub pełną ścieżkę na Twoim koncie:
```env
RECORDINGS_DIR=./recordings
```

---

## 🚀 5. Uruchomienie aplikacji w tle (PM2)

Do zarządzania procesami i zapewnienia ich ciągłego działania w tle użyjemy **PM2**.

### Krok A: Instalacja PM2
```bash
npm install -g pm2
```

### Krok B: Uruchomienie usług

1. **Uruchomienie panelu Web (Flask + Gunicorn):**
   *(Zamień `12345` na swój zarezerwowany port TCP)*
   ```bash
   pm2 start "venv/bin/gunicorn -b 127.0.0.1:12345 web.server:app" --name radio-web
   ```

2. **Uruchomienie Workera nagrywającego:**
   ```bash
   pm2 start worker/app.py --name radio-worker --interpreter ./venv/bin/python
   ```

3. **Zapisanie stanu procesów PM2:**
   ```bash
   pm2 save
   ```

---

## 🔄 6. Automatyczny restart po restarcie serwera (Cron)

Serv00 może okazyjnie restartować swoje węzły. Aby aplikacje wstawały automatycznie po restarcie:

1. Otwórz edytor tabeli Cron:
   ```bash
   crontab -e
   ```
2. Dodaj na końcu poniższą linijkę (zamień `TWOJ_USER` na swój login na Serv00):
   ```cron
   @reboot /home/TWOJ_USER/.npm-global/bin/pm2 resurrect
   ```

---

## 📊 Przydatne komendy PM2

* **Sprawdzenie statusu aplikacji:** `pm2 status`
* **Podgląd logów na żywo:** `pm2 logs`
* **Podgląd logów konkretnej usługi:** `pm2 logs radio-web` lub `pm2 logs radio-worker`
* **Restart aplikacji:** `pm2 restart all`
* **Zatrzymanie aplikacji:** `pm2 stop all`
