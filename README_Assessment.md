# Project Evaluator

Conţinutul repository-ului:

- environment/          - engine-ul jocului 
- replays/              - folder cu rezultatele rularii botului (fisiere tip *.hlt) - (se genereaza automat la rulare)
- bots/                 - folder cu botii pusi la dispozitie de echipa de PA
- run.py                - scriptul de evaluare
- halite-resources.zip  - arhivă cu conținutul acestui repository
- README.md             - acest fisier


Prerequisites
===============

Pentru rularea scriptului de evaluare aveți nevoie de Python (>= 3.6).
Scriptul a fost testat pe o masina de Linux de 64 bits.
    

Testare
===============

Scriptul va realiza urmatorii pasi inainte de executia propriu-zisa:

- va incerca sa compileze engine-ul jocului daca executabilul (halite) nu se afla in path
- va incerca sa ruleze "make" pentru a re-compila botul daca descopera un fisier de tip Makefile in path 
- va sterge log-urile ramase de la executiile precedente

Important: Folositi versiunea engine-ului din acest repo (folderul environment/).
Spre deosebire de engine-ul din competitia originala am facut cateva modificari minore pentru
ca fisierele generate de logging sa ofere mai multe informatii. Scriptul acesta se bazeaza 
pe modificarile respective.

Example rulare:

C++ Bot:

    python ./run.py --cmd "./MyBot" --round 2 

Java Bot:

    python ./run.py --cmd "java MyBot" --round 2 --visualizer "firefox"

Python:

    python ./run.py --cmd "python3 MyBot.py" --round 2 --visualizer "google-chrome-stable"
    
Arguments

    --cmd        Comanda de execuție pentru bot (trebuie sa fie validă pentru locația curentă)
    --round      (Optional) Indicele rundei (1, 2, 3, 4, 5), default 0 (le ruleaza pe toate)
    --clean      (Optional) Șterge fișierele de log/replays, apeleaza `make clean`
    --visualiser (Optional) Numele browser-ului in care sa fie afisate rezultatele fiecarui joc
    --logging    (Optional) Defineste cat de explicite (verbose) sunt mesajele de logging. Optiunile sunt: 
        - 'critical' (doar mesajele critice), 'info', 'debug' (most verbose) 
