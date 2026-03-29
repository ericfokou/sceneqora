# Titre
Etape 3_003 - Support entree parole reelle minimale

## Identifiant
etape_3_003_support_entree_parole_reelle_minimale

## Etape
Etape 3 - Assemblage pipeline local minimal

## Contexte / Probleme
Sceneqora dispose maintenant :
- d'un pipeline local minimal capable de produire les artefacts attendus ;
- d'une validation structurelle minimale des outputs produits ;
- de tests deterministes qui securisent le comportement technique de base.

En revanche, le pipeline n'a pas encore ete explicitement securise sur un cas live contenant reellement de la parole. Les runs de validation realises jusqu'ici sur des medias synthetiques peuvent produire des artefacts textuels vides tout en restant structurellement valides.

Avant d'ouvrir une evaluation plus riche, un scoring qualite ou une validation semantique avancee, il faut poser une capacite minimale, explicable et locale pour verifier qu'une vraie source vocale locale :
- peut etre traitee par le pipeline existant ;
- produit bien des artefacts textuels non vides ;
- reste dans une validation simple de presence exploitable, sans promesse de qualite semantique.

## Objectif
Introduire une capacite strictement minimale permettant de securiser un run live du pipeline sur une source locale contenant reellement de la parole, afin de verifier que les artefacts textuels produits ne restent pas vides sur ce cas.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une prise en compte explicite d'une source locale contenant de la parole reelle pour le test live ;
- l'execution du pipeline existant sur cette source ;
- une validation minimale orientee "presence de parole exploitable" :
  - `audio.wav` existe et n'est pas vide
  - `transcript.txt` existe et n'est pas vide
  - `transcript_segments.json` existe et contient au moins un segment
  - `subtitles.srt` existe et n'est pas vide
- soit une commande CLI simple dediee si c'est la solution la plus mince ;
- soit, a defaut, une validation / documentation explicite du run live vocal reel ;
- si une CLI est ajoutee, une sortie visible stable confirmant au minimum :
  - `output_dir`
  - `transcript_non_empty`
  - `segment_count`
  - `srt_non_empty`
  - `status`
- des tests deterministes sans dependance a un vrai media vocal ;
- un test live cible hors `make check`.

Le ticket s'arrete a une validation minimale de presence d'artefacts textuels non vides sur une vraie source vocale.
Il n'ouvre ni evaluation qualite avancee, ni benchmark, ni validation semantique riche.

## Perimetre
Inclus :
- prise en compte d'une source locale contenant de la parole reelle pour le test live ;
- execution du pipeline local existant sur cette source ;
- verification minimale que les artefacts textuels utiles ne restent pas vides ;
- ajout eventuel d'une commande CLI simple dediee si cela reste la solution la plus mince ;
- a defaut, ajout d'une validation / documentation explicite du run live vocal reel ;
- sortie visible stable si une CLI est ajoutee, confirmant au minimum :
  - `output_dir`
  - `transcript_non_empty`
  - `segment_count`
  - `srt_non_empty`
  - `status`
