# Prévention et Mitigations contre les Injections de Template Côté Serveur (SSTI)


La cause racine de cette vulnérabilité est la violation d'une règle sécurité informatique : ne jamais faire confiance aux entrées fournies par l'utilisateur.


L'attaque a été possible parce que l'application a pris une donnée fournie par l'utilisateur (notre payload) et l'a interprétée comme du code au lieu de la traiter comme une simple donnée textuelle. 


# Stratégie 1 : Ne Jamais Laisser l'Utilisateur Contrôler le Template

C'est l'erreur de conception la plus directe et la plus dangereuse. L'entrée de l'utilisateur ne doit jamais être concaténée ou formatée pour créer le template. Le template doit être une structure fixe, et les données utilisateur ne doivent être passées que comme des variables.


Exemple VULNÉRABLE :

from jinja2 import Template

//L'input de l'utilisateur (ex: "{{ 6*7 }}")
user_input = request.args.get('name')

//ERREUR : L'input de l'utilisateur fait partie de la chaîne du template ! Le template n’est pas fixe il ne va plus savoir distinguer les placeholder {{}} légitimes et initiaux des placeholders ajouté par un utilisateur malveillant {{}}

template_string = f"<h1>Bonjour {user_input} !</h1>"

//Le moteur de template exécutera donc ici l'input de l'utilisateur. Comme un placeholder légitimes
template = Template(template_string)
page_rendue = template.render()



Exemple SÉCURISÉ :

from jinja2 import Template

//L'input de l'utilisateur
user_input = request.args.get('name')

//BONNE PRATIQUE : Le template est fixe.
//La donnée utilisateur est passée comme une variable distincte. Le placeholder malveillant sera percu comme une donnée textuelle et non comme un placeholder du template ! Car le template est ici fixe 

template_string = "<h1>Bonjour {{ user_name }} !</h1>"
template = Template(template_string)

//Le moteur remplace la variable de manière sûre, sans l'interpréter.
page_rendue = template.render(user_name=user_input)


Stratégie 2 : Utiliser un Environnement "Sandboxé"

Même avec une conception sécurisée, il est vital de restreindre ce que le moteur de template a le droit de faire. C'est le principe du bac à sable (sandbox).
Un environnement "sandboxé" est un parc de jeu restreint et sécurisé pour le moteur de template.
Il lui est impossible d'accéder à des modules comme subprocess ou de naviguer dans les __subclasses__. Toute tentative de le faire lèvera une erreur de sécurité.




 Exemple de Sandbox avec Jinja2 :

Python

from jinja2.sandbox import SandboxedEnvironment

//Au lieu de 'Environment' ou 'Template', on utilise 'SandboxedEnvironment'.
env = SandboxedEnvironment()


// Le template est chargé dans cet environnement sécurisé
template = env.from_string("<h1>Bonjour {{ user_name }} !</h1>")
page_rendue = template.render(user_name=user_input)
Avec cet environnement, un payload comme {{ ''.__class__ }} échouera immédiatement, coupant l'attaque à la racine.


# Stratégie 3 : Valider et Assainir les Entrées Utilisateurs

Même si les autres défenses sont en place, il est toujours recommandé de valider les entrées en amont.
* Principe de la liste blanche (Whitelist) : Au lieu d'essayer de bloquer les caractères dangereux (liste noire), n'autorisez que les caractères attendus (liste blanche). Si un champ "nom" ne doit contenir que des lettres et des espaces, alors refusez tout caractère qui ne correspond pas à cette règle.
* Exemple : Pour un champ "nom", une règle pourrait être ^[a-zA-Z\s]*$. Tout ce qui ne correspond pas est rejeté.
