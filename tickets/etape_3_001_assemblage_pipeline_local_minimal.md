# Titre
Etape 3_001 - Assemblage pipeline local minimal

## Identifiant
etape_3_001_assemblage_pipeline_local_minimal

## Etape
Etape 3 - Assemblage pipeline local minimal

## Contexte / Probleme
Sceneqora dispose maintenant des briques unitaires minimales de l'etape 2 :
- probe video local ;
- extraction audio locale ;
- transcription texte locale ;
- transcription horodatee JSON locale ;
- generation SRT minimale.

En revanche, aucune orchestration locale minimale ne permet encore d'enchainer ces briques sur une video locale unique pour produire automatiquement les artefacts attendus dans un dossier de sortie local.

Avant d'ouvrir une orchestration plus riche, il faut poser une capacite simple, visible et bornee :
- prendre une video locale en entree ;
- creer un dossier de sortie local si necessaire, ou definir explicitement le comportement ;
- executer les briques existantes strictement en sequence ;
- produire les artefacts attendus avec des noms fixes ;
- exposer le tout via une commande CLI simple.

Cette brique doit rester un assembleur mince de briques existantes, sans devenir un moteur de pipeline generique.

## Objectif
Introduire une orchestration locale minimale capable d'enchainer sequentiellement les briques existantes sur une video locale unique afin de produire dans un dossier cible :
- `audio.wav`
- `transcript.txt`
- `transcript_segments.json`
- `subtitles.srt`

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une commande CLI simple dediee au pipeline local minimal ;
- une orchestration strictement sequentielle des briques existantes :
  1. extraction audio
  2. transcription texte
  3. transcription horodatee JSON
  4. generation SRT
- un comportement explicite vis-a-vis du dossier de sortie local ;
- une generation reelle des 4 artefacts attendus avec des noms fixes ;
- une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_dir`
  - `audio_path`
  - `transcript_path`
  - `segments_path`
  - `srt_path`
  - `status`
- des tests deterministes avec mocks / stubs des briques appelees ;
- un test live cible hors `make check`.

Le ticket s'arrete a l'assemblage local minimal.
Il n'ouvre ni moteur de pipeline generique, ni orchestration complexe, ni optimisations transverses.

## Perimetre
Inclus :
- lecture d'un fichier video local ;
- lecture d'un dossier de sortie local ;
- creation du dossier de sortie si necessaire, ou comportement explicitement defini si absent ;
- orchestration sequentielle minimale des briques existantes :
  1. extraction audio
  2. transcription texte
  3. transcription horodatee JSON
  4. generation SRT
- reutilisation stricte des briques existantes, sans duplication de logique ;
- generation des artefacts locaux suivants :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- ajout d'une commande CLI simple dediee au pipeline local minimal ;
- sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_dir`
  - `audio_path`
  - `transcript_path`
  - `segments_path`
  - `srt_path`
  - `status`
- tests unitaires / integration adaptes avec mocks / stubs ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- batch
- parallelisation
- reprise avancee sur erreur
- scheduler
- cache complexe
- configuration riche
- burn-in video
- UI
- API
- workflow distribue
- selection dynamique de moteurs
- optimisation perf transverse
- monitoring avance
- pipeline engine generique
- refactor transverse non justifie

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_2_002_extraction_audio_locale_minimale.md`
- `tickets/etape_2_003_transcription_audio_locale_minimale.md`
- `tickets/etape_2_004_horodatage_transcription_audio_minimal.md`
- `tickets/etape_2_005_generation_srt_minimale.md`

## Dependances / Pre-requis
- Etape 2 consideree comme suffisamment fermee pour les briques unitaires minimales
- une video locale exploitable en entree pour le test live cible
- `ffmpeg` disponible localement pour l'extraction audio lors du test live
- un moteur STT local disponible uniquement pour le test live cible
- les tests deterministes ne doivent pas dependre d'executions reelles lourdes
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple du type :

```bash
python -m sceneqora.cli.main run-local-pipeline /chemin/video.mp4 /chemin/output_dir
```

Cette commande doit :
- produire reellement les 4 artefacts dans le dossier cible ;
- afficher une sortie JSON stable avec :
  - `source_path`
  - `output_dir`
  - `audio_path`
  - `transcript_path`
  - `segments_path`
  - `srt_path`
  - `status`

## Exigences fonctionnelles
- [ ] Une video locale peut etre utilisee comme source
- [ ] Le pipeline produit les 4 artefacts attendus
- [ ] L'orchestration reste mince et reutilise les briques existantes
- [ ] En cas d'echec d'une etape, l'erreur est explicite
- [ ] La CLI expose une commande simple dediee
- [ ] Les tests deterministes ne dependent pas d'executions reelles lourdes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas de surconstruction
- Pas d'elargissement de scope
- Pas de pipeline engine generique
- Pas de duplication de logique metier
- Orchestration strictement sequentielle
- Pas de skip d'etape
- Pas d'options avancees
- Noms d'artefacts fixes et explicites :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- Sortie de synthese en JSON stable

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Dossier de sortie local avec les 4 artefacts generes
- [ ] Sortie visible lisible de confirmation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- assembleur mince de pipeline local minimal
- reutilisation des briques d'extraction, transcription texte, transcription horodatee et generation SRT
- commande CLI `run-local-pipeline`
- convention de noms fixes des artefacts
- format JSON stable de synthese

## Definition of Done (DoD)
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes ou mis a jour
- [ ] Les artefacts attendus sont generes et verifies
- [ ] Si le ticket touche une integration reelle, un test live cible hors `make check` est execute et documente
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `mypy` est vert sur le perimetre du ticket si le module est type
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Definir l'assembleur minimal et la convention de noms fixes des artefacts
2. Ajouter une orchestration sequentielle stricte qui reutilise les briques existantes sans dupliquer leur logique
3. Definir le comportement explicite du dossier de sortie local
4. Etendre la CLI avec une commande `run-local-pipeline` et une sortie JSON stable
5. Ajouter les tests deterministes avec mocks / stubs, puis executer et documenter le test live cible hors `make check`

## Cas limites
1. La video source n'existe pas
2. Le dossier de sortie est invalide ou non accessible
3. Une etape intermediaire echoue
4. Un artefact intermediaire attendu n'est pas produit
5. Le pipeline s'arrete proprement sur la premiere erreur bloquante
6. Le repertoire de sortie existe deja

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
python -m sceneqora.cli.main run-local-pipeline /chemin/video.mp4 /chemin/output_dir
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Ils doivent mocker ou stubber les briques appelees.
Le test live cible hors `make check` peut s'appuyer sur les integrations locales reelles deja introduites aux etapes 2.

## Validation manuelle attendue
- verifier que la commande CLI produit bien les 4 artefacts dans le dossier cible ;
- verifier que les noms d'artefacts sont fixes et conformes :
  - `audio.wav`
  - `transcript.txt`
  - `transcript_segments.json`
  - `subtitles.srt`
- verifier que la sortie visible confirme au minimum le chemin source, le dossier de sortie, les 4 chemins d'artefacts et le statut ;
- verifier que l'orchestration reste mince et ne duplique pas la logique des etapes 2 ;
- verifier que le pipeline s'arrete proprement sur la premiere erreur bloquante ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de transformer un assembleur mince en moteur de pipeline generique ;
- risque de dupliquer la logique des briques existantes plutot que de les reutiliser ;
- risque d'introduire trop tot des options, des skips ou des comportements conditionnels complexes ;
- risque de melanger orchestration, validation d'entree et logique metier des etapes ;
- attention a garder l'ordre d'execution strictement sequentiel et explicite.

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
