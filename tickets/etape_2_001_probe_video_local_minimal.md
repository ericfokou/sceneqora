# Titre
Etape 2_001 - Probe video local minimal

## Identifiant
etape_2_001_probe_video_local_minimal

## Etape
Etape 2 - Ingestion video minimale

## Contexte / Probleme
Le socle repo, la configuration minimale et les premiers contrats de bootstrap sont en place, mais Sceneqora ne dispose encore d'aucune brique media reelle.

Avant d'ouvrir une ingestion plus large, il faut poser une premiere capacite d'inspection video locale :
- lire un chemin de fichier video local ;
- interroger ses metadonnees de base ;
- les normaliser dans un contrat metier borne ;
- les exposer via une commande CLI simple et visible.

Cette premiere brique doit rester strictement limitee au probe d'entree, afin d'ouvrir l'etape media sans deriver vers un mini pipeline.

## Objectif
Introduire une brique minimale de probe video local capable d'inspecter un fichier video via `ffprobe`, de normaliser les metadonnees utiles dans un contrat metier `VideoAsset`, et de les afficher en JSON lisible via la CLI.

## Frontiere du ticket
A la fin du ticket, on doit disposer de :
- un contrat metier minimal `VideoAsset` strictement borne au probe d'entree ;
- une brique d'ingestion minimale capable d'inspecter un fichier video local ;
- une normalisation minimale des metadonnees dans un objet metier type ;
- un point CLI simple pour inspecter une video locale ;
- un livrable visible lisible en JSON normalise ;
- des tests locaux adaptes ;
- un test live cible hors `make check`.

Le ticket s'arrete au probe video.
Il n'ouvre ni extraction audio, ni orchestration pipeline reelle, ni etape media aval.

## Perimetre
Inclus :
- lecture d'un chemin video local ;
- appel minimal a `ffprobe` comme source de verite de l'inspection media ;
- isolation propre de l'appel externe dans une couche adaptee ;
- parsing des donnees `ffprobe` separe du contrat metier ;
- ajout d'un contrat metier `VideoAsset` strictement borne ;
- normalisation minimale des metadonnees utiles dans cet objet type ;
- ajout d'un point CLI simple d'inspection video locale ;
- sortie JSON normalisee et lisible ;
- tests unitaires et integration adaptes au probe, deterministes et independants de la presence reelle de `ffprobe` ;
- validation manuelle simple ;
- test live cible hors `make check`.

## Hors perimetre
- extraction audio
- proxy video
- FFmpeg de rendu
- transcription
- Whisper / WhisperX
- segmentation
- scoring
- tracking / crop
- sous-titres
- rendering
- orchestration pipeline reelle
- enrichissement large du manifest
- persistance d'artefacts multiples
- plusieurs contrats ingestion en parallele
- `Transcript`
- `CandidateClip`
- `ClipScore`
- `CropPlan`
- decisions de pipeline
- exports

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`
- `tickets/etape_1_002_config_contrats_manifest_minimal.md`

## Dependances / Pre-requis
- Etape 1 consideree comme suffisamment fermee
- socle repo, config minimale et CLI deja presents
- `ffprobe` disponible localement pour le test live cible
- aucun autre outil media requis dans ce ticket
- ne faire aucun commit / push / PR / merge avant validation GPT 5.4 du retour de ticket

## Livrable visible attendu
Une commande CLI simple qui prend un chemin video local et affiche un `VideoAsset` JSON normalise lisible contenant uniquement les champs autorises :
- `source_path`
- `filename`
- `duration_sec`
- `width`
- `height`
- `fps` si disponible
- `has_audio` si disponible
- `container` si disponible

## Exigences fonctionnelles
- [ ] Une video locale peut etre probee a partir de son chemin
- [ ] Les metadonnees minimales utiles sont lues via `ffprobe`
- [ ] Les metadonnees sont normalisees dans un contrat metier type `VideoAsset`
- [ ] La CLI expose une commande simple d'inspection video locale
- [ ] La sortie visible est un JSON normalise lisible
- [ ] Des tests unitaires / integration couvrent le probe avec mock ou rejeu d'une sortie `ffprobe` capturee
- [ ] Un test live cible hors `make check` est execute et documente

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- Ticket strictement borne au probe
- `ffprobe` privilegie comme source de verite
- Appel externe isole proprement
- Logique de parsing separee du contrat metier
- Pas de dispersion des appels subprocess
- Pas d'extraction audio
- Pas de rendu
- Pas d'ouverture de pipeline reel
- Pas d'enrichissement large du manifest
- Un seul contrat ingestion reel introduit dans ce ticket

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Sortie JSON visible lisible pour une video locale
- [ ] Documentation minimale si necessaire
- [ ] Notebook de validation du ticket

## Contrats / Interfaces touchés
- `VideoAsset` strictement borne au probe d'entree
- brique d'ingestion minimale pour l'inspection video locale
- isolation de l'appel `ffprobe`
- parsing / normalisation des metadonnees
- point d'entree CLI d'inspection video
- format JSON de sortie visible

## Champs autorisés dans `VideoAsset`
- `source_path`
- `filename`
- `duration_sec`
- `width`
- `height`
- `fps` si disponible
- `has_audio` si disponible
- `container` si disponible

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
1. Definir `VideoAsset` et la frontiere exacte du contrat metier de probe
2. Ajouter une brique minimale d'inspection video locale basee sur `ffprobe`
3. Separer l'appel externe, le parsing et la normalisation vers `VideoAsset`
4. Etendre la CLI avec une commande simple d'inspection video
5. Ajouter des tests locaux deterministes via mock ou rejeu d'une sortie `ffprobe` capturee, puis executer le test live cible hors `make check`

## Cas limites
1. Le chemin fourni n'existe pas ou ne pointe pas vers un fichier video exploitable
2. `ffprobe` retourne des champs partiels, par exemple `fps`, audio ou format indisponibles
3. Le probe fonctionne, mais la CLI produit un JSON non stabilise ou difficile a lire

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
python -m sceneqora.cli.main inspect-video /chemin/vers/video.mp4
```

Les tests executes dans `pytest` et `make check` ne doivent pas dependre de la presence reelle de `ffprobe`.
Ils doivent mocker l'appel externe ou rejouer une sortie `ffprobe` capturee.
Seul le test live cible hors `make check` depend de `ffprobe` reel.

## Validation manuelle attendue
- verifier qu'une video locale peut etre inspectee depuis la CLI ;
- verifier que la sortie est un JSON lisible ;
- verifier que seules les metadonnees autorisees de `VideoAsset` sont exposees ;
- verifier que le contrat `VideoAsset` reste borne au probe d'entree ;
- verifier que le test live cible est documente dans le retour.

## Risques / Points d'attention
- risque de deriver du probe vers une ingestion media trop large ;
- risque de melanger parsing media, subprocess et contrat metier ;
- risque de rendre `VideoAsset` trop riche trop tot ;
- risque de rendre les tests non deterministes s'ils dependent de `ffprobe` reel ;
- risque de rendre le ticket dependant d'un environnement sans `ffprobe` pour autre chose que le test live cible ;
- attention a ne pas enrichir le manifest au-dela du strict necessaire.

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
