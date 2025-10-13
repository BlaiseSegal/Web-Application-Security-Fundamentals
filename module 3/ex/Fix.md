Guide de Mitigation des Vulnérabilités XXE 

La protection contre les attaques XXE repose le principe de la configuration sécurisée du parseur XML pour qu'il refuse d'interpréter les composants dangereux d'un document, notamment les entités externes. 

Étant donné que la vulnérabilité ne vient pas du format XML lui-même, mais de la confiance aveugle qu'un parseur mal configuré accorde aux instructions (DTD) fournies par une source non fiable.


Stratégies de Mitigation

Règle n°1 : Désactiver le Traitement des DTD et des Entités Externes

La solution la plus robuste et universelle est de configurer le parseur XML pour qu'il désactive complètement ou restreigne le traitement des Définitions de Type de Document (DTD) et des entités externes. 

Par exemple en python : 

from lxml import etree

parser = etree.XMLParser(resolve_entities=False) 
xml_data = etree.fromstring(untrusted_xml_input, parser)


Mesures de Défense Complémentaires

1. Utiliser JSON : Si possible, privilégier des formats de sérialisation de données plus simples comme JSON, qui ne possèdent pas de mécanisme d'entités et ne sont donc pas vulnérables aux attaques XXE.
