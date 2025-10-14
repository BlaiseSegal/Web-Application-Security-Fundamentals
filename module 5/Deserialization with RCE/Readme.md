Exécution de Code à Distance par Désérialisation Insécurisée


1 La sérialisation


Imaginons que je construise une maison LEGO. Cette maison, c'est comme un objet en mémoire. Elle existe, elle est assemblée, mais elle ne peut pas quitter la table (l’ordinateur) sur laquelle je l’ai construite.

Maintenant, je veux l'envoyer à un ami qui habite loin. Je ne peux pas, la maison est trop fragile. J’ai deux solutions :
1. Prendre une photo (juste les données, l'apparence).
2. Démonter la sculpture pièce par pièce et écrire un manuel d'instructions très précis : "Prendre la brique rouge 2x4, la placer sur la plaque verte à la coordonnée X, Y..."


Cette deuxième option, le manuel d'instructions, c'est la sérialisation. 
Par la sérialisation (du terme série) j’ai converti un objet complexe (la maison) en un manuel d’instruction simple et transmissible (un texte sur papier).

Le manuel d'instructions, c'est mon flux (ou stream). c’est une séquence de données qui peut être lue ou écrite de manière continue. Comme un texte qui s'écrit dans un fichier, lettre par lettre, ou à l'eau qui coule dans un tuyau. Mon manuel c’est un "flux de texte".


* Pourquoi un flux ? Quel intérêt de la sérialisation ? Dans quel contexte ? 

    * Sauvegarder une partie de jeu vidéo : mon personnage avec son inventaire, ses points de vie, sa position, est un objet complexe. Quand je sauvegarde, le jeu sérialise cet objet dans un fichier. Et Quand  je retourne sur le jeu et charge la partie, le jeu lit le fichier et le désérialise pour reconstruire mon personnage à l'identique.

    * Envoyer des informations sur le web : Quand je me connecte à un site, le serveur doit peut-être envoyer les infos de mon profil à mon navigateur. Il va sérialiser l'objet "profil utilisateur" (en format JSON, par exemple) et l'envoyer sur le réseau. Mon navigateur le reçoit et l'utilise.

    * Mettre des données en cache : Si un calcul est très long à faire, on peut le faire une fois, sérialiser le résultat et le stocker. La prochaine fois, au lieu de tout recalculer, on récupère juste le résultat sérialisé et on le désérialise. C'est beaucoup plus rapide !


 la sérialisation, c'est le "mode d'emploi" pour reconstruire un objet. C'est essentiel dès qu'on veut stocker un objet pour plus tard ou l'envoyer ailleurs !


En terme plus technique La sérialisation est un processus qui consiste à convertir un objet en mémoire (une instance de classe, une structure de données) 
en un format de flux, tel qu'une chaîne de caractères ou une séquence d'octets. 

Ce processus permet la persistance de l'état de l'objet sur un support de stockage (fichier, base de données) ou sa transmission à travers un réseau. 

Et la désérialisation, c’est l'opération inverse : c’est à dire la reconstruction de l'objet original à partir de ce flux de données.


De nombreux langages de programmation fournissent des mécanismes natifs pour cette opération, comme pickle en Python



2 La Désérialisation Insécurisée


La vulnérabilité de désérialisation insécurisée survient lorsqu'une application désérialise des données provenant d'une source non fiable (par exemple, une entrée utilisateur, un cookie, un paramètre d'URL) sans validation préalable de leur intégrité et de leur contenu.

Le mécanisme d'exploitation repose souvent sur le concept de "gadgets". Un gadget est un morceau de code (une méthode ou une fonction) déjà présent dans le code de l'application ou dans ses bibliothèques dépendantes, qui peut être détourné à des fins malveillantes. L'attaquant enchaîne ces gadgets pour construire une "chaîne de gadgets" (gadget chain)

En effet les formats de sérialisation natifs ne se contentent pas de transporter des données passives ; 
ils transportent également la logique de reconstruction de l'objet impliquant souvent l’appel à des fonctions ou à des méthodes déjà présent dans le code de l'application ou dans ses bibliothèques dépendantes . 
Un attaquant peut ainsi forger une charge utile (payload) sérialisée qui, une fois désérialisée par l'application, instancie des objets inattendus et exécute des méthodes de manière implicite.



Ici, l’application FLASK va désérialiser dans un premier temps les données qu’on lui as donné via (pickle.loads).
Ensuite elle va prendre l'objet qui en résulte et le passer directement à une fonction qui exécute des commandes, comme os.system() …


Note : dans la réalité, nous aurions du vraisemblablement faire un payload plus complexe faisant appel à la méthode __reduce__() 
 L'exploit avec __reduce__() est la méthode "universelle" pour attaquer les failles de désérialisation pickle, car il exécute le code pendant la reconstruction de l'objet, ce qui fonctionne même si l'application ne fait rien de dangereux avec l'objet par la suite.  Ici nous n’avons même pas eu à utiliser ce dispositif en raison de la vulnérabilité forte de l’application qui a  executé notre commande APRES la désérialisation comme nous pouvons le voir dans app.py : 

def execute_command(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if process.returncode == 0:
            if output:
                return output.decode('utf-8')
            else:
                return "Command executed successfully"
        else:
            if error:
                return error.decode('utf-8')
            else:
                return "Error executing command"
    except Exception as e:
        pass  # Do nothing in case of exception

Or L'exploit avec __reduce__()  nous aurait permit d’exploiter la vulnérabilité PENDANT la désérialisation ce qui est mieux pour un attaquant .
la réussite d’un exploit ne devant en effet pas être tributaire de ce qu’une application fera  ou non de son objet APRES désérialisation .