- tests unitaires / integration adaptes et deterministes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- corpus de test
- benchmark comparatif
- scoring WER
- scoring CER
- multi-langue
- evaluation semantique riche
- nettoyage de transcript
- diarisation
- amelioration de modele
- reglages automatiques
- batch de medias vocaux
- reporting riche
- dashboard
- validation linguistique avancee

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_3_001_assemblage_pipeline_local_minimal.md`
- `tickets/etape_3_002_validation_output_pipeline_minimale.md`

## Dependances / Pre-requis
- Etape 3 deja ouverte avec le pipeline local minimal et la validation structurelle simple
- une source locale contenant reellement de la parole doit etre disponible pour le test live cible
- les tests `pytest` / `make check` ne doivent jamais dependre d'un vrai media vocal
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Soit une commande CLI du type :

```bash
python -m sceneqora.cli.main validate-real-speech-pipeline-output /chemin/output_dir
```

avec une sortie JSON stable contenant au minimum :
- `output_dir`
- `transcript_non_empty`
- `segment_count`
- `srt_non_empty`
- `status`

Soit, si cette option est plus mince et plus coherente avec l'architecture existante :
- une documentation stricte de validation live du pipeline sur une vraie source vocale locale ;
- un protocole de verification explicite ;
- un retour visible et testable documente dans le notebook / retour de ticket.

## Convention explicite
- sur une vraie source vocale locale, `transcript.txt` non vide est attendu
- sur une vraie source vocale locale, `segment_count > 0` est attendu
- sur une vraie source vocale locale, un SRT non vide est attendu
- cela ne constitue pas une promesse de qualite semantique du transcript
- les tests determines dans `pytest` / `make check` ne doivent jamais dependre d'un vrai media vocal

## Exigences fonctionnelles
- [ ] Une source locale contenant de la parole reelle peut etre utilisee pour un run live du pipeline
- [ ] Le run live produit des artefacts textuels non vides
- [ ] La validation reste minimale et explicable
- [ ] La solution n'ouvre pas d'evaluation qualite avancee
- [ ] Les tests restent deterministes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas de surconstruction
- Pas d'elargissement de scope
- Pas de benchmark riche
- Pas d'evaluation semantique avancee
- Pas de dependance a un vrai media vocal dans `pytest` / `make check`
- Si une CLI est ajoutee, elle doit rester tres mince

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Sortie visible lisible de validation ou documentation explicite du run live
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- eventuelle brique minimale de validation orientee parole reelle
- eventuelle commande CLI `validate-real-speech-pipeline-output`
- eventuel format JSON stable de sortie de validation live
- documentation du protocole live vocal si aucune CLI additionnelle n'est retenue

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] La validation minimale du cas parole reelle est documentee et verifiee
- [ ] Le test live cible hors `make check` est execute et documente
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Choisir la solution la plus mince entre une petite validation CLI dediee et une documentation stricte du run live vocal
2. Reutiliser le pipeline existant sans dupliquer sa logique ni ouvrir de nouveau moteur
3. Ajouter la validation minimale orientee artefacts textuels non vides sur vraie parole
4. Ajouter les tests deterministes sans dependance a un vrai media vocal
5. Executer et documenter le test live cible sur une source vocale locale reelle

## Cas limites
1. La source vocale reelle n'est pas disponible localement
2. Le pipeline s'execute mais le transcript reste vide
3. Le JSON segments est vide
4. Le SRT est vide
5. La validation live echoue alors que la validation structurelle simple passe
6. Les tests deterministes ne doivent jamais dependre d'un vrai media vocal

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
python -m sceneqora.cli.main run-local-pipeline /chemin/source_vocale_reelle.mp4 /chemin/output_dir
```

Si une CLI minimale dediee est retenue :

```bash
python -m sceneqora.cli.main validate-real-speech-pipeline-output /chemin/output_dir
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Le test live cible doit s'appuyer sur une vraie source vocale locale.

## Validation manuelle attendue
- verifier qu'une vraie source vocale locale peut etre traitee par le pipeline existant ;
- verifier que `audio.wav` est present et non vide ;
- verifier que `transcript.txt` est present et non vide ;
- verifier que `transcript_segments.json` contient au moins un segment ;
- verifier que `subtitles.srt` est present et non vide ;
- verifier qu'il n'y a aucune promesse de qualite semantique du transcript ;
- verifier que le test live cible est documente proprement dans le retour.

## Risques / Points d'attention
- risque de glisser d'une verification de presence exploitable vers une evaluation qualite trop riche ;
- risque d'introduire un mini-framework de benchmark ou de dataset management non demande ;
- risque de faire dependre les tests deterministes d'un vrai media vocal ;
- attention a garder une solution mince, explicable et strictement orientee validation live minimale.

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
