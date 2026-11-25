# Catalogo Libri Musica (`E:\Libri Musica`)

Catalogo locale con interfaccia web per gestire e tracciare i libri e le riviste musicali (incluso lo stato di caricamento su Gemini NotebookLM).

## Prerequisiti
* Python 3 con `flask` installato.

## Come si avvia
1. Clicca **AVVIA** dal Launcher (oppure esegui `avvia_catalogo.bat`).
2. Il server locale Flask (`server.py`) parte sulla porta **5055** e apre automaticamente nel browser l'indirizzo:
   `http://localhost:5055`
3. Per chiudere il server in background, termina il processo `python.exe` relativo a `server.py` (oppure chiudi la finestra del terminale).

## File principali
* `avvia_catalogo.bat` — Avvia il server e apre il browser.
* `server.py` — Backend Flask che legge e salva `database_libri.json`.
* `index.html` — Interfaccia web del catalogo.
* `database_libri.json` / `elenco_libri_riviste.csv` — Database dei titoli catalogati.
* `annulla_rinomina.py` — Script di utilità per ripristinare eventuali rinomine tramite `rename_log.json`.
* Sottocartelle raccolte: `Classic Rock/`, `Classifiche/`, `Monografie/`, `Storia/`, `Varie/`, `The Encyclopedia of Popular Music- Larkin, Colin/`.
