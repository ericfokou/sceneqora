# Titre
Etape 4_001 - API locale minimale

## Identifiant
etape_4_001_api_locale_minimale

## Etape
Etape 4 - API locale minimale

## Contexte / Probleme
Sceneqora dispose maintenant :
- d'un pipeline local minimal executable sur une video locale unique ;
- d'une validation structurelle minimale des outputs ;
- d'un support minimal du cas vocal reel ;
- d'un packaging local minimal des artefacts d'un run.

En revanche, l'acces a ces capacites reste borne a la CLI locale. Rien ne permet encore de declencher simplement un run via une interface HTTP locale minimale exploitable par un outil tiers, un script local ou un futur front local.

Avant d'ouvrir de l'asynchrone, de l'authentification, de la persistence ou une API plus riche, il faut poser une capacite strictement minimale, explicable et locale :
- demarrer un petit serveur API local ;
- verifier sa disponibilite ;
- declencher un run synchrone du pipeline existant ;
- retourner une reponse JSON simple et stable.

## Objectif
Introduire une API HTTP locale strictement minimale permettant de declencher un run du pipeline sur une video locale et de recuperer une reponse JSON simple.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- un serveur API local minimal ;
- un endpoint `GET /health` ;
- un endpoint `POST /runs` ;
- une entree JSON minimale avec :
  - `source_path`
  - `output_dir`
- une execution synchrone du pipeline local existant ;
- une reutilisation stricte des briques existantes ;
- une reponse JSON stable sur succes contenant au minimum :
  - `source_path`
  - `output_dir`
  - `audio_path`
  - `transcript_path`
  - `segments_path`
  - `srt_path`
  - `status`
- des erreurs HTTP simples et explicites ;
- des tests deterministes ;
- un test live cible hors `make check`.

Le ticket s'arrete a une API HTTP locale minimale, synchrone, mono-run par appel.
Il n'ouvre ni jobs asynchrones, ni persistence, ni API distribuee.

## Perimetre
Inclus :
- ajout d'un serveur API local minimal ;
- ajout d'un endpoint `GET /health` ;
- ajout d'un endpoint `POST /runs` ;
- lecture d'un payload JSON minimal avec :
  - `source_path`
  - `output_dir`
- execution synchrone du pipeline local existant ;
- reutilisation stricte des briques existantes ;
- reponse JSON stable sur succes contenant au minimum :
  - `source_path`
  - `output_dir`
  - `audio_path`
  - `transcript_path`
  - `segments_path`
  - `srt_path`
  - `status`
- erreurs HTTP simples et explicites ;
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- auth
- queue
- jobs asynchrones
- websocket
- streaming
- upload de fichier
- stockage distant
- base de donnees
- historique de runs
- pagination
- UI
- API distribuee
- deploiement cloud
- rate limiting
- observabilite avancee
- refactor transverse non justifie

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_3_001_assemblage_pipeline_local_minimal.md`
- `tickets/etape_3_002_validation_output_pipeline_minimale.md`
- `tickets/etape_3_003_support_entree_parole_reelle_minimale.md`
- `tickets/etape_3_004_packaging_run_output_minimal.md`

## Dependances / Pre-requis
- Etape 3 deja stabilisee avec un pipeline local minimal exploitable
- l'API doit reutiliser le pipeline existant sans dupliquer sa logique
- aucun service externe ne doit etre requis
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
1. un endpoint :

```http
GET /health
```

reponse :

```json
{"status": "ok"}
```

2. un endpoint :

```http
POST /runs
```

payload :

```json
{
  "source_path": "/chemin/video.mp4",
  "output_dir": "/chemin/output_dir"
}
```

reponse de succes :

```json
{
  "source_path": "/chemin/video.mp4",
  "output_dir": "/chemin/output_dir",
  "audio_path": "/chemin/output_dir/audio.wav",
  "transcript_path": "/chemin/output_dir/transcript.txt",
  "segments_path": "/chemin/output_dir/transcript_segments.json",
  "srt_path": "/chemin/output_dir/subtitles.srt",
  "status": "completed"
}
```

## Convention explicite
- l'API est locale uniquement
- l'execution du pipeline est synchrone
- aucun `job_id` n'est introduit
- aucune persistence n'est introduite
- les erreurs HTTP restent simples et explicites
- la sortie JSON de succes reste stable et coherente avec le contrat du pipeline existant

## Exigences fonctionnelles
- [ ] L'API locale peut demarrer
- [ ] `GET /health` repond correctement
- [ ] `POST /runs` lance le pipeline local existant
- [ ] La reponse JSON de succes est stable et testable
- [ ] Les erreurs d'entree sont explicites
- [ ] Les tests restent deterministes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas de surconstruction
- Pas d'elargissement de scope
- API HTTP locale uniquement
- Execution synchrone
- Pas de dependance a des services externes

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Serveur API local minimal executable
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- serveur API HTTP local minimal
- endpoint `GET /health`
- endpoint `POST /runs`
- format JSON minimal de requete pour `POST /runs`
- format JSON minimal de reponse de succes
- convention simple d'erreurs HTTP

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] Le serveur local et les endpoints attendus sont verifies
- [ ] Le test live cible hors `make check` est execute et documente
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Choisir une solution de serveur HTTP locale minimale, simple et explicable
2. Ajouter `GET /health` avec une reponse JSON fixe
3. Ajouter `POST /runs` en reutilisant strictement le pipeline local existant
4. Ajouter les tests deterministes sur succes et erreurs simples
5. Executer et documenter le test live cible hors `make check`

## Cas limites
1. Payload absent ou invalide
2. `source_path` absent
3. `output_dir` absent
4. Fichier source inexistant
5. Echec du pipeline
6. Methode HTTP invalide
7. Serveur demarre mais endpoint inconnu

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
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/runs \
  -H "Content-Type: application/json" \
  -d '{"source_path":"/chemin/video.mp4","output_dir":"/chemin/output_dir"}'
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Le test live cible peut s'appuyer sur un serveur local demarre uniquement pour cette validation.

## Validation manuelle attendue
- verifier que le serveur API local demarre correctement ;
- verifier que `GET /health` repond bien avec `{"status":"ok"}` ;
- verifier que `POST /runs` declenche bien le pipeline local existant ;
- verifier que la reponse JSON de succes contient les chemins attendus et le statut ;
- verifier que les erreurs HTTP d'entree restent simples et explicites ;
- verifier qu'il n'y a aucun glissement vers jobs asynchrones, persistence, auth ou API distribuee.

## Risques / Points d'attention
- risque de glisser d'une API locale minimale vers une API de jobs plus riche sans validation ;
- risque de dupliquer la logique du pipeline au lieu de la reutiliser ;
- risque de sur-construire la gestion d'erreurs HTTP ;
- attention a garder une execution synchrone simple, un contrat JSON stable et aucun mecanisme de persistence.

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
