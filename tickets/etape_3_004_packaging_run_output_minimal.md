# Titre
Etape 3_004 - Packaging run output minimal

## Identifiant
etape_3_004_packaging_run_output_minimal

## Etape
Etape 3 - Assemblage pipeline local minimal

## Contexte / Probleme
Sceneqora dispose maintenant :
- d'un pipeline local minimal capable de produire un dossier de sortie exploitable ;
- d'une validation structurelle minimale des outputs produits ;
- d'un support minimal du cas vocal reel pour verifier que les artefacts textuels utiles ne restent pas vides.

En revanche, rien ne permet encore de packager simplement les artefacts d'un run local dans un conteneur unique facile a partager, archiver ou conserver.

Avant d'ouvrir du stockage distant, du packaging riche, de la signature ou du versioning avance, il faut poser une capacite strictement minimale, explicable et locale :
- lire un dossier de sortie de pipeline ;
- verifier minimalement les artefacts attendus ;
- produire une archive locale unique et standard ;
- remonter une sortie visible simple et stable.

## Objectif
Introduire une brique strictement minimale permettant de packager localement les artefacts d'un run du pipeline dans une archive unique facile a exploiter et archiver.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- la lecture d'un dossier de sortie local produit par le pipeline ;
- une verification minimale des artefacts attendus :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- un packaging minimal de ces artefacts dans une archive locale unique ;
- un format d'archive simple et standard, de preference `.zip` ;
- une commande CLI simple dediee ;
- une sortie visible stable confirmant au minimum :
  - `output_dir`
  - `archive_path`
  - `included_files`
  - `status`
- des tests deterministes ;
- un test live cible hors `make check`.

Le ticket s'arrete a un packaging local minimal, mono-run, dans une archive standard unique.
Il n'ouvre ni upload distant, ni chiffrement, ni packaging distribue, ni manifest riche.

## Perimetre
Inclus :
- lecture d'un dossier de sortie local produit par le pipeline ;
- verification minimale des 4 artefacts attendus :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- creation d'une archive locale unique contenant ces artefacts ;
- format d'archive simple et standard, de preference `.zip` ;
- ajout d'une commande CLI simple dediee ;
- sortie visible stable confirmant au minimum :
  - `output_dir`
  - `archive_path`
  - `included_files`
  - `status`
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- upload distant
- stockage cloud
- chiffrement
- signature
- versioning riche
- manifest metier complexe
- compression avancee configurable
- reporting riche
- UI
- batch
- packaging multi-run
- orchestration distribuee

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_3_001_assemblage_pipeline_local_minimal.md`
- `tickets/etape_3_002_validation_output_pipeline_minimale.md`
- `tickets/etape_3_003_support_entree_parole_reelle_minimale.md`

## Dependances / Pre-requis
- Etape 3 deja ouverte avec un pipeline local minimal et un dossier de sortie exploitable
- un dossier de sortie reel du pipeline doit etre disponible pour le test live cible
- aucun service externe ne doit etre requis
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI du type :

```bash
python -m sceneqora.cli.main package-run-output /chemin/output_dir /chemin/archive.zip
```

Cette commande doit :
- creer reellement une archive locale ;
- inclure les artefacts attendus ;
- afficher une sortie JSON stable avec :
  - `output_dir`
  - `archive_path`
  - `included_files`
  - `status`

## Convention explicite
- l'archive contient exactement les artefacts attendus du run :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- le statut global reste simple et coherent, par exemple `completed` ou `invalid`
- l'archive cible est ecrasee explicitement si elle existe deja

## Exigences fonctionnelles
- [ ] Un dossier de sortie de pipeline peut etre package localement
- [ ] Les 4 artefacts attendus sont inclus dans l'archive
- [ ] La CLI expose une commande simple dediee
- [ ] La sortie visible est stable et testable
- [ ] Les tests restent deterministes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas de surconstruction
- Pas d'elargissement de scope
- Archive standard locale
- Pas de dependance a des services externes
- Si l'archive cible existe deja, le comportement doit rester simple et explicite

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Archive locale produite
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale de packaging local de run
- commande CLI `package-run-output`
- format JSON stable de sortie de packaging
- convention de contenu exact de l'archive `.zip`

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] L'archive attendue est produite et verifiee
- [ ] Le test live cible hors `make check` est execute et documente
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Definir la convention minimale du packaging local et le contenu exact de l'archive
2. Ajouter une brique locale de packaging qui verifie les artefacts attendus avant archivage
3. Ajouter la commande `package-run-output` et la sortie JSON stable
4. Ajouter les tests deterministes sur les cas valides et invalides
5. Executer et documenter le test live cible sur un vrai dossier de sortie local

## Cas limites
1. Le dossier source n'existe pas
2. Un artefact attendu est absent
3. L'archive ne peut pas etre creee
4. L'archive existe deja
5. Le dossier source est incomplet
6. L'archive produite ne contient pas tous les fichiers attendus

## Critères de vérification
```bash
pytest
ruff check .
mypy src
make check
python -m sceneqora.cli.main --help
```

Test live cible hors `make check` :

```bash
python -m sceneqora.cli.main package-run-output /chemin/output_dir /chemin/archive.zip
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Le test live cible doit s'appuyer sur un dossier de sortie local reel.

## Validation manuelle attendue
- verifier que la commande CLI lit bien un dossier de sortie de pipeline ;
- verifier que l'archive locale est reellement creee ;
- verifier que l'archive contient exactement les 4 artefacts attendus ;
- verifier que la sortie visible confirme au minimum le dossier source, l'archive cible, les fichiers inclus et le statut ;
- verifier que l'ecrasement explicite d'une archive existante reste simple et lisible ;
- verifier qu'il n'y a aucun glissement vers stockage distant, chiffrement, versioning riche ou packaging distribue.

## Risques / Points d'attention
- risque de glisser d'un packaging local simple vers un systeme de distribution trop riche ;
- risque d'introduire un manifest ou une structure d'archive trop complexe sans besoin ;
- risque de sur-construire la gestion des archives existantes ;
- attention a garder une archive standard unique, un contenu exact et un statut global simple.

## Retour Codex attendu
- fichiers ajoutes / modifies
- ce que le ticket apporte
- frontiere respectee ou non
- validations executees
- etat git
- points ouverts
- prochain move logique

## Notes d'implementation
- Ticket redige par Codex a partir du cadrage utilisateur, en attente de validation ou correction par GPT 5.4 avant implementation.
