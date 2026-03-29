<!--
Sceneqora — Ticket Template v1

But :
- un ticket = un objectif principal ;
- un ticket = une frontière nette ;
- un ticket = un livrable visible ;
- exécutable localement par Codex ;
- reviewable proprement par GPT 5.4.

Ce fichier est le template des tickets que Codex va créer sous supervision de GPT 5.4.
-->

# Titre
<!-- Exemple : Etape 1_001 - CLI minimale d’ingestion vidéo -->

## Identifiant
<!-- Exemple : etape_1_001_cli_ingestion_video -->

## Etape
<!-- Exemple : Etape 1 - Socle d’ingestion et contrats initiaux -->

## Contexte / Problème
<!-- Pourquoi ce ticket existe. Quel manque concret adresse-t-on dans Sceneqora. -->

## Objectif
<!-- Résultat attendu, observable, testable, visible. -->

## Frontière du ticket
<!-- Expliquer très clairement la frontière : ce qu’on veut rendre possible à la fin du ticket. -->

## Périmètre
<!-- Ce qui est explicitement inclus dans ce ticket. -->

## Hors périmètre
<!-- Ce qu’on ne fait pas ici, même si proche et tentant. -->

## Références
<!-- guide.md, docs d’étape, tickets précédents, modules existants, notes de review. -->

## Dépendances / Pré-requis
<!-- Tickets précédents, artefacts nécessaires, dépendances locales, binaire FFmpeg, modèles, etc. -->

## Livrable visible attendu
<!-- Décrire l’output visible du ticket : CLI fonctionnelle, manifeste JSON, fichier ASS, clip exporté, etc. -->

## Exigences fonctionnelles
- [ ] Exigence 1
- [ ] Exigence 2
- [ ] Exigence 3

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d’élargissement de scope
- Pas de refactor transverse non justifié
- Si intégration réelle : prévoir aussi un test live ciblé hors `make check`
<!-- Ajouter ici les contraintes spécifiques du ticket -->

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Artefact(s) généré(s) localement
- [ ] Documentation minimale si nécessaire
- [ ] Notebook de validation si demandé par l’étape

## Contrats / Interfaces touchés
<!-- Types, schémas JSON, signatures, chemins de fichiers, conventions de nommage, etc. -->

## Definition of Done (DoD)
- [ ] Le comportement attendu est implémenté
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests liés au ticket sont ajoutés ou mis à jour
- [ ] Les artefacts attendus sont générés et vérifiés
- [ ] Si le ticket touche une intégration réelle, un test live ciblé hors `make check` est exécuté et documenté
- [ ] `pytest` est vert sur le périmètre du ticket
- [ ] `ruff check` est vert sur le périmètre du ticket
- [ ] `mypy` est vert sur le périmètre du ticket si le module est typé
- [ ] `make check` est exécuté en fin de ticket et est vert
- [ ] Le retour Codex est prêt pour review GPT 5.4

## Stratégie d’implémentation
<!-- Décomposer en 3 à 6 étapes concrètes maximum. -->

1. 
2. 
3. 

## Cas limites
<!-- Lister au moins 3 cas limites concrets à couvrir ou vérifier. -->

1. 
2. 
3. 

## Critères de vérification
<!-- Commandes ou checks manuels attendus. Adapter au ticket. -->

```bash
pytest
ruff check .
make check
```

<!-- Si intégration réelle : ajouter ici le test live attendu hors `make check`. -->

## Validation manuelle attendue
<!-- Ce qu’il faut inspecter visuellement ou fonctionnellement : manifeste, transcript, sous-titres, clip exporté, logs, etc. -->

## Risques / Points d’attention
<!-- Compat, dette, hypothèses, dépendances externes, coût CPU/GPU, variabilité média, etc. -->

## Retour Codex attendu
<!-- Rappel du format de retour demandé à Codex. -->

- fichiers ajoutés / modifiés
- ce que le ticket apporte
- frontière respectée ou non
- validations exécutées
- état git
- points ouverts
- prochain move logique

## Notes d’implémentation
<!-- Section à compléter pendant ou après exécution si utile. -->
