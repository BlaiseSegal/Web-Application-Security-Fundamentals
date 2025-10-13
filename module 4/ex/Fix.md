# Correctifs de Sécurité pour les Vulnérabilités LFI et SSRF


---

## ## Correction de la Vulnérabilité LFI

La faille LFI est due au fait que l'application permet de lire n'importe quel fichier sur le disque du serveur.

### Solution 1 : Interdiction Stricte 

La fonctionnalité permettant de lire des fichiers locaux via un paramètre d'URL est dangereuse et rarement justifiée.

Le bloc de code suivant doit être retiré :
```python
if url.startswith('file:///'):
    file_path = url[7:]
    if os.path.exists(file_path):
        file_content = open(file_path, 'r').read()
        # ... Reste du code d'affichage
```

### Solution 2 : Si la fonctionnalité est indispensable on peut songer à une Approche par Liste Blanche

on peut utiliser un identifiant et le mapper à un chemin de fichier sûr côté serveur.

**Exemple :**
Au lieu de demander `file:///pages/contact.html`, l'utilisateur demanderait `?page=contact`.

```python
ALLOWED_FILES = {
    'contact': '/var/www/safe_pages/contact.html',
    'about': '/var/www/safe_pages/about_us.html'
}

page_identifier = request.args.get('page')

if page_identifier in ALLOWED_FILES:
    safe_path = ALLOWED_FILES[page_identifier]
    file_content = open(safe_path, 'r').read()
else:
    return "Page non valide.", 403
```
Cette méthode empêche toute tentative de **Path Traversal** (`../`) car l'entrée de l'utilisateur n'est jamais utilisée pour construire le chemin du fichier.

---

## ## Correction de la Vulnérabilité SSRF

La faille SSRF permet de forcer le serveur à effectuer des requêtes vers des destinations arbitraires.

### Solution 1 : Approche par Liste Blanche d'Hôtes

- définir une **liste blanche (allow-list)** explicite des seuls domaines que notre application est autorisée à contacter. Toute autre destination sera rejetée.

```python
from urllib.parse import urlparse

ALLOWED_HOSTS = {'api.partner.com', 'static.example.org'}

url = request.args.get('url')
try:
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if hostname in ALLOWED_HOSTS:
        response = requests.get(url, timeout=5)
    else:
        return "Accès non autorisé à cette destination.", 403

except Exception as e:
    return "URL invalide.", 400
```
Cette méthode  bloquera `localhost`, les IP privées et les nouveaux domaines malveillants.

### Solution 2 : Blocage des Adresses IP Privées

Si la solution 1 par liste blanche est trop restrictive, une alternative est de bloquer les requêtes vers les adresses IP non publiques. C'est moins sûr car on pourra utiliser des techniques de contournement (comme du DNS rebinding)

---

on peut corriger le code, mais il faut aussi renforcer l'environnement d'exécution.
avec le principe du Moindre Privilège :
Le serveur web ne doit **jamais** s'exécuter avec le compte `root`. Il doit utiliser un compte de service dédié avec des permissions minimales (ex: `www-data`). Cela limite l'**impact** d'une LFI si elle venait à être exploitée.
