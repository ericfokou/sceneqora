# Sceneqora — Guide de structure cible

## 1. Objet du document

Ce document définit la **structure cible de référence** du projet **Sceneqora**.

Son rôle est double :
- servir de **guide d’architecture** pour organiser le repo ;
- servir de **contrat de cohérence** pour les futures implémentations locales réalisées par Codex / gemini-cli.

Ce document ne décrit pas uniquement une arborescence. Il précise aussi :
- les responsabilités de chaque couche ;
- les frontières entre modules ;
- les conventions de nommage ;
- les points d’extension ;
- les règles à respecter pour éviter qu’un pipeline média/IA devienne monolithique et fragile.

---

## 2. Vision produit

**Sceneqora** est un pipeline IA vidéo qui prend en entrée une vidéo longue et produit des extraits courts optimisés pour des formats de type Reels / TikTok / Shorts.

Le système doit pouvoir :
- ingérer une vidéo longue ;
- analyser audio, transcript et signal visuel ;
- détecter des passages intéressants ;
- scorer et sélectionner les meilleurs moments ;
- recadrer les extraits en format vertical ;
- générer des sous-titres dynamiques ;
- exporter des clips prêts à publier.

Le projet doit rester :
- **modulaire** ;
- **testable** ;
- **observable** ;
- **extensible** ;
- **pilotable par configuration**.

---

## 3. Principes d’architecture

## 3.1 Python d’abord

Le repo doit être pensé **Python-first**.

Python est l’orchestrateur principal de :
- l’ingestion ;
- l’analyse ;
- la segmentation ;
- le scoring ;
- le recadrage ;
- la génération des assets intermédiaires ;
- l’export.

## 3.2 ComfyUI optionnel, jamais central

ComfyUI peut exister comme **brique optionnelle** pour :
- stylisation ;
- habillage ;
- effets visuels ;
- post-traitements spécifiques.

Mais ComfyUI ne doit **pas** devenir le cœur d’orchestration du pipeline.

## 3.3 Pipeline orienté artefacts

Chaque étape importante doit produire des **artefacts intermédiaires explicites**, par exemple :
- audio extrait ;
- transcript ;
- diarisation ;
- shots ;
- segments candidats ;
- scores ;
- trajectoire de crop ;
- fichier de sous-titres ;
- manifest final.

Objectif : permettre le debug, la reprise, l’inspection et le recalcul partiel.

## 3.4 Architecture par domaines, pas par librairies

L’organisation du code ne doit pas être pilotée par les outils utilisés.

À éviter :
- un dossier `whisper/`
- un dossier `ffmpeg/`
- un dossier `opencv/`

À privilégier :
- `transcription/`
- `segmentation/`
- `scoring/`
- `rendering/`

Les outils sont des détails d’implémentation derrière des interfaces claires.

## 3.5 Contrat fort entre analyse et rendu

La couche d’analyse ne doit pas écrire directement la vidéo finale.

Elle doit produire des **décisions structurées** :
- début / fin du clip ;
- score ;
- justification ;
- sujet principal ;
- trajectoire de crop ;
- style de sous-titres.

La couche de rendu consomme ces décisions et produit l’export.

---

## 4. Structure cible du repo

