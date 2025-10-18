## Payloads Utilisés

### Payload 1 : Contournement d'Authentification (SQLi + Type Juggling)

C'est le payload principal pour obtenir l'accès initial et générer les cookies de session.

* **Type :** Injection SQL + PHP Type Juggling
* **Payload (Champs du formulaire) :**
    * `username`: `' UNION SELECT 'guest', 'a' -- `
    * `password`: `(vide)`
* **Objectif :**
    1.  L'injection SQL force la requête `SELECT` à retourner une ligne, donc `$row` devient `true`.
    2.  La valeur `'a'` pour `encrypted_pass` est invalide, `openssl_decrypt` retourne `false`.
    3.  Le mot de passe vide fait que `login()` évalue `false == ""` à `true`.
    4.  La condition `if ($row && login(...))` est `true && true`.
    5.  L'application appelle `get_identity()` et nous donne les cookies `ID` et `token` pour "guest".


### Payload 2 : Attaque par Padding Oracle (Méthodologie de déchiffrement)

Il ne s'agit pas d'un payload unique, mais d'un processus pour déchiffrer le cookie `ID` (valant `pad(b"guest", 16)`).

* **Type :** Forgery d'IV (Byte-by-Byte Guessing)
* **Pseudo-Payload :**
    ```python
    # Pour chaque octet (byte_index) de 15 à 0:
    #   Pour chaque supposition (guess) de 0 à 255:
    #     1. Créer un forged_iv (cookie 'token')
    #     2. Y insérer la 'guess' à la position byte_index
    #     3. Ajuster les octets suivants pour créer un padding valide
    #     4. Envoyer (forged_iv, original_ciphertext) au serveur
    #     5. Si le serveur ne renvoie PAS "ERROR!":
    #          -> La supposition est correcte.
    #          -> Calculer l'octet du Plaintext.
    #          -> Passer à l'octet suivant.
    ```
* **Objectif :** Découvrir le `Plaintext` original (`"guest"`) caché dans le cookie `ID`.

### Payload 3 : CBC Bit-Flipping (Escalade de Privilèges)

Ce payload final est un `token` (IV) entièrement forgé, conçu pour changer le `Plaintext` déchiffré de `"guest"` à `"admin"`.

* **Type :** Forgery d'IV (Bit-Flipping)
* **Payload (Logique de calcul) :**
    ```python
    # 1. Obtenir l'IV original (cookie 'token' de 'guest')
    iv_original = base64.b64decode(token_b64)

    # 2. Définir le Plaintext original (découvert via Payload 2)
    p_guest = pad(b"guest", 16)

    # 3. Définir le Plaintext désiré
    p_admin = pad(b"admin", 16)

    # 4. Calculer l'IV forgé (le nouveau cookie 'token')
    iv_forged = bytes(a ^ b ^ c for a,b,c in zip(p_guest, iv_original, p_admin))
    iv_forged_b64 = base64.b64encode(iv_forged).decode()
    ```
* **Objectif :** Envoyer le couple `(iv_forged, original_ciphertext)` au serveur. Le serveur calculera `Decrypt(original_ciphertext) ⊕ iv_forged`, ce qui résultera en `pad(b"admin", 16)`, accordant une session administrateur.