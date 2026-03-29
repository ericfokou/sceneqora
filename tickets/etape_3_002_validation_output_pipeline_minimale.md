# Titre
Etape 3_002 - Validation output pipeline minimale

## Identifiant
etape_3_002_validation_output_pipeline_minimale

## Etape
Etape 3 - Assemblage pipeline local minimal

## Contexte / Probleme
Sceneqora dispose maintenant d'un pipeline local minimal capable de produire un dossier de sortie avec les artefacts attendus, mais aucune brique reelle ne permet encore de valider localement la presence et la coherence structurelle de ces artefacts.

Avant d'ouvrir une validation plus riche, du scoring qualite ou une logique de correction, il faut poser une capacite minimale, explicable et locale :
- lire un dossier de sortie produit par le pipeline ;
- verifier la presence des artefacts attendus ;
- verifier quelques proprietes structurelles simples ;
- remonter un statut global stable et lisible.

Cette brique doit rester strictement centree sur la validation locale minimale des outputs, sans glisser vers une evaluation semantique ou qualitative avancee.

## Objectif
Introduire une brique minimale de validation locale des artefacts produits par le pipeline afin de verifier leur presence et leur coherence structurelle simple, puis de remonter une synthese JSON stable.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une brique minimale de validation locale des outputs du pipeline ;
- la lecture d'un dossier de sortie local produit par `etape_3_001` ;
- la validation minimale des artefacts attendus :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- une verification de presence des fichiers ;
- une verification minimale qu'un fichier audio attendu n'est pas vide ;
- une verification que `transcript_segments.json` est un JSON valide ;
- une verification que ce JSON contient au minimum `segments` ;
- un calcul minimal de :
  - `segment_count`
  - `subtitle_count`
- une coherence minimale :
  - si `segments` est vide, un SRT vide est autorise
  - si `segments` n'est pas vide, un SRT non vide est attendu
- une commande CLI simple dediee a la validation ;
- une sortie visible stable confirmant au minimum :
  - `output_dir`
  - `audio_exists`
  - `transcript_exists`
  - `segments_exists`
  - `srt_exists`
  - `segment_count`
  - `subtitle_count`
  - `status`
- des tests deterministes ;
- un test live cible hors `make check`.

Le ticket s'arrete a une validation locale minimale, structurelle et de coherence simple.
Il n'ouvre ni scoring qualite avance, ni correction automatique, ni reporting riche.

## Perimetre
Inclus :
- lecture d'un dossier de sortie local produit par `etape_3_001` ;
- verification explicite des 4 artefacts attendus :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- verification de presence des fichiers ;
- verification minimale qu'un fichier audio attendu n'est pas vide ;
- verification que `transcript_segments.json` est un JSON valide ;
- verification que le JSON contient au minimum `segments` ;
- calcul minimal de :
  - `segment_count`
  - `subtitle_count`
- verification d'une coherence simple entre `segments` et `subtitles.srt` ;
- ajout d'une commande CLI simple dediee ;
- sortie visible stable confirmant au minimum :
  - `output_dir`
  - `audio_exists`
  - `transcript_exists`
  - `segments_exists`
  - `srt_exists`
  - `segment_count`
  - `subtitle_count`
  - `status`
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- scoring qualite avance
- metriques ML
- detection semantique
- correction automatique
- retry
- auto-reparation
- comparaison multi-run
- reporting riche
- dashboard
- UI
- batch
- pipeline distribue
- validation linguistique
- validation metier riche

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_3_001_assemblage_pipeline_local_minimal.md`

## Dependances / Pre-requis
- Etape 3 deja ouverte avec le pipeline local minimal
- un dossier de sortie local reel produit par `etape_3_001` pour le test live cible
- aucun moteur STT reel requis pour `pytest` / `make check`
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI du type :

```bash
python -m sceneqora.cli.main validate-local-pipeline-output /chemin/output_dir
```

Cette commande doit :
- lire le dossier d'artefacts produit par le pipeline ;
- afficher une sortie JSON stable avec :
  - `output_dir`
  - `audio_exists`
  - `transcript_exists`
  - `segments_exists`
  - `srt_exists`
  - `segment_count`
  - `subtitle_count`
  - `status`

## Convention explicite
- un transcript texte vide reste autorise
- un SRT vide est autorise seulement si `segments` est vide
- le statut global doit etre explicite et coherent, par exemple `completed` ou `invalid`

## Exigences fonctionnelles
- [ ] Un dossier produit par le pipeline local peut etre valide
- [ ] Les 4 artefacts attendus sont verifies explicitement
- [ ] Le JSON segments est valide minimalement
- [ ] Une coherence simple entre `segments` et `subtitles.srt` est verifiee
- [ ] La CLI expose une commande simple dediee
- [ ] Les tests restent deterministes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas de surconstruction
- Pas d'elargissement de scope
- Pas de validation semantique avancee
- Validation locale, minimale, explicable
- Validation structurelle et de coherence seulement
- Pas de logique smart
- Pas de correction automatique
- Sortie de validation en JSON stable

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Sortie visible lisible de validation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale de validation locale des outputs du pipeline
- commande CLI `validate-local-pipeline-output`
- format JSON stable de validation
- eventuel contrat minimal de sortie de validation

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] Les artefacts attendus sont verifies
- [ ] Si le ticket touche une integration reelle, un test live cible hors `make check` est execute et documente
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Definir la validation minimale des 4 artefacts attendus et la convention de statut global
2. Ajouter une brique locale de validation structurelle et de coherence simple
3. Ajouter la commande `validate-local-pipeline-output` et la sortie JSON stable
4. Ajouter les tests deterministes sur les cas valides et invalides
5. Executer et documenter le test live cible hors `make check`

## Cas limites
1. Le dossier de sortie n'existe pas
2. Un artefact attendu est absent
3. `transcript_segments.json` est invalide
4. `transcript_segments.json` ne contient pas `segments`
5. `segments` est non vide mais le SRT est vide
6. `audio.wav` est vide
7. Le dossier est present mais incomplet

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
python -m sceneqora.cli.main validate-local-pipeline-output /chemin/output_dir
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Le test live cible peut s'appuyer sur un dossier de sortie local reel produit par `etape_3_001`.

## Validation manuelle attendue
- verifier que la commande CLI lit bien un dossier de sortie de pipeline ;
- verifier que la sortie visible confirme au minimum la presence des 4 artefacts, les compteurs minimaux et le statut ;
- verifier que `audio.wav` vide est bien rejete ;
- verifier que `transcript_segments.json` est valide minimalement ;
- verifier que la coherence simple entre `segments` et `subtitles.srt` est respectee ;
- verifier qu'il n'y a aucun glissement vers scoring qualite, correction ou reporting riche ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de glisser de la validation structurelle vers une evaluation semantique trop riche ;
- risque d'introduire une logique de correction automatique non demandee ;
- risque de sur-modeliser la sortie de validation ;
- risque de melanger verification locale simple et interpretation metier plus lourde ;
- attention a garder un statut global simple, explicite et coherent.

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
