# Scénarios d'exploitation

Voici deux scénarios dans lesquels cette vulnérabilité pourrait être exploitée :

## Scénario 1 : Le Vol de Cookie de Session (Session Hijacking)

**Objectif :** Voler le cookie de session d'un utilisateur pour usurper son identité.

**Méthode :**  
L'attaquant crée une URL piégée qui contient un payload XSS. Ce payload, au lieu d'afficher une alerte, envoie discrètement le `document.cookie` de la victime vers un serveur contrôlé par l'attaquant. Il diffuse ensuite ce lien via une campagne de phishing (e‑mail, message privé). Lorsqu'un utilisateur connecté clique sur le lien, son cookie de session est envoyé à l'attaquant, qui peut alors l'utiliser pour se connecter au compte de la victime.


---

## Scénario 2 : Le Phishing Ciblé (Credential Theft)

**Objectif :** Dérober l'identifiant et le mot de passe d'un utilisateur.

**Méthode :**  
L'attaquant utilise la faille XSS pour injecter du code JavaScript qui modifie l'apparence de la page légitime. Par exemple, le script peut afficher un faux formulaire de connexion très crédible par-dessus le vrai site, avec un message comme *"Votre session a expiré"*. La victime, étant sur le vrai nom de domaine, pense que le formulaire est légitime et y tape ses identifiants. Le script de l'attaquant les capture et les envoie sur son serveur.