```text
sceneqora/
├─ README.md
├─ guide.md
├─ pyproject.toml
├─ .env.example
├─ .gitignore
├─ Makefile
├─ configs/
│  ├─ default.yaml
│  ├─ profiles/
│  │  ├─ documentary.yaml
│  │  ├─ interview.yaml
│  │  ├─ movie.yaml
│  │  └─ social_clip.yaml
│  └─ prompts/
│     ├─ clip_scoring.yaml
│     └─ hook_detection.yaml
├─ data/
│  ├─ raw/
│  ├─ working/
│  ├─ outputs/
│  └─ fixtures/
├─ docs/
│  ├─ architecture/
│  ├─ decisions/
│  ├─ runbooks/
│  └─ recaps/
├─ scripts/
│  ├─ dev/
│  ├─ batch/
│  └─ release/
├─ src/
│  └─ sceneqora/
│     ├─ __init__.py
│     ├─ cli/
│     │  ├─ __init__.py
│     │  └─ main.py
│     ├─ app/
│     │  ├─ __init__.py
│     │  ├─ pipeline.py
│     │  ├─ orchestrator.py
│     │  └─ jobs.py
│     ├─ domain/
│     │  ├─ __init__.py
│     │  ├─ models.py
│     │  ├─ enums.py
│     │  ├─ manifests.py
│     │  └─ policies.py
│     ├─ ingestion/
│     │  ├─ __init__.py
│     │  ├─ video_loader.py
│     │  ├─ audio_extractor.py
│     │  └─ probe.py
│     ├─ transcription/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ whisper_adapter.py
│     │  ├─ whisperx_adapter.py
│     │  └─ diarization.py
│     ├─ segmentation/
│     │  ├─ __init__.py
│     │  ├─ shot_detection.py
│     │  ├─ silence_detection.py
│     │  ├─ candidate_builder.py
│     │  └─ deduplication.py
│     ├─ scoring/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ semantic.py
│     │  ├─ audio.py
│     │  ├─ visual.py
│     │  ├─ fusion.py
│     │  └─ ranking.py
│     ├─ tracking/
│     │  ├─ __init__.py
│     │  ├─ faces.py
│     │  ├─ subjects.py
│     │  ├─ saliency.py
│     │  └─ crop_path.py
│     ├─ subtitles/
│     │  ├─ __init__.py
│     │  ├─ tokens.py
│     │  ├─ ass_writer.py
│     │  ├─ styling.py
│     │  └─ templates.py
│     ├─ rendering/
│     │  ├─ __init__.py
│     │  ├─ ffmpeg_builder.py
│     │  ├─ vertical_reframe.py
│     │  ├─ burn_subtitles.py
│     │  └─ exporter.py
│     ├─ integrations/
│     │  ├─ __init__.py
│     │  ├─ comfyui/
│     │  │  ├─ __init__.py
│     │  │  ├─ client.py
│     │  │  └─ workflows.py
│     │  └─ llm/
│     │     ├─ __init__.py
│     │     ├─ client.py
│     │     └─ prompts.py
│     ├─ infra/
│     │  ├─ __init__.py
│     │  ├─ config.py
│     │  ├─ logging.py
│     │  ├─ paths.py
│     │  ├─ subprocess.py
│     │  └─ cache.py
│     ├─ observability/
│     │  ├─ __init__.py
│     │  ├─ metrics.py
│     │  ├─ tracing.py
│     │  └─ reports.py
│     └─ utils/
│        ├─ __init__.py
│        ├─ time.py
│        ├─ hashing.py
│        └─ validation.py
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ e2e/
│  └─ fixtures/
└─ outputs/
   └─ .gitkeep
```

---

## 5. Rôle de chaque zone

## 5.1 `configs/`

Contient toute la configuration pilotant le pipeline.

On doit y trouver :
- profils par type de contenu ;
- paramètres de scoring ;
- contraintes de durée ;
- styles de sous-titres ;
- paramètres de rendu ;
- prompts éventuels pour les briques LLM.

Règle : **aucune valeur métier importante ne doit être hardcodée dans les modules** si elle peut raisonnablement vivre en configuration.

## 5.2 `data/`

Zone de travail locale.

- `raw/` : entrées brutes
- `working/` : artefacts intermédiaires temporaires
- `outputs/` : exports finaux produits localement
- `fixtures/` : médias de test contrôlés

Règle : les sorties de pipeline ne doivent pas être dispersées ailleurs dans le repo.

## 5.3 `docs/`

Zone de documentation vivante.

- `architecture/` : vues système
- `decisions/` : ADR, arbitrages structurants
- `runbooks/` : procédures opératoires
- `recaps/` : récapitulatifs de sessions

## 5.4 `scripts/`

Scripts utilitaires d’environnement et d’exploitation.

À réserver à :
- bootstrap local ;
- exécution batch ;
- packaging ;
- scripts ponctuels de maintenance.

