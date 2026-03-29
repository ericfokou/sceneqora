# Titre
Etape 1_001 - Bootstrap repo minimal Sceneqora

## Identifiant
etape_1_001_bootstrap_repo_minimal

## Etape
Etape 1 - Bootstrap repo minimal et socle executable

## Contexte / Probleme
Le dossier `sceneqora/` contient aujourd'hui les documents de cadrage principaux (`guide.md`, `sceneqora_codex_builder.md`, `sceneqora_gpt_5_4_architect.md`, `sceneqora_ticket.md`), mais il ne constitue pas encore un repo operationnel :
- pas de depot Git ;
- pas de structure Python ;
- pas de packaging ;
- pas de CLI ;
- pas de Makefile ;
- pas de `plan.md` local.

Cette situation bloque le workflow normal defini par les documents de gouvernance.

## Objectif
Transformer `sceneqora/` en repo Python minimal executable, proprement structure, sans ouvrir encore les chantiers metier video/IA.

## Frontiere du ticket
A la fin du ticket, on doit disposer d'un socle repo minimal permettant :
- d'avoir un depot Git initialise localement ;
- d'avoir une structure de base alignee avec `guide.md` ;
- d'executer une CLI minimale ;
- d'executer des checks de base ;
- d'avoir un `plan.md` minimal local pour cadrer les etapes.

Le ticket s'arrete au socle.
Aucune logique pipeline metier n'est attendue.

## Perimetre
Inclus :
- initialisation du depot Git local si absent ;
- creation des fichiers racine minimaux :
  - `README.md`
  - `pyproject.toml`
  - `.gitignore`
  - `.env.example`
  - `Makefile`
  - `plan.md`
- creation de l'arborescence minimale utile :
  - `src/sceneqora/`
  - `src/sceneqora/cli/`
  - `src/sceneqora/domain/`
  - `src/sceneqora/app/`
  - `src/sceneqora/infra/`
  - `tests/unit/`
  - `configs/`
  - `docs/`
  - `scripts/`
  - `outputs/`
- ajout des `__init__.py` minimaux necessaires ;
- ajout d'une CLI minimale de bootstrap ;
- ajout d'un test smoke ;
- ajout d'un premier `make check` simple et realiste pour ce stade.

## Hors perimetre
- ingestion video
- extraction audio
- FFmpeg
- transcription
- Whisper / WhisperX
- scoring
- tracking / crop
- sous-titres
- rendering
- integrations externes
- architecture avancee de config
- notebooks

## References
- `guide.md`
- `sceneqora_codex_builder.md`
- `sceneqora_gpt_5_4_architect.md`
- `sceneqora_ticket.md`

## Dependances / Pre-requis
- Python local disponible
- aucun code existant a reprendre
- depot Git absent au depart : ce ticket constitue l'exception bootstrap permettant de creer le repo local
- ne faire aucun commit / push / PR / merge a l'issue du ticket sans GO explicite

## Livrable visible attendu
Un repo local Sceneqora minimal, structure et executable, avec :
- une CLI de base qui repond correctement ;
- un `plan.md` present ;
- des checks de base executables ;
- un test smoke vert.

## Exigences fonctionnelles
- [ ] Le depot Git local est initialise si absent
- [ ] Le repo contient les fichiers racine minimaux du socle
- [ ] Le package Python `sceneqora` existe sous `src/`
- [ ] Une CLI minimale est executable
- [ ] Un `plan.md` minimal est cree
- [ ] Un test smoke valide le bootstrap
- [ ] `make check` fonctionne au niveau attendu pour ce ticket

## Contraintes techniques
- Python 3.10 minimum
- Solution simple, explicable, locale
- Pas d'elargissement de scope
- Pas de refactor transverse non justifie
- Ne pas creer de logique pipeline metier prematuree
- La CLI doit rester minimale
- Le `Makefile` doit rester simple et realiste pour ce stade
- Pas d'integration reelle externe dans ce ticket

## Artefacts / Outputs attendus
- [ ] Code
- [ ] Tests
- [ ] Structure repo minimale creee localement
- [ ] `plan.md` cree localement
- [ ] Documentation minimale de bootstrap si necessaire

## Contrats / Interfaces touches
- structure de base du package `sceneqora`
- point d'entree CLI minimal
- convention de chemins minimaux
- cibles `Makefile`
- outillage de base defini dans `pyproject.toml`

## Definition of Done (DoD)
- [ ] Le depot Git local est initialise si absent
- [ ] Le comportement attendu est implemente
- [ ] Le livrable visible du ticket est bien produit
- [ ] Les tests lies au ticket sont ajoutes
- [ ] `pytest` est vert sur le perimetre du ticket
- [ ] `ruff check` est vert sur le perimetre du ticket
- [ ] `make check` est execute en fin de ticket et est vert
- [ ] Le retour Codex est pret pour review GPT 5.4

## Strategie d'implementation
1. Initialiser le depot Git local si absent et confirmer l'etat de depart
2. Creer les fichiers racine minimaux et l'arborescence minimale
3. Poser le package Python Sceneqora et une CLI minimale executable
4. Ajouter un test smoke et l'outillage minimal (`pyproject.toml`, `Makefile`)
5. Executer les validations locales et remonter le resultat

## Cas limites
1. Le depot Git existe deja partiellement au moment d'executer le ticket
2. La CLI minimale est presente mais non executable depuis la structure choisie
3. `make check` est trop ambitieux pour ce stade et doit rester borne au socle minimal

## Criteres de verification
```bash
git status
pytest
ruff check .
make check
python -m sceneqora.cli.main --help
```

## Validation manuelle attendue
- verifier que la CLI affiche bien son aide ;
- verifier que `plan.md` est present ;
- verifier que la structure minimale du repo est en place ;
- verifier que les checks de base passent localement.

## Risques / Points d'attention
- confusion possible entre bootstrap repo et debut de pipeline metier ;
- risque de sur-construire l'outillage trop tot ;
- risque de rendre `make check` trop ambitieux pour ce stade ;
- attention a ne pas engager de sequence Git au-dela de l'initialisation locale sans GO explicite.

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
