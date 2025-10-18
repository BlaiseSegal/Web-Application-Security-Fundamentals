## Scénarios d'Exploitation

### Scénario 1 : Vol d'Informations Sensibles (Cookies, Jetons)

Un attaquant pourrait utiliser cette chaîne de vulnérabilités pour déchiffrer le contenu des cookies d'autres utilisateurs s'il parvient à les intercepter (via XSS ou sniffing).

1.  L'attaquant obtient le cookie `ID` (ciphertext) et `token` (IV) d'une victime.
2.  Il utilise le **Padding Oracle** (Payload 2) pour déchiffrer le contenu du cookie `ID` octet par octet.
3.  L'attaquant extrait les informations sensibles contenues dans le cookie (par exemple, un identifiant utilisateur, un niveau de permission, ou même des informations personnelles) sans jamais avoir besoin de la clé secrète du serveur.

### Scénario 2 : Escalade de Privilèges et Prise de Contrôle (Full Chained Attack)

Un attaquant sans aucun compte peut devenir administrateur.

1.  L'attaquant audite le code et découvre la **clé tronquée**.
2.  Il utilise la clé pour forger un mot de passe chiffré pour l'utilisateur de son choix.
3.  Il utilise l'**Injection SQL** (Payload 1) pour se connecter en tant que cet utilisateur (ex: "guest") et obtenir des cookies valides (`ID` et `token`).
4.  Il utilise le **Padding Oracle** (Payload 2) pour déchiffrer le cookie `ID` et confirmer le `Plaintext` ("guest").
5.  Il utilise l'attaque **CBC Bit-Flipping** (Payload 3) pour forger un nouveau `token` (IV) qui transforme "guest" en "admin".
6.  L'attaquant envoie ce cookie `token` forgé au serveur et obtient un accès administratif complet à l'application.


