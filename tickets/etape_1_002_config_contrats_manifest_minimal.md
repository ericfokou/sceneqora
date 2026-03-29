# Titre
Etape 1_002 - Configuration minimale et contrats metier initiaux

## Identifiant
etape_1_002_config_contrats_manifest_minimal

## Etape
Etape 1 - Bootstrap repo minimal et socle executable

## Contexte / Probleme
Le bootstrap minimal du repo existe desormais, mais le socle du pipeline reste incomplet :
- aucune configuration minimale chargeable n'est encore posee ;
- aucun contrat metier initial structurant n'est formalise au niveau le plus basique ;
- aucun manifest minimal de job n'existe pour decrire proprement un run ;
- la CLI reste limitee au bootstrap et n'expose pas encore de mode simple d'inspection.

Cette absence bloque la prochaine couche du projet, car Sceneqora doit rester pipeline-first, explicite et oriente artefacts sans partir trop tot dans l'implementation video/IA.

## Objectif
Poser un socle minimal de configuration et de contrats metier initiaux permettant de charger une configuration unique simple, de manipuler un manifest de job minimal, et d'exposer ces elements via une CLI legere d'inspection.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- un loader de configuration minimal et local chargeant une seule config `configs/default.yaml` ;
- les premiers modeles metier types strictement bornes au noyau minimal du projet ;
- un manifest minimal de job serialisable ;
- une CLI simple avec un seul mode d'inspection minimal ;
- des tests locaux couvrant ce socle.

Le ticket s'arrete a cette couche de contrats et de configuration.
Aucune logique d'ingestion video reelle n'est attendue.

## Perimetre
Inclus :
- ajout d'un module minimal de configuration dans `infra/` ;
- ajout d'un fichier de configuration minimale unique chargeable dans `configs/default.yaml` ;
- ajout des premiers modeles metier types dans `domain/`, limites a `AppConfig`, `JobManifest` et eventuellement un identifiant ou statut minimal de job ;
- ajout d'un manifest minimal de job borne aux champs simples `job_id`, `created_at`, `profile_name` ou equivalent, `app_version` ou equivalent, `status` et un snapshot minimal de configuration ;
- ajout ou extension minimale de la CLI pour un seul mode d'inspection ;
- ajout des tests associes au chargement de config, aux contrats metier, au manifest et a la CLI ;
- ajustement minimal du `Makefile` ou du socle de checks si necessaire pour couvrir ce ticket.

## Hors perimetre
- ingestion video reelle
- extraction audio
- FFmpeg
- transcription
- Whisper / WhisperX
- segmentation
- scoring
- tracking / crop
- sous-titres
- rendering
- integrations externes
- plugin system
- profils de configuration
- overrides de configuration
- hierarchie de configuration complexe
- orchestration pipeline reelle
- artefacts de job
- metadonnees video
- decisions de pipeline
- clips
- exports
- scores
- `VideoAsset`
- `Transcript`
- `CandidateClip`
- `ClipScore`
- `CropPlan`
- tout contrat pipeline reel au-dela du noyau minimal

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_1_001_bootstrap_repo_minimal.md`

## Dependances / Pre-requis
- bootstrap repo minimal deja en place
- package Python `sceneqora` deja present
- CLI minimale deja disponible
- aucun binaire externe requis
- ne faire aucun commit / push / PR / merge a l'issue du ticket sans GO explicite

## Livrable visible attendu
Un socle local testable dans lequel :
- une config minimale unique `configs/default.yaml` est chargeable ;
- des contrats metier initiaux explicites existent au niveau noyau minimal ;
- un manifest minimal de job est serialisable ;
- la CLI permet de charger la config et d'afficher un manifest minimal serialize de maniere lisible ;
- les tests associes passent localement.

## Exigences fonctionnelles
- [ ] Une configuration minimale unique `configs/default.yaml` peut etre chargee depuis le repo
- [ ] Les premiers modeles metier structures existent et sont types, limites a `AppConfig`, `JobManifest` et eventuellement un identifiant ou statut minimal de job
- [ ] Un manifest minimal de job peut etre instancie et serialize avec comme champs simples `job_id`, `created_at`, `profile_name` ou equivalent, `app_version` ou equivalent, `status` et un snapshot minimal de configuration
- [ ] La CLI expose un seul mode simple d'inspection pour charger la config et afficher un manifest minimal serialize
- [ ] Les tests couvrent le chargement de config, le manifest et la CLI
- [ ] `make check` fonctionne au niveau attendu pour ce ticket

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- Pas de logique pipeline metier reelle
- Pas d'integration externe
- Pas de surconstruction
- Pas de plugin system
- Pas de config complexe prematuree
- Une seule config `configs/default.yaml`
- Pas de profils
- Pas d'overrides
- Pas de hierarchie complexe
- La CLI doit rester minimale et lisible
- Pas de logique d'orchestration
- Le manifest doit rester limite a des champs simples

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Config minimale unique chargeable localement
- [ ] Manifest minimal serialisable
- [ ] Documentation minimale si necessaire

## Contrats / Interfaces touches
- loader de configuration minimal
- schema ou modele de configuration initial
- `AppConfig`
- `JobManifest`
- identifiant ou statut minimal de job si necessaire
- manifest minimal de job borne a `job_id`, `created_at`, `profile_name` ou equivalent, `app_version` ou equivalent, `status` et un snapshot minimal de configuration
- point d'entree CLI pour un seul mode d'inspection
- conventions minimales de serialisation

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] Les artefacts attendus sont generes et verifies
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Poser `configs/default.yaml` et un loader simple dans `infra/`
2. Definir `AppConfig`, `JobManifest` et le noyau minimal associe dans `domain/`
3. Etendre la CLI avec un seul mode d'inspection pour charger la config et afficher un manifest minimal serialize, sans lancer de pipeline reel
4. Ajouter les tests locaux cibles et ajuster les checks de base
5. Executer les validations locales et remonter le resultat pour review

## Cas limites
1. Le fichier de config minimal existe mais ne se charge pas proprement depuis la racine du repo
2. Le manifest minimal devient trop riche et commence a embarquer des artefacts, des metadonnees video ou des decisions de pipeline prematurees
3. La CLI d'inspection devient trop bavarde ou melange deja inspection, orchestration et logique metier

## Criteres de verification
```bash
pytest
ruff check .
make check
python -m sceneqora.cli.main --help
```

## Validation manuelle attendue
- verifier que `configs/default.yaml` peut etre charge sans dependance externe ;
- verifier qu'un manifest minimal est lisible, serialisable et borne a des champs simples ;
- verifier que la CLI expose clairement un seul mode d'inspection ;
- verifier que les contrats metier restent petits, explicites et sans logique pipeline reelle.

## Risques / Points d'attention
- risque de sur-modeliser trop tot les contrats metier ;
- risque de faire porter a la config des responsabilites d'orchestration prematurees ;
- risque de glisser vers de l'ingestion ou du pipeline reel sous couvert de manifest ;
- risque d'introduire trop tot des contrats comme `VideoAsset`, `Transcript`, `CandidateClip`, `ClipScore` ou `CropPlan` ;
- attention a garder la separation entre `domain`, `infra` et `cli`.

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
