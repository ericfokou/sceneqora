# Titre
Etape 2_005 - Generation SRT minimale

## Identifiant
etape_2_005_generation_srt_minimale

## Etape
Etape 2 - Ingestion video minimale

## Contexte / Probleme
Sceneqora dispose maintenant d'un JSON horodate minimal issu de la transcription audio, mais aucune brique reelle ne permet encore de le convertir en sous-titres SRT locaux exploitables.

Avant d'ouvrir VTT, le styling, le wrapping avance ou le burn-in video, il faut poser une capacite minimale, locale et bornee :
- lire un fichier JSON horodate local ;
- valider minimalement sa structure ;
- convertir chaque segment en bloc SRT simple ;
- generer un unique fichier `.srt` local ;
- exposer ce comportement via une commande CLI visible.

Cette brique doit rester strictement centree sur la generation SRT minimale, sans glisser vers des formats plus riches ou une logique aval de rendu.

## Objectif
Introduire une brique minimale de generation SRT capable de prendre en entree un JSON horodate local issu de `etape_2_004`, de convertir ses segments en blocs SRT minimaux, et de generer un fichier `.srt` local UTF-8 exploitable.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- une brique minimale de conversion JSON horodate local -> SRT local ;
- une validation minimale de la structure d'entree attendue ;
- une conversion simple et deterministe des segments en blocs SRT ;
- un point CLI simple dedie ;
- une sortie unique en fichier `.srt` local UTF-8 ;
- un artefact visible genere localement ;
- une sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `status`
  - `subtitle_count`
- des tests deterministes dans `pytest` / `make check` ;
- un test live cible hors `make check`.

Le ticket s'arrete a la generation SRT minimale.
Il n'ouvre ni VTT, ni styling de sous-titres, ni wrapping avance, ni burn-in video.

## Perimetre
Inclus :
- lecture d'un fichier JSON local UTF-8 issu de `etape_2_004` ;
- validation minimale de la structure attendue ;
- structure d'entree attendue avec au minimum :
  - `segments`
- validation de chaque segment avec uniquement :
  - `start`
  - `end`
  - `text`
- conversion minimale segment -> bloc SRT ;
- generation d'un unique fichier `.srt` local UTF-8 ;
- ajout d'une commande CLI simple dediee a la generation SRT ;
- sortie visible stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `status`
  - `subtitle_count`
- tests unitaires / integration adaptes ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- generation VTT
- generation ASS
- styling de sous-titres
- wrapping avance
- decoupage intelligent de lignes
- resegmentation
- correction texte
- fusion video / burn-in
- batch
- pipeline multi-etapes
- edition manuelle
- offsets complexes
- support de formats plus riches
- enrichissement aval du transcript

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_2_003_transcription_audio_locale_minimale.md`
- `tickets/etape_2_004_horodatage_transcription_audio_minimal.md`

## Dependances / Pre-requis
- Etape 2 deja ouverte avec la transcription audio locale minimale et l'horodatage de transcription audio minimal
- un artefact JSON local reel issu de `etape_2_004` pour le test live cible
- aucun moteur STT reel requis pour `pytest` / `make check`
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple du type :

```bash
python -m sceneqora.cli.main generate-srt /chemin/transcript_segments.json /chemin/output.srt
```

Cette commande doit :
- creer reellement un fichier `.srt` local ;
- afficher une sortie JSON stable confirmant au minimum :
  - `source_path`
  - `output_path`
  - `format`
  - `status`
  - `subtitle_count`

## Structure d'entrée attendue
- JSON avec au minimum :
  - `segments`
- pour chaque segment :
  - `start`
  - `end`
  - `text`

## Structure de sortie attendue
- fichier `.srt` UTF-8
- chaque bloc contient :
  1. index
  2. plage temporelle au format SRT
  3. texte
  4. ligne vide

## Convention explicite
- si `segments` est vide, le fichier `.srt` est quand meme genere
- la CLI annonce `subtitle_count: 0`
- le `status` est explicite et coherent
- aucune logique avancee de reformatage du texte n'est ajoutee

## Exigences fonctionnelles
- [ ] Un JSON horodate minimal local peut etre utilise comme source
- [ ] Un fichier `.srt` local est genere
- [ ] La conversion segment -> bloc SRT est correcte
- [ ] La CLI expose une commande simple dediee
- [ ] La sortie visible est stable et testable
- [ ] Les tests sont deterministes
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- UTF-8 en entree et en sortie
- Format SRT minimal uniquement
- Entree unique : JSON horodate minimal local
- Sortie unique : SRT local
- Conversion simple, explicable, deterministe
- Pas de smart formatting
- Pas de sur-modelisation
- Pas de dependance a un moteur STT reel dans `pytest` / `make check`
- Le test live peut s'appuyer sur un artefact JSON local reel
- Pas de surconstruction

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Fichier `.srt` reellement genere localement
- [ ] Sortie visible lisible de confirmation
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- brique minimale de generation SRT locale
- validation minimale du JSON horodate d'entree
- commande CLI de generation SRT
- eventuel contrat minimal de retour de confirmation
- format SRT minimal en sortie

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
1. Definir la validation minimale du JSON d'entree et la convention de statut associee
2. Ajouter une brique minimale de conversion segment -> bloc SRT
3. Fixer le format de sortie SRT minimal et la sortie CLI stable
4. Ajouter la commande `generate-srt`
5. Ajouter les tests deterministes, puis executer et documenter le test live cible hors `make check`

## Cas limites
1. Le fichier source n'existe pas
2. Le JSON est invalide
3. La structure ne contient pas les champs attendus
4. Un segment est invalide (`start`, `end`, `text`)
5. `end < start`
6. Aucun segment n'est produit
7. Le fichier `.srt` n'est pas genere

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
python -m sceneqora.cli.main generate-srt /chemin/transcript_segments.json /chemin/output.srt
```

Les tests executes dans `pytest` et `make check` doivent rester deterministes.
Ils ne doivent dependre ni d'un moteur STT reel ni d'un telechargement de modele.
Le test live peut s'appuyer sur un artefact JSON local reel deja genere.

## Validation manuelle attendue
- verifier que la commande CLI genere bien un fichier `.srt` local ;
- verifier que la sortie visible confirme au minimum le chemin source, le chemin de sortie, le format, le statut et le nombre de sous-titres ;
- verifier que chaque bloc SRT contient bien index, plage temporelle, texte et ligne vide ;
- verifier que le cas `segments` vide genere bien un fichier `.srt` avec `subtitle_count: 0` ;
- verifier qu'il n'y a aucun glissement vers VTT, styling, wrapping avance ou burn-in ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de glisser de la generation SRT minimale vers une logique implicite de formatting intelligent ;
- risque d'ouvrir trop tot VTT ou d'autres formats riches ;
- risque de melanger validation d'entree, logique CLI et ecriture SRT ;
- risque de sur-modeliser l'artefact ou la sortie de confirmation ;
- attention a garder la conversion strictement deterministe et explicable.

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
