Analyse de Vulnérabilité : Cross-Site Request Forgery (CSRF)

1. Le Concept : Qu'est-ce que le CSRF ?

Le CSRF (cross-site request forgery), ou "Falsification de Requête Intersite", est une attaque qui force un utilisateur authentifié à exécuter une action non désirée sur une application web. L'attaquant abuse de la relation de confiance qu'un site web a envers le navigateur de l'utilisateur.



'Analogie du Barman Amnésique

1. Un Web "Sans Mémoire" : Imaginez que chaque site web est un barman qui souffre d'amnésie. Chaque fois que vous lui parlez, il vous oublie. C'est ce qu'on appelle un protocole "stateless" (sans état). Pour passer une commande (faire une action), vous devriez prouver votre identité à chaque fois, ce qui est très fastidieux.
2. La Solution : Les Cookies (un tampon sur la main) : Pour régler ce problème, après votre première authentification (login), le serveur-barman vous applique un "tampon" unique sur la main. Ce tampon, c'est le cookie de session. Désormais, pour toute nouvelle commande, il vous suffit de montrer votre main. Le barman reconnaît le tampon et vous fait confiance.

Le Rôle Clé du Navigateur : 

Le travail fondamental du navigateur est de maintenir le contexte de votre navigation. Sans ce mécanisme, le web serait inutilisable. Imaginons que le navigateur est notre assistant qui se déplace voir le barman a notre place et que c’est lui qui a le tampon (le cookie de session a notre place) nous pouvons lui dire de se déplacer voir le barman a notre place et de montrer son poignet au barman comme cela nous pouvons rester a notre table 

1. Ce comportement est essentiel : pour toute requête vers un domaine le navigateur doit joindre tous les cookies qu'il détient pour ce même domaine. C'est automatique. Exemple légitime : On se connecte sur le site votredistributeur.com. Le serveur nous donne un cookie. Ensuite, on clique sur "Mon Panier". Pour que le site se souvienne de qui on est et affiche notre panier, le navigateur doit renvoyer le cookie reçu lors de la connexion. On n'a pas à se reconnecter à chaque clic. Le cookie est un palliatif des requete stateless. C’est automatique, le navigateur doit joindre tous les cookies qu'il détient pour ce même domaine La vulnérabilité CSRF naît de cette automaticité. Le navigateur ne se demande pas qui a donné l'ordre, il se contente de l'exécuter en présentant le bon cookie.


L'attaque par Cross-Site Request Forgery (CSRF) exploite la gestion de session standard des navigateurs web pour soumettre des requêtes non autorisées au nom d'un utilisateur authentifié. Son succès repose sur trois piliers :

- La Gestion de Session par Cookies

- L'Initiation d'une Requête Intersite 

- L'Exploitation de la Confiance Serveur-Navigateur 


Le navigateur, voyant que la requête est destinée a un domaine donné meme si cette requete n'a pas ete formulé par l'utilisateur lui meme suit sa procédure standard et y attache le cookie de session  de l'utilisateur 'qu'il détient pour ce domaine.

Le serveur  reçoit la requête. De son point de vue, elle est parfaitement légitime : elle est adressée au bon endpoint, utilise la bonne méthode HTTP, et surtout, contient un cookie de session valide qui identifie un utilisateur authentifié.

En l'absence d'une défense spécifique (comme un jeton anti-CSRF), le serveur n'a aucun moyen de distinguer cette requête forgée d'une requête légitime. Il fait confiance au cookie de session comme preuve d'intention de l'utilisateur et exécute l'action demandée.

l'attaque CSRF réussit parce que le serveur valide l'identité de l'utilisateur via le cookie de session, mais ne vérifie pas l'origine de la requête elle-même. Il fait implicitement confiance au navigateur pour n'envoyer que des requêtes initiées volontairement par l'utilisateur depuis les pages de l'application, une confiance que l'attaquant peut aisément abuser.
