# Ogólne
Kod grafu reprezentującego połączenia jest w pliku ```graph.py```, realizacja grafa również zaweira funkcję pomocnicze
które są wykorzystywane przez algorytmy poszukiwania, np. ```min_cost_route``` która szuka najszybsze połączenie między
dwoma sąsiednimi(!) przystankami pod pewnymi warunkami.

Realizajca dodatkowych wykorzystanych przez mnie struktur danych znajduje się w pliku ```utilities.py```, wraz z dekoratorem
który przekształca surowe wyniki funkcji wyszukiwania do wymaganej w zadaniach postaci, dodatkowo oblicza czas wykonania algorytmów wyszukiwania.
# Zadanie 1
## Punkt a
Dijkstra został opracowany i w oparciu o kryterium czasu i o kryterium przesiadek.

## Punkt b, c
Realizaja A* znajduje się w odpowiednim pliku, wraz z ciężkim marszrutem do przetestowania.

## Punkt d
Nie do końca zrozumiałem jak miałbym zmodyfikować algorytm dla jego polepszenia, ale i tak działa bardzo dobrze,
tym bardziej że kryterium przesiadek w A* można kontrolować za pomocą parametru ```transfer_cost_multiplier``` grafu.

# Zadanie 2
## Punkt a, b
Domyślnie tabela Tabu jest ograniczona, ale można to ograniczenie usunąć podając bardzo duże wartości dla parametru ```tabu_table_size_multiplier```, np. 1000.
## Punkt c
Z instrukcji nie udało się wydedukować kryterium aspiracji dla danego zadania, a i tak ogólnie ten kryterium polega na
ocenie tego kroku który jest tabu w odróżnieniu od innych możliwych, co nie jest możliwe podczas działania algorytmu
gdzie krokiem jest poruszenie się od jednego przystanku do drugiego, dlatego zamieniłem aspirację na Tabu Tenure - każdemu 
krokowi jest przypisywana pewna wartość liczbowa, każdy raz gdy algorytm chcę zrobić Tabu krok, Tenure się dekrementuje o 1,
i kiedy osiąga 0, krok przestaje być Tabu.
## Punkt b
Znaleźnienie nowej trasy polega na wykorzystaniu Dijkstry z Tabu, chyba to można liczyć jako dobór strategii próbkowania sąsiedztwa.
