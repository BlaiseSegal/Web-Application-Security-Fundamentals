Stratégies de Correction pour la Vulnérabilité de Désérialisation Insécurisée


De facon liminaire, il ne faut jamais faire confiance aux données provenant d'une source non contrôlée.
Ici l'application traite une chaîne de caractères fournie par l'utilisateur comme un objet de confiance à reconstruire, ce qui donne à ce même utilisateur le pouvoir d'exécuter du code..

1. Utiliser un Format de Données Sûr

La méthode la plus robuste pour éradiquer cette faille est de remplacer le format de sérialisation par un format conçu uniquement pour représenter des données.

Recommandation : Utilisation de JSON (JavaScript Object Notation)

JSON est un format de sérialisation de données pures. Il ne peut décrire que des structures de données (objets, listes, chaînes, nombres, booléens). Il n'a aucun mécanisme pour spécifier l'exécution de fonctions ou la reconstruction d'objets complexes. La désérialisation d'une chaîne JSON ne peut, par conception, déclencher une exécution de code.


2. La Vérification d'Intégrité

Utiliser un HMAC (Hash-based Message Authentication Code).

Quand le serveur sérialise un objet, il calcule une signature (un hash) de l'objet sérialisé en utilisant une clé secrète connue de lui seul.

Il envoie l'objet sérialisé et sa signature au client.

Quand le client renvoie les données, le serveur recalcule la signature des données reçues avec sa clé secrète.

Si la signature calculée correspond à celle qui a été envoyée, les données sont intègres et fiables. Si elles ne correspondent pas, cela signifie que les données ont été modifiées, et elles doivent être rejetées avant toute tentative de désérialisation.



