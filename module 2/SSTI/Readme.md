Injection de Template Côté Serveur (SSTI)

l'application web fournie possède la faille critique suivante :  Injection de Template Côté Serveur (Server-Side Template Injection - SSTI) .


Qu'est-ce qu'une SSTI ?

Une injection de template côté serveur est une faille de sécurité qui se produit lorsqu'une application utilise un moteur de template pour générer du contenu dynamique (comme des e-mails ou des pages web personnalisé (comme avec le nom de l’utilisateur, etc) 
et que les entrées fournies par un utilisateur sont directement insérées dans ce template sans être correctement neutralisées.

Au lieu de simplement afficher le texte de l'utilisateur, le serveur l'interprète comme une partie du code du template lui-même. Cela permet à un attaquant d'exécuter des commandes qui n'étaient pas prévues, directement sur le serveur.


imaginons un site qui nous accueille avec le message : Bienvenue, {{ nom_utilisateur }} !.
* Usage normal : Si vous entrez « Blaise », le site affiche Bienvenue, Blaise !.
* Attaque SSTI : Si, au lieu de votre nom, vous entrez {{ 7*6 }}, le site vulnérable n'affichera pas le texte, mais calculera le résultat et affichera Bienvenue, 42 !.

L'attaquant a réussi à faire exécuter une instruction au serveur, là où il aurait dû simplement afficher une donnée.


Pourquoi est-ce si Dangereux ? (SSTI vs. XSS)

La criticité de cette faille vient du fait qu'elle s'exécute côté serveur et non côté navigateur.
pour XSS : L'attaque s'exécute dans le navigateur de la victime. Le pirate s'attaque a un  utilisateur du site, mais pas au site lui-même.

Pour SSTI L'attaque s'exécute directement sur le serveur. Le pirate ne s'attaque plus à un simple utilisateur, il prend le contrôle de l'infrastructure elle-même.
C'est pour cela que la SSTI est infiniment plus critique.



Une fois la faille SSTI confirmée, un attaquant peut potentiellement :
* Lire des fichiers sensibles du serveur (/etc/passwd, fichiers de configuration).