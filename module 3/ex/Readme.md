Qu'est-ce qu'une vulnérabilité XXE ?

XXE est l'acronyme de "XML External Entity". Il s'agit d'une vulnérabilité de sécurité qui affecte les applications qui analysent (ou "parsent") des données au format XML provenant d'une source non fiable.


 le format XML a une fonctionnalité qui permet de définir des "entités", qui sont essentiellement des alias ou des raccourcis pour des données plus complexes. 

Certaines de ces entités peuvent être "externes", c'est-à-dire qu'elles peuvent demander au parseur XML d'aller chercher des données en dehors du document XML lui-même, par exemple dans un fichier local sur le serveur ou à une adresse réseau.

La vulnérabilité se produit lorsqu'un parseur XML mal configuré traite un document XML fourni par un attaquant, et suit aveuglément les instructions de l'entité externe.




la surface d'attaque est très large :


Contexte 1 : Les APIs Web (SOAP et REST)


C'est le cas d'usage le plus fréquent.
* APIs SOAP : C'est un protocole plus ancien mais encore extrêmement répandu dans les systèmes d'entreprise (banques, assurances, systèmes gouvernementaux, télécommunications). Une API SOAP communique exclusivement en XML. Chaque requête envoyée à un service SOAP est un document XML. Si le serveur qui reçoit cette requête est mal configuré, il est vulnérable.
* APIs REST : Bien que le JSON soit plus populaire aujourd'hui pour les nouvelles APIs REST, beaucoup d'entre elles supportent encore le XML pour des raisons de compatibilité. Un attaquant peut simplement changer l'en-tête de sa requête (Content-Type: application/xml) et envoyer un payload XXE. Si le développeur n'a pas sécurisé ce point d'entrée "secondaire", l'attaque réussit.


Contexte 2 : Le Téléchargement de Fichiers (Upload)

C'est un vecteur d'attaque très courant et souvent sous-estimé. De nombreux formats de fichiers que nous utilisons tous les jours sont en réalité des archives (des .zip) contenant des fichiers XML.

* Documents bureautiques : Les formats .docx (Word), .xlsx (Excel), ou .pptx (PowerPoint) sont des collections de fichiers XML. Si vous téléchargez un .docx sur un site qui doit en extraire le texte ou les images, le serveur va devoir parser ces fichiers XML.

* Images vectorielles : Le format .svg est entièrement basé sur du XML. Si un site vous permet de télécharger un avatar en SVG et le traite côté serveur (par exemple pour le redimensionner), son parseur XML est exposé.

* Autres : Fichiers de configuration, exports de données, documents PDF (qui peuvent aussi embarquer du XML), etc.



Scenario 

* Exfiltration de données (vol de fichiers) : C'est le cas le plus classique et celui de votre exercice. Un attaquant peut lire des fichiers sensibles sur le serveur, comme des fichiers de configuration, le code source de l'application, des clés privées, ou le fameux fichier  /etc/passwd.

* Server-Side Request Forgery (SSRF) : L'attaquant peut forcer le serveur à effectuer des requêtes réseau en son nom. Cela peut lui permettre de scanner le réseau interne de l'entreprise, d'accéder à des services non exposés sur Internet ou d'interagir avec des services cloud internes.

* Déni de Service (DoS) : Des attaques XXE spécifiques, comme la "Billion Laughs Attack", peuvent être utilisées pour surcharger le parseur XML, consommant toute la mémoire ou le processeur du serveur jusqu'à le faire planter.
