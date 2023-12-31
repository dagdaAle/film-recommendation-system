# Progetto di Raccomandazione Film

## Introduzione
Il progetto di raccomandazione film è una piattaforma interattiva progettata per suggerire film agli utenti in base alle loro preferenze. L'obiettivo principale del progetto è migliorare l'esperienza degli utenti nell'esplorazione di opzioni cinematografiche, guidandoli verso scoperte che si allineano ai loro gusti e interessi.

La piattaforma utilizza tecnologie moderne e tecniche di analisi dati avanzate, con un cuore basato su un algoritmo di machine learning che si basa sull'analisi testuale con TF-IDF.

## Tecnologia di Machine Learning Utilizzata
La componente centrale del sistema di raccomandazione è l'analisi testuale basata su TF-IDF, una tecnica popolare nel campo del machine learning e del natural language processing.

### Analisi Testuale con TF-IDF
- **Descrizione**: TF-IDF sta per Term Frequency-Inverse Document Frequency. Questa tecnica quantifica l'importanza di una parola in un documento in un corpus. L'uso di TF-IDF consente al nostro sistema di identificare parole chiave significative nelle descrizioni dei film (overview) e di usarle per calcolare la similarità tra i vari film.
- **Implementazione**: Abbiamo implementato TF-IDF attraverso la libreria TfidfVectorizer di scikit-learn. Questo strumento converte l'overview dei film in vettori numerici, permettendoci di analizzare e confrontare il contenuto testuale in modo quantitativo.
- **Calcolo della Similarità**: Utilizziamo la similarità del coseno per misurare quanto due film siano simili basandoci sui loro vettori TF-IDF. Questo approccio ci permette di suggerire agli utenti film con contenuti simili a quello da loro scelto.

### Unione di Diverse Caratteristiche
Oltre all'overview, il nostro sistema integra altre informazioni come i generi, le parole chiave, i nomi degli attori principali e del regista. Questo arricchisce la rappresentazione di ogni film, consentendo al nostro modello di fare raccomandazioni più accurate e dettagliate.

## Processo di Raccomandazione
Il processo di raccomandazione inizia con la raccolta e la preparazione dei dati, seguito dal calcolo delle raccomandazioni.

### Raccolta dei Dati
- **Raccolta dei Dati**: I dati sui film sono stati raccolti da fonti affidabili e sono stati attentamente selezionati per garantire che includessero informazioni rilevanti e aggiornate.
- **Preprocessing**: Questo passaggio è fondamentale per trasformare i dati grezzi in un formato adatto per l'analisi. Include la pulizia dei dati, la rimozione delle informazioni non pertinenti e la loro standardizzazione.
- **Calcolo delle Raccomandazioni**: Il sistema prende in input il titolo di un film scelto dall'utente e calcola la similarità con altri film nel database usando l'algoritmo TF-IDF. I film più simili vengono poi selezionati e presentati all'utente come raccomandazioni.

## Tecnologie Utilizzate
Il progetto utilizza una varietà di tecnologie e librerie, tra cui Python per il backend, Flask come framework web, scikit-learn per l'analisi dei dati e HTML/CSS/JavaScript per il frontend. Queste tecnologie sono state scelte per la loro efficienza, flessibilità e la vasta comunità di supporto.

---

### Cos'è TF-IDF?
TF-IDF è una tecnica statistica utilizzata per valutare l'importanza di una parola in un documento, che fa parte di una collezione o corpus di documenti. È spesso utilizzata in task di ricerca di informazioni e data mining, specialmente nel contesto del Natural Language Processing (NLP). L'idea di base è identificare l'importanza relativa di una parola in un documento specifico rispetto a un insieme di documenti.

#### Componenti del TF-IDF
- **Term Frequency (TF)**: Indica la frequenza con cui una parola appare in un documento.
- **Inverse Document Frequency (IDF)**: Misura l'importanza di una parola in tutto il corpus.
- **Calcolo del Punteggio TF-IDF**: Il punteggio TF-IDF di una parola in un documento è il prodotto del suo TF e del suo IDF.

#### Applicazione nel Sistema di Raccomandazione
Nel contesto del nostro sistema di raccomandazione di film, il TF-IDF è utilizzato per convertire le descrizioni testuali (overview) dei film in vettori numerici. Ogni film diventa un vettore in uno spazio n-dimensionale, dove n è il numero di parole uniche nel corpus. Questi vettori vengono poi utilizzati per calcolare la similarità tra i film utilizzando metriche come la similarità del coseno.

#### La Similarità del Coseno
La Similarità del Coseno calcola il coseno dell'angolo tra due vettori nello spazio vettoriale. Il valore di questa similarità varia da -1 a 1, dove 1 indica che i due vettori sono identici, 0 indica che sono completamente indipendenti e -1 indica esattamente l'opposto.

#### Come si Calcola
- **Interpretazione nel Contesto dei Sistemi di Raccomandazione**: Nel caso di un sistema di raccomandazione basato su contenuti, come quello per i film, ogni film può essere rappresentato come un vettore di caratteristiche derivato dalle sue descrizioni tramite tecniche come TF-IDF. Quando un utente sceglie un film, il sistema calcola la Similarità del Coseno tra il vettore di questo film e i vettori di tutti gli altri film nel database. I film con la similarità del coseno più alta rispetto al film scelto vengono poi raccomandati.
