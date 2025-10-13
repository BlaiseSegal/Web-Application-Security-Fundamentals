🛡️ Pour protéger une application web contre les vulnérabilités XSS, il convient par principe ne jamais faire confiance aux données provenant de l'utilisateur.

### Mesure principale : L'encodage des sorties (Output Encoding)

toute donnée fournie par un utilisateur doit être encodée avant
d'être insérée dans une page HTML.

L'encodage consiste à remplacer les caractères ayant une signification
spéciale en HTML (comme \<, \>, ", ') par leurs équivalents inoffensifs
(entités HTML).

**Exemple :** Si un utilisateur entre le payload :
`<img src=x onerror="alert(1)">`\
Le serveur doit le transformer en :
`&lt;img src=x onerror=&quot;alert(1)&quot;&gt;`

Ainsi, le navigateur affichera cette chaîne comme un simple texte au
lieu de l'interpréter comme une balise HTML et d'exécuter le code.

### Mesures complémentaires

-   **Validation des entrées (Input Validation)** : Avant même de
    stocker ou d'utiliser une donnée, il faut la valider. La meilleure
    approche est la liste blanche (*whitelist*), qui n'autorise qu'un
    ensemble de caractères connus et sûrs (par ex., a-z, 0-9 pour un nom
    d'utilisateur) et rejette tout le reste. C'est bien plus efficace
    que la liste noire (*blacklist*) qui tente, souvent sans succès, de
    bloquer les caractères dangereux.

-   **Content Security Policy (CSP)** : Il s'agit d'un en-tête HTTP que
    le serveur envoie au navigateur pour lui dicter des règles de
    sécurité strictes. Une CSP bien configurée peut, par exemple,
    interdire tous les scripts "inline" (comme notre `onerror`). Même si
    l'encodage des sorties échouait, la CSP agirait comme un dernier
    rempart et bloquerait l'attaque côté navigateur.
    
    ** Example : ** `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';`
    

-   **Configurer l'attribut HttpOnly sur les cookies** : Pour mitiger
    l'impact d'un vol de cookie, les cookies de session doivent être
    configurés avec l'attribut `HttpOnly`. Cela indique au navigateur
    que ce cookie ne doit pas être accessible via JavaScript
    (`document.cookie`), rendant le scénario de *Session Hijacking*
    beaucoup plus difficile.
