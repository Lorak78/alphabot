# alphabot
Questo repository contiene tutto il codice e il materiale per alphabot.
## Versioni
Le versioni degli esercizi applicate sull'alphabot sono numerate in ordine, attualmente, l'ultima è l'8.

Mentre le cartelle *login* e *login_token* servono per testare le funzionalità **non** dell'alphabot (quindi token, cookie, ecc..)


## Esecuzione
Per l'esecuzione, bisogna avere la cartella col programma che si vuole eseguire sia sull'alphabot che sul proprio pc (questo **solo** se la versione è minore di 5, altrimenti basta averla solo sull'alphabot).
Poi bisogna assicurarsi di aver connesso l'alphabot e il proprio pc alla stessa rete, e stabilire una connessione **SSH** con l'alphabot, ad esempio tramite *[PuTTY](https://www.putty.org/)*.
A questo punto in base alla versione, si esegue in 2 modi:
#### 1. Versione 4 o minore
   Lanciare dal terminale SSH il file *server.py* e dal terminale del proprio pc il file *client.py*.
#### 2. Versione 5 o maggiore
   Lanciare dal terminale SSH il file *app.py* e dal proprio pc aprire un browser, per fare l'accesso al sito.

#### Attenzione
Verificare che l'ip assegnato nei file *app.py*, *server.py* e *client.py* siano corretti, altrimenti non può funzionare l'accesso. 
