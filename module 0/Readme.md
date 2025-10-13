# Type de vulnérabilité : Cross‑Site Scripting (XSS)

La vulnérabilité identifiée sur ce site est une faille de type **XSS Réfléchi** (en anglais, *Reflected Cross‑Site Scripting*).

## Explication du mécanisme

Le Cross‑Site Scripting est une attaque par injection où un attaquant parvient à faire exécuter un script malveillant (généralement du JavaScript) par le navigateur d'une victime.

Dans le cas d'un **XSS Réfléchi**, l'attaque se déroule en deux temps :

1. L'attaquant injecte son code malveillant dans une requête envoyée au serveur web (par exemple via un paramètre dans l'URL ou un champ de formulaire).
2. Le serveur web, n'ayant pas de structure de controle et/ou n'encodant pas correctement cette entrée, la renvoie ("la réfléchit") telle quelle dans la page HTML qu'il sert au navigateur de la victime.

Le navigateur de la victime, recevant ce code d'un serveur en qui il a confiance, l'exécute sans se méfier. La vulnérabilité réside dans la manière dont le serveur gère et "réfléchit" une entrée utilisateur à un instant T.

## Pourquoi employer le terme 'Reflected' 'Reflechi' ?

Le terme "Réfléchi" (ou Reflected en anglais) est une analogie visuelle pour décrire précisément comment l'attaque fonctionne.

si on pense à un miroir. Il ne garde rien en mémoire ; il se contente de renvoyer instantanément l'image de ce qui se trouve en face de lui.

La charge utile n'est jamais stockée sur le serveur (dans une base de données, par exemple). Elle fait simplement un aller-retour rapide, "rebondissant" sur le serveur pour revenir s'exécuter dans le navigateur de la victime.

c'est la grande différence avec un XSS Stocké (Stored XSS), où la charge utile est d'abord sauvegardée par le serveur (comme un commentaire de blog) avant d'être servie plus tard à d'autres utilisateurs. Dans le cas du XSS Stocké, le serveur ne réfléchit pas, il "retient" et "sert" le poison.
