# Mesures de Protection et Correctifs de Sécurité


## 1. Correction de l'Injection SQL

La cause racine est la concaténation de données utilisateur dans la requête SQL.

* **Solution : Requêtes Préparées (Prepared Statements)**
    Il faut impérativement utiliser des **requêtes préparées** avec des **paramètres liés (bound parameters)**. Cela sépare la logique SQL (la requête) des données (fournies par l'utilisateur), rendant l'injection impossible.

* **Exemple (PHP/PDO) :**
    ```php
    // NE PAS FAIRE :
    // $query = "SELECT ... from users WHERE username='$username'";

    // FAIRE CECI :
    $stmt = $pdo->prepare("SELECT username, encrypted_pass FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $row = $stmt->fetch();
    ```

## 2. Correction du PHP Type Juggling

La cause racine est l'utilisation de l'opérateur de comparaison faible (`==`) sur une valeur qui peut devenir `false`.

* **Solution : Comparaison Stricte (Strict Comparison)**
    Utilisez toujours l'opérateur de comparaison stricte (`===`) qui vérifie à la fois la valeur et le type. `false === ""` est évalué à **FALSE**.

* **Exemple (PHP) :**
    ```php
    // NE PAS FAIRE :
    // return $password == $pass;

    // FAIRE CECI :
    return $password === $pass;
    ```
    De plus, il est bon de vérifier si `$password` est `false` avant même la comparaison.

  

## 3. Correction des Vulnérabilités Cryptographiques (Padding Oracle & Bit-Flipping)

Ces deux attaques sont possibles parce que le mode de chiffrement **AES-CBC** n'offre, par défaut, aucune garantie d'**intégrité**.

* **Solution Prioritaire : Utiliser un mode AEAD (Authenticated Encryption)**
    Il faut abandonner `AES-CBC` au profit d'un mode moderne qui intègre l'authentification, comme **AES-GCM** (Galois/Counter Mode). 
    GCM chiffre les données *et* génère une étiquette d'authentification (tag). 
    Si le ciphertext ou l'IV est modifié, le tag ne correspondra plus et le déchiffrement échouera avant même de vérifier le padding. 
    Cela tue l'Oracle et le Bit-Flipping d'un seul coup.

* **Solution Alternative (si CBC est imposé) : Encrypt-then-MAC**
    Si CBC doit être utilisé, il faut ajouter l'intégrité manuellement via un **HMAC (Hash-based Message Authentication Code)**.
    1.  **Chiffrer** les données.
    2.  **Calculer** un HMAC sur le **ciphertext** (et non le plaintext).
    3.  **Transmettre** `Ciphertext + HMAC`.
    4.  Côté serveur : D'abord, **vérifier** le HMAC. S'il est valide, et *seulement* s'il est valide, procéder au déchiffrement.


## 4. Bonnes Pratiques de Gestion des Clés

* **Ne jamais coder de clés en dur :** Les clés doivent être stockées dans des **variables d'environnement** ou un système de gestion des secrets.
* **Utiliser la bonne longueur de clé :** Assurez-vous que la longueur de la clé correspond à l'algorithme (16 octets pour AES-128).