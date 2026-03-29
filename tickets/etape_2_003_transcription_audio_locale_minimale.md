# Titre
Etape 2_003 - Transcription audio locale minimale

## Identifiant
etape_2_003_transcription_audio_locale_minimale

## Etape
Etape 2 - Ingestion video minimale

## Contexte / Probleme
Sceneqora dispose maintenant d'une extraction audio locale minimale, mais aucune brique reelle ne permet encore de transcrire un fichier audio local dans une forme texte simple et exploitable.

Avant toute logique aval de type sous-titres, segmentation ou enrichissement de transcript, il faut poser une capacite minimale, locale et bornee :
- lire un fichier audio WAV local ;
- appeler un moteur STT local de facon isolee ;
- generer un unique artefact texte ;
- exposer cette transcription via une commande CLI simple ;
- verifier visiblement que le fichier texte attendu est bien genere.

Cette brique doit rester strictement centree sur la transcription audio locale minimale, sans glisser vers une couche de traitement de transcript ou de pipeline.

## Objectif
Introduire une brique minimale de transcription audio locale capable de prendre un fichier WAV local en entree et de generer un fichier texte `.txt` local via un moteur STT local isole proprement.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une brique minimale de transcription audio locale ;
- un appel a un moteur STT local isole proprement ;
- un point CLI simple dedie a la transcription audio ;
- une sortie unique en fichier `.txt` local ;
- un artefact visible genere localement ;
- une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
- des tests deterministes sans dependance obligatoire a un moteur STT reel ou a un telechargement de modele ;
- un test live cible hors `make check`.

Le ticket s'arrete a la transcription audio locale minimale.
Il n'ouvre ni diarisation, ni timestamps detailles, ni sous-titres, ni enchainement multi-etapes.

## Perimetre
Inclus :
- lecture d'un fichier audio local `.wav` ;
- lecture d'un chemin de sortie texte cible ;
- appel a un moteur STT local isole derriere une interface / un adaptateur minimal ;
- generation d'un unique fichier de sortie `.txt` ;
- ajout d'une commande CLI simple dediee a la transcription audio ;
- sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
- ajout d'un contrat metier minimal uniquement si necessaire, strictement borne a l'artefact texte genere ;
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- diarisation
- segmentation
- timestamps detailles
- word timestamps
- confidence scoring
- traduction
- sous-titres VTT/SRT
- batch
- pipeline multi-etapes
- enrichissement large du manifest
- fusion avec la video
- post-traitement avance du texte
- detection de langue avancee
- resumee ou structuration semantique
- toute logique aval de type clip selection

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_2_001_probe_video_local_minimal.md`
- `tickets/etape_2_002_extraction_audio_locale_minimale.md`

## Dependances / Pre-requis
- Etape 2 deja ouverte avec le probe video local minimal et l'extraction audio locale minimale
- un fichier audio WAV local exploitable en entree
- un moteur STT local disponible uniquement pour le test live cible
- aucun telechargement de modele requis dans `pytest` / `make check`
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple du type :

```bash
python -m sceneqora.cli.main transcribe-audio /chemin/audio.wav /chemin/transcript.txt
```

Cette commande doit :
- creer reellement un fichier `.txt` local ;
- afficher une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`

## Exigences fonctionnelles
- [ ] Un fichier WAV local peut etre utilise comme source de transcription
- [ ] Un transcript texte local `.txt` est genere
- [ ] L'appel au moteur STT est isole proprement
- [ ] La CLI expose une commande simple dediee a la transcription audio
- [ ] La sortie visible est stable et testable
- [ ] Les tests deterministes ne dependent pas d'un moteur STT reel
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- Entree unique : WAV local
- Sortie unique : TXT local
- Moteur STT isole derriere une interface / un adaptateur minimal
- CLI dediee
- Pas de dependance obligatoire au moteur reel dans `pytest` / `make check`
- Seul le test live hors `make check` depend d'un moteur STT reellement disponible localement
- Pas de sur-modelisation
- Pas de surconstruction

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Fichier `.txt` reellement genere localement
- [ ] Sortie visible lisible de confirmation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale de transcription audio locale
- isolation de l'appel au moteur STT
- commande CLI de transcription audio
- eventuel contrat metier minimal borne a l'artefact texte genere
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
1. Definir la frontiere exacte de la transcription audio minimale et l'eventuel contrat borne a l'artefact texte
2. Ajouter une brique minimale de transcription audio locale avec moteur STT isole derriere un adaptateur simple
3. Etendre la CLI avec une commande `transcribe-audio` et une sortie stable
4. Ajouter les tests deterministes sans moteur STT reel ni telechargement de modele
5. Executer et documenter le test live cible hors `make check`

## Cas limites
1. Le chemin source n'existe pas ou ne pointe pas vers un fichier WAV exploitable
2. Le chemin de sortie est invalide ou non accessible en ecriture
3. Le moteur STT echoue, n'est pas disponible localement, ou ne produit pas le fichier texte attendu

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
python -m sceneqora.cli.main transcribe-audio /chemin/audio.wav /chemin/transcript.txt
```

Les tests executes dans `pytest` et `make check` ne doivent pas dependre d'un moteur STT reel ni d'un telechargement de modele.
Ils doivent mocker l'appel externe ou rejouer une execution capturee.
Seul le test live cible hors `make check` depend d'un moteur STT reellement disponible localement.

## Validation manuelle attendue
- verifier que la commande CLI genere bien un fichier `.txt` local ;
- verifier que la sortie visible confirme au minimum le chemin source, le chemin de sortie, le format, le moteur et le statut ;
- verifier que l'appel au moteur STT reste isole proprement ;
- verifier qu'il n'y a aucun glissement vers diarisation, timestamps detailles, sous-titres ou pipeline ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de glisser de la transcription minimale vers un contrat de transcript trop riche trop tot ;
- risque d'introduire une dependance reelle a un moteur ou a un modele dans `pytest` / `make check` ;
- risque de melanger logique CLI, logique metier et appel externe ;
- risque d'ouvrir prematurement timestamps, segmentation ou formats de sortie multiples ;
- risque de sur-modeliser l'artefact texte genere.

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
