Scénarios d'Exploitation d'une RCE via Désérialisation


Scénario 1 : Vol d'Informations Confidentielles (Exfiltration de Données)

L'objectif de ce scénario est d'utiliser la capacité d'exécution de commandes pour lire des fichiers sensibles sur le serveur et en extraire les données.


Scénario 2 : Prise de Contrôle Totale du Serveur (Reverse Shell)

On ne se contente plus d'exécuter des commandes une par une. on force le serveur hôte à établir une connexion interactive vers notre propre machine obtenant ainsi un "shell" distant, nous donnant un contrôle total et persistant sur le serveur compromis.

a) on met sa machine en écoute sur un port spécifique (ex: nc -lvnp 9001).

b) on forge un payload qui, une fois exécuté sur le serveur, ordonne à ce dernier de se connecter à notre adresse IP et a notre port 