Règle : un script ne doit pas contenir la logique métier principale. Il appelle le code de `src/`.

## 5.5 `src/sceneqora/domain/`

Le cœur du langage métier.

Doit contenir les objets structurants, par exemple :
- `VideoAsset`
- `Transcript`
- `WordToken`
- `SpeakerTurn`
- `Shot`
- `CandidateClip`
- `ClipScore`
- `CropPlan`
- `SubtitleTrack`
- `RenderPlan`
- `ExportedClip`

Règle : toute couche du système doit échanger via ces objets ou des structures voisines, pas via des dictionnaires informels partout.

## 5.6 `src/sceneqora/app/`

Couche d’orchestration applicative.

Responsable de :
- l’enchaînement des étapes ;
- la reprise d’un job ;
- l’exécution conditionnelle d’étapes ;
- la coordination des modules.

Règle : cette couche orchestre, mais ne doit pas porter la logique détaillée des algorithmes.

## 5.7 `src/sceneqora/ingestion/`

Responsable de l’ouverture et de l’inspection des médias.

Exemples :
- lecture des métadonnées vidéo ;
- extraction audio ;
- génération de proxy ;
- validation du format d’entrée.

## 5.8 `src/sceneqora/transcription/`

Responsable de :
- la transcription ;
- l’alignement mot à mot ;
- la diarisation ;
- la normalisation des sorties vers le domaine interne.

Règle : les différences entre Whisper, WhisperX ou autres doivent être absorbées par des adapters.

## 5.9 `src/sceneqora/segmentation/`

Responsable de la génération de candidats.

Exemples :
- détection de changements de plan ;
- détection de silences ;
- construction de fenêtres candidates ;
- fusion ou suppression de doublons.

## 5.10 `src/sceneqora/scoring/`

Responsable de l’évaluation des extraits.

Le scoring doit rester **composable**.

Il faut pouvoir calculer séparément :
- score sémantique ;
- score audio ;
- score visuel ;
- score de nouveauté ;
- score de compatibilité short-form.

Puis fusionner via une politique claire.

## 5.11 `src/sceneqora/tracking/`

Responsable de l’identification du sujet principal et de la trajectoire de crop.

Exemples :
- détection de visages ;
- tracking du sujet ;
- fallback saliency ;
- lissage de trajectoire.

## 5.12 `src/sceneqora/subtitles/`

Responsable de la logique de sous-titrage dynamique.

Exemples :
- segmentation en lignes ;
- timing des mots ;
- styles ;
- templates ASS ;
- règles de mise en avant du mot courant.

## 5.13 `src/sceneqora/rendering/`

Responsable de la production vidéo finale.

Exemples :
- découpe propre ;
- composition verticale ;
- brûlage des sous-titres ;
- export final ;
- génération de variantes.

## 5.14 `src/sceneqora/integrations/`

Responsable des connexions vers des systèmes externes.

Exemples :
- client ComfyUI ;
- client LLM ;
- futurs services externes.

Règle : aucune dépendance externe complexe ne doit contaminer le cœur métier.

## 5.15 `src/sceneqora/infra/`

Regroupe les briques transverses techniques.

Exemples :
- chargement de configuration ;
- gestion des chemins ;
- logging ;
- wrappers subprocess ;
- cache local.

## 5.16 `src/sceneqora/observability/`

Responsable des signaux de suivi.

Exemples :
- métriques d’étapes ;
- temps de traitement ;
- ratios d’échec ;
- rapports d’analyse ;
- scoring breakdown par clip.

---

## 6. Flux de pipeline cible

Le pipeline cible doit respecter ce flux logique :

```text
ingestion
  -> transcription
  -> segmentation
  -> scoring
  -> sélection
  -> tracking / crop planning
  -> subtitles planning
  -> rendering
  -> export + manifest
```

### Artefacts attendus par étape

1. **Ingestion**
   - metadata.json
   - audio.wav
   - proxy.mp4

2. **Transcription**
   - transcript.json
   - words.json
   - speakers.json

