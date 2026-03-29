# Titre
Etape 2_004 - Horodatage transcription audio minimal

## Identifiant
etape_2_004_horodatage_transcription_audio_minimal

## Etape
Etape 2 - Ingestion video minimale

## Contexte / Probleme
Sceneqora dispose maintenant d'une transcription audio locale minimale, mais aucune brique reelle ne permet encore de produire un artefact horodate simple et exploitable a partir d'un fichier audio local.

Avant d'ouvrir la generation de sous-titres ou la structuration plus riche du transcript, il faut poser une capacite minimale, locale et bornee :
- lire un fichier audio WAV local ;
- appeler un moteur STT local de facon isolee ;
- recuperer une liste minimale de segments horodates ;
- les serialiser dans un unique artefact JSON simple ;
- exposer ce comportement via une commande CLI visible.

Cette brique doit rester strictement centree sur l'horodatage minimal du transcript, sans glisser vers SRT/VTT, formatting de sous-titres ou pipeline multi-etapes.

## Objectif
Introduire une brique minimale d'horodatage de transcription audio locale capable de prendre un fichier WAV local en entree, d'obtenir des segments horodates minimaux via un moteur STT local isole proprement, et de generer un fichier `.json` local explicable.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une brique minimale de transcription audio horodatee locale ;
- un appel a un moteur STT local isole proprement ;
- une recuperation minimale de segments horodates ;
- un point CLI simple dedie ;
- une sortie unique en fichier `.json` local ;
- un artefact visible genere localement ;
- une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
  - `segment_count`
- un contenu JSON minimal avec :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
  - `segments`
- pour chaque segment :
  - `start`
  - `end`
  - `text`
- des tests deterministes sans dependance obligatoire a un moteur STT reel ni a un telechargement de modele ;
- un test live cible hors `make check`.

Le ticket s'arrete a l'horodatage minimal de transcription audio.
Il n'ouvre ni generation SRT/VTT, ni styling de sous-titres, ni structuration de transcript plus riche.

## Perimetre
Inclus :
- lecture d'un fichier audio local `.wav` ;
- lecture d'un chemin de sortie JSON cible ;
- appel a un moteur STT local isole derriere une interface / un adaptateur minimal ;
- recuperation minimale de segments horodates ;
- generation d'un unique fichier `.json` local UTF-8 ;
- ajout d'une commande CLI simple dediee a l'horodatage du transcript audio ;
- sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
  - `segment_count`
- contenu JSON minimal avec :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
  - `segments`
- segments limites a :
  - `start`
  - `end`
  - `text`
- ajout d'un contrat metier minimal uniquement si necessaire, strictement borne a cet artefact JSON ;
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- generation SRT
- generation VTT
- styling de sous-titres
- line wrapping avance
- word timestamps detailles
- confidence scoring
- diarisation
- traduction
- batch
- pipeline multi-etapes
- fusion avec la video
- post-traitement avance du texte
- edition / correction de transcript
- enrichissement large du manifest
- detection de langue avancee

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_2_002_extraction_audio_locale_minimale.md`
- `tickets/etape_2_003_transcription_audio_locale_minimale.md`

## Dependances / Pre-requis
- Etape 2 deja ouverte avec le probe video local minimal, l'extraction audio locale minimale et la transcription audio locale minimale
- un fichier audio WAV local exploitable en entree
- un moteur STT local disponible uniquement pour le test live cible
- aucun telechargement de modele requis dans `pytest` / `make check`
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple du type :

```bash
python -m sceneqora.cli.main transcribe-audio-timestamps /chemin/audio.wav /chemin/transcript_segments.json
```

Cette commande doit :
- creer reellement un fichier `.json` local ;
- afficher une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `engine`
  - `status`
  - `segment_count`

## Exigences fonctionnelles
- [ ] Un fichier WAV local peut etre utilise comme source
- [ ] Un JSON local horodate minimal est genere
- [ ] L'appel au moteur STT est isole proprement
- [ ] La CLI expose une commande simple dediee
- [ ] La sortie visible est stable et testable
- [ ] Les tests deterministes ne dependent pas d'un moteur STT reel
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- Entree unique : WAV local
- Sortie unique : JSON local
- JSON UTF-8
- Moteur STT isole derriere un adaptateur minimal
- Structure JSON minimale et explicable
- Segments limites a `start`, `end`, `text`
- Pas de dependance obligatoire au moteur reel dans `pytest`
- Pas de dependance obligatoire au moteur reel ni a un telechargement de modele dans `make check`
- Seul le test live hors `make check` depend d'un moteur reellement disponible localement
- Pas de sur-modelisation
- Pas de surconstruction

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Fichier `.json` reellement genere localement
- [ ] Sortie visible lisible de confirmation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale d'horodatage de transcription audio locale
- isolation de l'appel au moteur STT
- commande CLI de transcription audio horodatee
- eventuel contrat metier minimal borne a l'artefact JSON
- format JSON visible de confirmation et de segments

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
1. Definir la frontiere exacte de l'artefact JSON horodate minimal et l'eventuel contrat borne
2. Ajouter une brique minimale de transcription horodatee locale avec moteur STT isole derriere un adaptateur simple
3. Fixer la structure JSON minimale et limiter chaque segment a `start`, `end`, `text`
4. Etendre la CLI avec une commande `transcribe-audio-timestamps` et une sortie visible stable
5. Ajouter les tests deterministes, puis executer et documenter le test live cible hors `make check`

## Cas limites
1. La source audio n'existe pas ou ne pointe pas vers un fichier WAV exploitable
2. Le chemin de sortie est invalide ou non accessible en ecriture
3. Le moteur STT est indisponible ou echoue pendant l'horodatage
4. Aucun segment n'est produit
5. La sortie JSON n'est pas produite ou est invalide

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
python -m sceneqora.cli.main transcribe-audio-timestamps /chemin/audio.wav /chemin/transcript_segments.json
```

Les tests executes dans `pytest` et `make check` ne doivent pas dependre d'un moteur STT reel ni d'un telechargement de modele.
Ils doivent mocker l'appel externe ou rejouer une execution capturee.
Seul le test live cible hors `make check` depend d'un moteur reellement disponible localement.

## Validation manuelle attendue
- verifier que la commande CLI genere bien un fichier `.json` local ;
- verifier que la sortie visible confirme au minimum le chemin source, le chemin de sortie, le format, le moteur, le statut et le nombre de segments ;
- verifier que le JSON genere reste minimal et explicable ;
- verifier que chaque segment est strictement limite a `start`, `end`, `text` ;
- verifier qu'il n'y a aucun glissement vers SRT/VTT, styling de sous-titres ou pipeline ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de glisser de l'horodatage minimal vers une generation implicite de sous-titres ;
- risque d'ouvrir trop tot des structures de transcript trop riches ;
- risque de melanger logique CLI, logique metier et appel externe ;
- risque d'introduire une dependance reelle a un moteur ou a un modele dans `pytest` / `make check` ;
- risque de sur-modeliser les segments ou d'ajouter des champs non demandes ;
- attention a ne pas ouvrir SRT/VTT dans ce ticket.

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
