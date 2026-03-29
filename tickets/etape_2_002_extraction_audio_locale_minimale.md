# Titre
Etape 2_002 - Extraction audio locale minimale

## Identifiant
etape_2_002_extraction_audio_locale_minimale

## Etape
Etape 2 - Ingestion video minimale

## Contexte / Probleme
Sceneqora dispose maintenant d'un probe video local minimal, mais aucune brique reelle ne permet encore d'extraire l'audio d'une video locale dans un format simple et exploitable.

Avant toute transcription ou etape audio aval, il faut poser une capacite minimale, locale et bornee :
- lire une video locale ;
- extraire un unique artefact audio ;
- fixer une cible de sortie stable ;
- exposer cette extraction via une commande CLI simple ;
- verifier visiblement que le fichier audio attendu est bien genere.

Cette brique doit rester strictement centree sur l'extraction audio minimale, sans glisser vers une couche de traitement audio ou de pipeline.

## Objectif
Introduire une brique minimale d'extraction audio locale capable de prendre une video locale en entree et de generer un fichier WAV PCM mono 16 kHz via `ffmpeg`.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une brique minimale d'extraction audio locale via `ffmpeg` ;
- un appel externe isole proprement ;
- un point CLI simple dedie a l'extraction audio ;
- une sortie unique en WAV PCM mono 16 kHz ;
- un artefact visible genere localement ;
- des tests deterministes sans dependance obligatoire a `ffmpeg` reel ;
- un test live cible hors `make check`.

Le ticket s'arrete a l'extraction audio locale minimale.
Il n'ouvre ni transcription, ni traitement audio avance, ni enchainement multi-etapes.

## Perimetre
Inclus :
- lecture d'un chemin video local ;
- lecture d'un chemin de sortie cible ;
- extraction audio locale minimale via `ffmpeg` ;
- format de sortie unique : WAV PCM, mono, 16 kHz ;
- isolation propre de l'appel externe ;
- ajout d'une commande CLI simple dediee a l'extraction audio ;
- sortie lisible confirmant au minimum :
  - chemin source
  - chemin de sortie
  - sample rate
  - channels
  - format attendu
- ajout d'un contrat metier minimal uniquement si necessaire, strictement borne a l'artefact audio extrait ;
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- transcription
- diarisation
- proxy video
- segmentation
- scoring
- rendu
- pipeline multi-etapes
- batch
- plusieurs formats de sortie
- enrichissement large du manifest
- traitement audio avance
- normalisation ou mastering audio
- detection de parole
- toute logique aval de type STT

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_2_001_probe_video_local_minimal.md`

## Dependances / Pre-requis
- Etape 2 deja ouverte avec le probe video local minimal
- `ffmpeg` disponible localement pour le test live cible
- aucun autre outil externe requis
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple qui prend une video locale et un chemin de sortie, genere un fichier `.wav` reellement cree localement, puis affiche une sortie lisible confirmant au minimum :
- `source_path`
- `output_path`
- `sample_rate`
- `channels`
- `format`

## Exigences fonctionnelles
- [ ] Une video locale peut etre utilisee comme source d'extraction audio
- [ ] Un fichier audio WAV PCM mono 16 kHz est genere localement
- [ ] L'appel `ffmpeg` est isole proprement
- [ ] La CLI expose une commande simple dediee a l'extraction audio
- [ ] Une sortie visible confirme les informations minimales attendues
- [ ] Les tests deterministes couvrent l'extraction sans dependre de `ffmpeg` reel
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- `ffmpeg` utilise comme moteur d'extraction
- Sortie unique : WAV PCM mono 16 kHz
- Appel externe isole proprement
- Pas de dependance obligatoire a `ffmpeg` reel dans `pytest` / `make check`
- Seul le test live hors `make check` depend de `ffmpeg` reel
- Pas de transcription
- Pas de pipeline multi-etapes
- Pas de surconstruction

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Fichier `.wav` reellement genere localement
- [ ] Sortie visible lisible de confirmation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale d'extraction audio locale
- isolation de l'appel `ffmpeg`
- commande CLI d'extraction audio
- eventuel contrat metier minimal borne a l'artefact audio extrait
- format de sortie visible de confirmation

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
1. Definir la frontiere exacte de l'extraction audio minimale et l'eventuel contrat borne a l'artefact
2. Ajouter une brique minimale d'extraction audio basee sur `ffmpeg`
3. Isoler l'appel externe et fixer les parametres de sortie WAV PCM mono 16 kHz
4. Etendre la CLI avec une commande simple d'extraction audio
5. Ajouter les tests deterministes, puis executer le test live cible hors `make check`

## Cas limites
1. Le chemin source n'existe pas ou ne pointe pas vers une video exploitable
2. Le chemin de sortie est invalide ou non accessible en ecriture
3. `ffmpeg` echoue ou la sortie n'est pas produite dans le format attendu

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
python -m sceneqora.cli.main extract-audio /chemin/vers/video.mp4 /chemin/vers/output.wav
```

Les tests executes dans `pytest` et `make check` ne doivent pas dependre de la presence reelle de `ffmpeg`.
Ils doivent mocker l'appel externe ou rejouer une execution capturee.
Seul le test live cible hors `make check` depend de `ffmpeg` reel.

## Validation manuelle attendue
- verifier que la commande CLI genere bien un fichier `.wav` local ;
- verifier que le format cible reste WAV PCM mono 16 kHz ;
- verifier que la sortie visible confirme au minimum le chemin source, le chemin de sortie, le sample rate, le nombre de canaux et le format ;
- verifier qu'il n'y a aucun glissement vers transcription ou pipeline ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de glisser de l'extraction audio vers une pre-transcription implicite ;
- risque d'ouvrir trop tot des formats ou options multiples ;
- risque de melanger subprocess, logique CLI et logique metier ;
- risque de rendre les tests non deterministes s'ils dependent de `ffmpeg` reel ;
- risque de sur-modeliser l'artefact audio extrait.

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