3. **Segmentation**
   - shots.json
   - candidate_clips.json

4. **Scoring**
   - clip_scores.json
   - ranking.json

5. **Tracking / crop**
   - crop_plan.json

6. **Subtitles**
   - subtitles.ass
   - subtitles_preview.json

7. **Rendering**
   - ffmpeg_plan.json
   - output.mp4

8. **Final**
   - manifest.json

---

## 7. Contrats métier recommandés

Les contrats ci-dessous doivent exister explicitement sous forme de modèles typés.

## 7.1 `CandidateClip`

Doit contenir au minimum :
- `id`
- `source_video_id`
- `start_sec`
- `end_sec`
- `duration_sec`
- `transcript_excerpt`
- `speaker_ids`
- `source_signals`

## 7.2 `ClipScore`

Doit contenir :
- `candidate_clip_id`
- `semantic_score`
- `audio_score`
- `visual_score`
- `novelty_score`
- `short_form_score`
- `final_score`
- `score_reasoning`

## 7.3 `CropPlan`

Doit contenir :
- `clip_id`
- `target_aspect_ratio`
- `crop_keyframes`
- `tracking_source`
- `fallback_mode`
- `smoothing_params`

## 7.4 `RenderPlan`

Doit contenir :
- `clip_id`
- `input_master_path`
- `start_sec`
- `end_sec`
- `output_resolution`
- `crop_plan_ref`
- `subtitle_track_ref`
- `ffmpeg_filters`
- `export_profile`

---

## 8. Conventions de nommage

## 8.1 Fichiers et modules

Préférer :
- `snake_case.py` pour les fichiers
- noms explicites et métier

Exemples corrects :
- `candidate_builder.py`
- `vertical_reframe.py`
- `clip_scoring.yaml`

À éviter :
- `helpers.py`
- `misc.py`
- `final_utils.py`
- `new_pipeline.py`

## 8.2 Classes

Préférer des noms métier lisibles :
- `CandidateClip`
- `ClipScoringService`
- `VerticalReframeEngine`

## 8.3 Fonctions

Une fonction doit décrire une action claire :
- `build_candidate_clips`
- `score_candidate_clip`
- `generate_crop_plan`
- `render_vertical_clip`

---

## 9. Règles d’implémentation

## 9.1 Une étape = une responsabilité claire

Un module ne doit pas mélanger :
- détection de candidats ;
- scoring ;
- rendu final.

## 9.2 Pas de logique opaque dans la CLI

La CLI doit uniquement :
- parser les arguments ;
- charger la config ;
- déclencher les services applicatifs.

## 9.3 Les wrappers externes doivent être isolés

Tout appel à :
- FFmpeg
- WhisperX
- ComfyUI
- modèles externes
- API LLM

... doit passer par une couche dédiée, jamais être dispersé dans tout le code.

## 9.4 Les objets intermédiaires doivent être persistables

Tout résultat important doit pouvoir être :
- sérialisé ;
- relu ;
- rejoué.

## 9.5 Le pipeline doit être relançable partiellement

Le design doit permettre de :
- recalculer le scoring sans refaire la transcription ;
- rerendre un clip sans refaire toute l’analyse ;
- régénérer un style de sous-titre sans rescanner la vidéo.

---

## 10. Tests attendus

La structure du projet doit encourager 3 niveaux de tests.

## 10.1 Tests unitaires

Portent sur :
- calculs de score ;
- fusion de segments ;
- formatage de sous-titres ;
- règles de crop.

## 10.2 Tests d’intégration

Portent sur :
- adapter Whisper/WhisperX ;
- génération de fichiers ASS ;
- construction des commandes FFmpeg ;
- manifest final.

## 10.3 Tests end-to-end

Portent sur un petit fixture vidéo et vérifient :
- exécution du pipeline ;
- production des artefacts ;
- présence d’au moins un clip exporté ;
- cohérence du manifest.

## 10.4 Live tests

En plus des tests déterministes, certains tickets devront prévoir un **live test local** sur un échantillon réaliste pour vérifier :
- la robustesse du pipeline ;
- les temps de traitement ;
- la qualité du recadrage ;
- la lisibilité des sous-titres ;
- la pertinence du scoring.

