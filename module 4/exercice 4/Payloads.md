L'analyse a révélé la présence de deux failles critiques : une **Inclusion de Fichiers Locaux (LFI)** et une **Falsification de Requête Côté Serveur (SSRF)**.

L'approche a consisté à :
1.  **Comprendre** la fonctionnalité attendue de l'application —> récupérer le contenu d'une URL).
2.  **Émettre des hypothèses** —> sur les déviations de sécurité possibles (lecture de fichiers locaux, requêtes vers des services internes).
3.  **Tester** ces hypothèses —> à l'aide de charges utiles (payloads) spécifiques pour confirmer les vulnérabilités.

---

## Vulnérabilité n°1 : Inclusion de Fichiers Locaux (LFI - Local File Inclusion)

### **Définition**

Une vulnérabilité de type LFI se produit lorsque l'application utilise une entrée utilisateur pour construire le chemin d'un fichier à inclure ou à afficher, sans valider ou assainir correctement cette entrée. Cela permet à un attaquant de manipuler le chemin pour accéder à des fichiers arbitraires sur le système de fichiers du serveur.



La vulnérabilité a été confirmée en soumettant la charge utile suivante dans le champ "Enter URL:" :

```
file:///etc/passwd
```

**Résultat :** L'application a interprété le wrapper `file://` et, au lieu d'initier une requête réseau, a lu le fichier `/etc/passwd` sur le disque du serveur et en a affiché le contenu.

Le wrapper est un système de routage 
Quand un navigateur ou une application web voit une chaîne de caractères qui ressemble à une adresse, il regarde le tout début pour savoir comment il doit la traiter.
* http:// et https:// lui disent : "Utilise le protocole web. Va chercher cette ressource sur le réseau Internet."
* ftp:// lui dit : "Utilise le protocole de transfert de fichiers pour te connecter à un serveur de fichiers."
* file:// lui dit : "Stop. Ne sors pas sur le réseau. Ce que je te donne est un chemin vers un fichier qui se trouve sur le système de fichiers local."

En temps et en condition réelles La vulnérabilité se produit parce que le développeur a utilisé une fonction très puissante pour gérer les URL et que cette fonction, conçue pour comprendre plusieurs protocoles (http, ftp, file, etc.) n’a pas été restreinte ! 



Mais dans ce projet c’est le code lui même qui a une logique de traitement de fichier implémenté : 

if url.startswith('file:///'): …..

 file_path = url[7:] 
 if os.path.exists(file_path): 
    file_content = open(file_path, 'r').read() 






## Vulnérabilité n°2 : Falsification de Requête Côté Serveur (SSRF - Server-Side Request Forgery)

### **Définition**

Une vulnérabilité SSRF apparaît lorsqu'un attaquant peut forcer le serveur à effectuer des requêtes HTTP (ou autres protocoles) vers une destination choisie par l'attaquant. Le serveur agit comme un proxy involontaire.
. La fonctionnalité normale est de lui donner l'adresse d'un site web public. Une attaque SSRF consiste à le tromper en lui donnant :
* L'adresse d'un serveur sur le réseau interne de l'entreprise (ex: `http://192.168.1.10/admin`).
* Sa propre adresse (`localhost`), pour qu'il interagisse avec des services qui ne sont pas exposés sur Internet.

La vulnérabilité a été confirmée avec la charge utile :

```
http://localhost:5000/

```

**Résultat :** L'application a traité la requête sans générer d'erreur de connexion. Bien qu'aucun contenu sensible n'ait été affiché (on parle de **SSRF "aveugle"** ou "Blind SSRF"), le test prouve que le serveur a bien initié une connexion sur lui-même.


