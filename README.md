# CAR GAZ – AUTA Z USA 1.5 (silnik kalkulatora 1.4)

## Uruchomienie z odczytem stron aukcyjnych
1. Rozpakuj ZIP. Zainstaluj Python 3 (jeśli nie jest zainstalowany).
2. Windows: uruchom URUCHOM-WINDOWS.bat. Alternatywnie w terminalu w katalogu projektu wpisz `python server.py` (macOS/Linux: `python3 server.py`).
3. Otwórz http://127.0.0.1:8000. Pozostaw okno serwera otwarte.
4. Wklej link do oferty Copart, IAAI lub BidCars. Po około 650 ms nastąpi próba odczytu publicznej strony. Możesz powtórzyć ją przyciskiem. Dane potwierdź ręcznie.

Niektóre strony blokują automatyczny dostęp lub zwracają dane dopiero po wykonaniu JavaScript. W tej sytuacji aplikacja nie obchodzi blokady, informuje o braku odczytu i umożliwia ręczny wybór stanu. HTML uruchamiany bez serwera próbuje bezpośrednio pobrać stronę, co często jest blokowane przez CORS. Pełny odczyt na wszystkich aukcjach wymaga dostępu do autoryzowanego API. Bezpośrednie połączenie w środowisku testowym było niedostępne (DNS).

## Stawki
- USD 4,00 PLN, EUR 4,48 PLN: kursy firmowe do szacowania, nie kursy urzędowe.
- USA → Holandia: przekazany cennik stanowy, przy nieznanym stanie 2 000 USD; dla znanego stanu spoza tabeli wymagamy ręcznej stawki.
- Holandia → Polska 2 500 PLN, obsługa celna 300 USD, prowizja 3 000 PLN (przyjęta jako końcowa kwota), opcjonalna usługa usuwania danych 1 500 PLN.
- Usunięto pozostałe dopłaty, koszty dodatkowe, zaawansowane ustawienia celne oraz automatyczne kursy NBP.
- Cło 10%, VAT 21% jako orientacyjne założenie odprawy w Holandii. Oba pola edytowalne. Wartość celna szacowana od ceny zakupu, opłat aukcyjnych i przewozu do UE; VAT szacunkowo obejmuje cło i dostawę do Polski. Właściwe składniki podstawy, kurs urzędowy, stawki i klasyfikację musi potwierdzić agencja. Akcyza poza sumą.
- Suwak zmienia planowaną cenę zakupu w całej wycenie, wraz z opłatami aukcyjnymi i podatkami. W trybie budżetu suwak jest ukryty, by nie zakłócać limitu. Nie służy do deklarowania niższej wartości celnej przy tej samej rzeczywistej cenie.
- Opłaty aukcyjne szacowane z progów publicznych, sprawdzonych 26.11.2026: Copart Preferred Pricing (licencjonowany, salvage, secured, live), IAAI standard vehicle (standardowy cennik z SCA Help Center, aktualizacja 02.11.2026, live; dopłata EH&S 25 USD orientacyjna). Cennik IAAI nie został bezpośrednio odczytany ze strony IAA. Nie naliczamy dodatkowej prowizji SCA. Konta, dokumenty, płatności, kary i opłaty specjalne mogą zmienić wynik. Pole ręcznej stawki zastępuje cały automat. Źródła w config.js.

## Kod i testy
`src/config.js`: stawki; `src/engine.js`: obliczenia; `src/auction.js`: rozpoznanie URL; `src/ui.js`: interfejs; `server.py`: serwer i parser HTML. `python build.py` składa plik kalkulator.html. `node test.js` (Node.js) i `python -m unittest test_server.py` uruchamiają testy. Serwer wyłącznie lokalny, nie jest wdrożeniem produkcyjnym. Historia zapisywana lokalnie w przeglądarce; nie ma logowania.

Instrukcja publikacji: START-STRONA-WWW.md.
