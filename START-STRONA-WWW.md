# CAR GAZ – AUTA Z USA | publikacja strony 1.5

## 1. Podgląd na swoim komputerze
Rozpakuj ZIP. Otwórz `kalkulator.html` w Chrome lub Edge. Do odczytu publicznych stron aukcji zainstaluj Python 3 (https://www.python.org/downloads/), a następnie uruchom `URUCHOM-WINDOWS.bat` lub polecenie `python server.py` w katalogu projektu. Otwórz http://127.0.0.1:8000. Na Mac/Linux użyj `python3 server.py`.

## 2. Publikacja w internecie (GitHub + Render)
1. Załóż konto na https://github.com i utwórz prywatne repozytorium np. `car-gaz-www`. Rozpakuj ZIP i wgraj zawartość katalogu (pliki w katalogu głównym repozytorium, z folderem `src`). Nie umieszczaj kluczy API lub haseł w repozytorium.
2. Zaloguj się na https://render.com, wybierz New > Web Service i połącz repozytorium GitHub. Zezwól na dostęp do tego repozytorium. Ustaw Runtime: Python, Root Directory: puste, Build Command: `pip install -r requirements.txt && python build.py`, Start Command: `gunicorn app:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 40`. Health Check Path: `/health`. Alternatywnie użyj New > Blueprint (z pliku `render.yaml`).
3. Wybierz plan. Free do testów (usypia po okresie bezczynności); dla klientów wybierz plan płatny, sprawdź aktualny koszt. Kliknij Create Web Service. Po udanym wdrożeniu otwórz przydzielony adres `*.onrender.com`.
4. Kup wolną domenę albo użyj posiadanej. W Render: Settings > Custom Domains > Add Custom Domain. W panelu operatora domeny ustaw dokładnie rekordy DNS wskazane przez Render, następnie zweryfikuj domenę. Render zapewnia certyfikat TLS. Nie zgaduj adresów IP ani rekordów DNS. Przed zmianami istniejącej domeny zachowaj rekordy obsługujące pocztę.
5. Po zmianie kodu w repozytorium Render może automatycznie wdrożyć nową wersję. Przed publikacją testuj kalkulację i działanie linków aukcyjnych na rzeczywistym hostingu.

Dokumentacja: https://render.com/docs/web-services ; https://render.com/docs/custom-domains ; https://render.com/docs/free

## 3. Zanim udostępnisz klientom
- Uzupełnij dane kontaktowe, dane przedsiębiorcy i informacje o prywatności w `index.html`. Nie podano ich w briefie, więc nie wymyślono numeru telefonu ani adresu. Tekst stopki jest jawnie oznaczony jako do uzupełnienia. Uzupełnij właściwe informacje prawne zgodnie z rzeczywistym modelem usług i przetwarzania danych.
- Zweryfikuj z agencją celną stawki i podstawy oraz sprawdź cenniki kont aukcyjnych. Aktualne założenia są szacunkowe; brak akcyzy jest wyraźnie oznaczony. Suwak zmienia planowaną cenę faktycznego zakupu.
- Odczyt publicznych ofert działa tylko jeśli strona aukcyjna udostępnia dane; nie omijamy blokad. Do niezawodnego odczytu potrzebna jest autoryzowana integracja API. W razie błędu wybierz stan ręcznie. Sprawdź warunki korzystania z danych aukcyjnych przed uruchomieniem publicznym.
- Serwis nie ma logowania, panelu administracyjnego, CRM ani bazy wycen. Historia jest lokalna. Stawki w JavaScript są publiczne, więc nie umieszczaj w nich danych poufnych. Serwer ma podstawowy limit globalny 30 zapytań/min na proces i limit 3 jednoczesnych odczytów, ale przed większym ruchem należy dobrać ochronę i monitoring. Wdrożenie na rzeczywistym hostingu i połączenia z aukcjami nie zostały potwierdzone w tym środowisku.

## 4. Edycja
- `index.html`: teksty, logo osadzone w HTML, ilustracje SVG, nawigacja i stopka. `logo.jpg`: oryginał logo.
- `src/style.css`: kolory, wygląd i responsywność.
- `src/config.js`: stawki firmowe, aukcyjne i transportowe.
- `src/engine.js`: niezmieniony silnik kalkulatora 1.4.
- `src/ui.js`: interakcje i podsumowania.
- `app.py`: publiczny serwer WSGI; `server.py`: lokalny serwer i parser ofert.
- `python build.py` składa plik `kalkulator.html` z kodu źródłowego; po edycji zawsze uruchom ponownie. Render wykonuje to automatycznie podczas budowania.
- Testy: `node test.js`, `python -m unittest test_server.py test_app.py`. 54 testy silnika + 4 parsera + 4 aplikacji WSGI. Interfejs sprawdzony w Chromium przez osadzenie HTML: suwak, usługa, tryb transportu, motyw i szerokość 390 px. Test serwera z rzeczywistą siecią i Gunicorn pozostaje do wykonania po publikacji.
