Le Scénario d'Attaque : Comment le Compte a-t-il été Vidé ?

Dans le cadre de notre application, l'attaque s'est déroulée en plusieurs étapes logiques, exploitant le mécanisme décrit ci-dessus.
1. Phase 1 : L'Authentification de la Victime La victime se connecte à l'application bancaire sur http://localhost:8080. Le serveur lui fournit un cookie de session, que le navigateur stocke précieusement. La victime est maintenant "authentifiée".
2. Phase 2 : Le Piège La victime, dans un autre onglet, visite une page web à l'apparence inoffensive (attack.html) préparée par un attaquant. Cette page peut contenir n'importe quoi
3. Phase 3 : L'Action Forgée Caché dans le code de la page attack.html, se trouve un formulaire invisible qui est une copie parfaite du formulaire de virement de l'application bancaire. Voir notre script fichier attack.html joint 

p.s : On a du étudier le code pour voir comment était structuré la requete légitime du server : Résultat de notre Reconnaissance 

* URL de l'action (action) : Le formulaire envoie les données à /transfer. Comme le serveur tourne sur http://localhost:8080, l'URL complète de l'action est http://localhost:8080/transfer.
* Méthode (method) : La méthode utilisée est  post, comme indiqué dans <form action="/transfer" method="post">.
* Nom du paramètre (name) : Le champ contenant le montant s'appelle amount, comme le montre <input type="number" id="amount" name="amount">. Nous savons  desormais exactement comment forger une requête que le serveur acceptera comme légitime et pré-remplissons  les données choisies avec la valeur de 1000$).


1. Phase 4 : L'Exécution Automatique Un script JavaScript, également présent sur la page attack.html, se déclenche dès le chargement de la page. Son unique rôle est de soumettre ce formulaire caché.
2. Phase 5 : La Complicité Involontaire du Navigateur Le navigateur de la victime reçoit l'ordre de soumettre le formulaire vers http://localhost:8080/transfer. En voyant la destination, il suit sa règle automatique celle de joindre tous les cookies qu'il détient pour ce même domaine pour pallier la dimension stateless des requetes http : il récupère le cookie de session associé à localhost:8080 et le joint à la requête.
3. Phase 6 : La Validation par le Serveur Le serveur de l'application bancaire reçoit une requête de virement. Il examine la requête, y trouve un cookie de session parfaitement valide et conclut que la demande est légitime. Il n'a aucun moyen de savoir que l'ordre initial provenait d'un site malveillant. Le virement est exécuté, et le solde du compte passe à 0$.



Pour Exécuter l'Attaque

1. on se connecte : on ouvre un onglet dans notre navigateur et allons sur http://localhost:8080. On est maintenant la "victime authentifiée". Notre solde est de 1000$.
2. On se rend sur le site web issu de notre fichier html en local (attack.html sur notre bureau). alors que le localhost:8080 est bien  simultanément en état de fonctionnement  
3. on retourne sur le premier onglet localhost:8080) et actualisons la page.
On voit que le  solde est  maintenant à 0$ ! 

L'attaque a réussi car le navigateur, en soumettant le formulaire depuis attack.html vers localhost:8080, a gentiment joint le "contexte de session" de la victime. Le serveur, ne voyant aucune protection, a cru que la requête était légitime !