---

## 11. Stratégie de configuration

La configuration doit être hiérarchique.

Exemple :
- `default.yaml` pour les valeurs globales ;
- `profiles/documentary.yaml` pour les overrides d’un documentaire ;
- un éventuel fichier runtime pour surcharges locales.

Les catégories attendues :
- `ingestion`
- `transcription`
- `segmentation`
- `scoring`
- `tracking`
- `subtitles`
- `rendering`
- `observability`

---

## 12. Manifest final recommandé

Chaque exécution doit produire un `manifest.json` lisible et exploitable.

Il doit contenir au minimum :
- identifiant du job ;
- vidéo source ;
- profil utilisé ;
- date d’exécution ;
- durée source ;
- liste des clips exportés ;
- score détaillé de chaque clip ;
- chemins des artefacts ;
- versions des composants majeurs ;
- erreurs ou warnings éventuels.

Ce manifest devient la source de vérité du pipeline.

---

## 13. Roadmap structurelle recommandée

## Phase 1 — Squelette repo

Objectif : poser une base saine.

À obtenir :
- arborescence minimale ;
- packaging Python ;
- config loader ;
- CLI de base ;
- modèles de domaine ;
- manifest minimal.

## Phase 2 — Ingestion + transcription

À obtenir :
- extraction audio ;
- probe vidéo ;
- transcription normalisée ;
- persistance des artefacts.

## Phase 3 — Segmentation + scoring MVP

À obtenir :
- candidats simples ;
- score heuristique initial ;
- ranking.

## Phase 4 — Reframe vertical + sous-titres

À obtenir :
- crop plan ;
- génération ASS ;
- rendu vertical ;
- export MVP.

## Phase 5 — Durcissement produit

À obtenir :
- observabilité ;
- meilleure reprise sur erreur ;
- rapports ;
- profils de contenu ;
- live tests plus complets.

---

## 14. Ce qu’il faut éviter absolument

- un unique fichier géant qui orchestre tout ;
- des appels FFmpeg dispersés partout ;
- des dictionnaires non typés comme contrat principal ;
- de la logique métier cachée dans les scripts ;
- des sorties écrites dans des chemins arbitraires ;
- des modules “fourre-tout” ;
- une dépendance forte de l’architecture à un seul fournisseur ou à un seul modèle.

---

## 15. Définition de réussite

La structure du projet est considérée comme saine si :
- un nouveau contributeur comprend vite où placer un changement ;
- un ticket n’oblige pas à modifier 10 couches sans raison ;
- un clip peut être ré-exporté sans relancer toute la pipeline ;
- les artefacts intermédiaires sont inspectables ;
- le scoring est explicable ;
- le rendu est remplaçable sans casser l’analyse ;
- l’intégration future avec d’autres modèles reste possible.

---

## 16. Règle de gouvernance pour ce projet

Dans ce projet :
- **GPT** agit comme **architecte, reviewer, roadmap owner** ;
- **Codex / gemini-cli** gèrent l’implémentation locale et l’exécution du repo.

Ce guide doit donc être utilisé comme **référence d’alignement** pour :
- la création des tickets ;
- les revues d’architecture ;
- les revues de code ;
- l’évolution progressive du repo.

---

## 17. Résumé exécutable

Si un doute existe sur l’emplacement d’un nouveau composant, appliquer cette règle :

- **Est-ce du langage métier ?** → `domain/`
- **Est-ce de l’orchestration ?** → `app/`
- **Est-ce une étape d’analyse ?** → dossier métier dédié (`transcription/`, `segmentation/`, `scoring/`, `tracking/`)
- **Est-ce du rendu ?** → `rendering/` ou `subtitles/`
- **Est-ce un appel externe ?** → `integrations/`
- **Est-ce transversal et technique ?** → `infra/`
- **Est-ce de la doc d’architecture ou d’exploitation ?** → `docs/`

Ce document est la **structure cible de référence** de Sceneqora.
