# Rapport de Vulnérabilité

L'analyse a révélé une **chaîne de vulnérabilités critiques** qui, une fois combinées, permettent à un attaquant de contourner l'authentification et d'usurper l'identité d'un administrateur.

L'attaque se décompose en plusieurs phases :

1.  **Phase 1 : Reconnaissance et Hypothèse (Théorie AES-CBC)**
2.  **Phase 2 : Contournement de l'Authentification (SQLi + Type Juggling / Clé Tronquée)**
3.  **Phase 3 : Déchiffrement d'Information (Attaque par Padding Oracle)**
4.  **Phase 4 : Usurpation d'Identité (Attaque par CBC Bit-Flipping)**

---

## Phase 1 : Hypothèse

Avant d'attaquer, nous devons comprendre notre cible. L'observation initiale du trafic réseau a révélé deux cookies suspects : `token` et `ID`.

* `token` (décodé) : `716b636462000102030c0d0e0f08090a` (16 octets)
* `ID` (décodé) : `00000000000000000000000000000000` (16 octets)

La taille de **16 octets** (128 bits) est un indice d'un chiffrement par bloc, très probablement **AES**, est utilisé.

### 1. Le Chiffrement par Bloc : La Brique de Base

Imaginez un système de chiffrement ayant une contrainte : elle ne peut traiter que des morceaux de 16 octets à la fois. C'est ce qu'on appelle un **bloc**. L'algorithme **AES** (Advanced Encryption Standard) fonctionne comme ça : il prend un bloc de 16 octets de texte en clair et le transforme, via une clé secrète, en un bloc de 16 octets de texte chiffré (ciphertext).

### 2. Le Problème : Le Chiffrement "Naïf" (ECB)

Si nous avons un message long, nous le coupons en blocs. Si nous chiffrons chaque bloc séparément (mode **ECB - Electronic Codebook**), deux blocs identiques en clair (ex: "passwordpassword") produiront deux blocs chiffrés identiques. Cela crée des motifs qu'un attaquant peut analyser. C'est très dangereux.

### 3. La Solution : Le Mode CBC (Cipher Block Chaining)

Pour éviter les motifs, le mode **CBC** (Cipher Block Chaining) crée une réaction en chaîne, comme des dominos. Avant de chiffrer un bloc de texte en clair, on le "mélange" (via une opération **XOR**) avec le bloc de texte *chiffré* précédent.

* Bloc 2 (clair) est mélangé avec Bloc 1 (chiffré) avant d'être chiffré.
* Bloc 3 (clair) est mélangé avec Bloc 2 (chiffré) avant d'être chiffré.

Ainsi, même si le Bloc 2 et le Bloc 3 étaient identiques en clair, leurs versions chiffrées seront totalement différentes.

### 4. Le Vecteur d'Initialisation (IV) : Le Premier Domino

Comment chiffrer le *tout premier bloc* ? Il n'a pas de bloc précédent. Pour cela, nous créons un "faux" premier bloc : le **Vecteur d'Initialisation (IV)**. C'est un bloc de 16 octets, aléatoire et unique, qui n'est pas secret. Il est utilisé pour démarrer la chaîne.

### 5. Synthèse de l'Hypothèse

Revenons à nos cookies :
* Un cookie `token` de 16 octets.
* Un cookie `ID` de 16 octets.

L'hypothèse la plus probable est que l'application utilise **AES-CBC**.
* Le cookie `token` est le **Vecteur d'Initialisation (IV)**.
* Le cookie `ID` est le **premier bloc du Ciphertext**.

L'application les a simplement scindés en deux cookies. Cela confirme la surface d'attaque : le chiffrement CBC.

---

## Vulnérabilité Principale : Le Padding Oracle

La vulnérabilité centrale est un **Padding Oracle**. Lorsque nous avons manipulé le cookie `token` (l'IV) et l'avons envoyé avec le cookie `ID`, le serveur a répondu de deux façons :
* **Padding Valide :** La page s'est chargée.
* **Padding Invalide :** La page a renvoyé un message `ERROR!` (visible dans `test_identity()`).

Ce comportement binaire ("chaud/froid") est un oracle. Il nous permet de deviner, octet par octet, le contenu du cookie `ID` (le ciphertext) sans jamais connaître la clé, simplement en posant des milliers de questions au serveur.

---

## Vulnérabilités Secondaires (Vecteurs d'Activation)

Pour exploiter l'oracle, nous avons d'abord dû obtenir un couple `ID`/`token` valide en nous connectant. L'analyse du code (`index.php`) a révélé que la table `users` était vide, rendant un login normal impossible. Le contournement a nécessité les failles suivantes :

### 1. Injection SQL (SQLi)

La seule façon de faire en sorte que la requête `SELECT` renvoie une ligne (et que `$row` soit `true`) était d'injecter une clause `UNION`.
```sql
' UNION SELECT 'guest', 'nimp' -- '

Cela force la requête à retourner une ligne, satisfaisant la première partie de la condition if ($row && login(...)).


### 2. Vulnérabilité Authentification : Le "PHP Type Juggling"

La seconde partie de la condition est login($encrypted_pass, $password).

Notre injection SQL fournit une valeur invalide pour encrypted_pass (ex: 'nimp').
La fonction login() tente de le déchiffrer. openssl_decrypt échoue et retourne false.
La comparaison devient return false == $pass;. En laissant le champ mot de passe vide ($pass = ""), PHP évalue false == "" à TRUE.
En combinant l'Injection SQL (pour $row) et un mot de passe vide (pour le Type Juggling), l'authentification est contournée et le serveur nous octroie des cookies via get_identity() !


### 3. (Alternative) Gestion Inappropriée de la Clé de Chiffrement

Une autre méthode pour passer l'authentification était de découvrir la clé. L'audit de index.php a révélé :
define("SECRET_KEY", "this_is_key_you_do_not_know"); (32 octets)
define("METHOD", "aes-128-cbc"); (attend 16 octets)

La fonction openssl_encrypt de cette version de PHP tronque silencieusement la clé à 16 octets (this_is_key_you_). En connaissant cette clé, nous aurions pu forger un mot de passe chiffré valide pour notre injection SQL, sans avoir besoin du Type Juggling.


### 4. Absence Authentification du Ciphertext (CBC Bit-Flipping)

Enfin, une fois le cookie "guest" déchiffré grâce à l'Oracle, la vulnérabilité finale est l'absence de vérification d'intégrité. Le mode CBC seul est malléable. Un attaquant peut "flipper" des bits dans l'IV (le cookie token) pour contrôler le Plaintext qui sera déchiffré par le serveur.

cette technique qui a été utilisée pour forger un token qui change le Plaintext déchiffré de "guest" à "admin".

'IV_forgé = Plaintext_original ("guest") ⊕ IV_original ⊕ Plaintext_désiré ("admin")'

