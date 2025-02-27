# Gestion de matériel pour l'association 803Z

Ce projet, développé en équipe, vise à fournir une application web pour la gestion du matériel de l'association 803Z. L'application permettra aux étudiants de consulter le matériel disponible et d'effectuer des réservations, tandis que les administrateurs pourront gérer ces réservations et le stock de matériel.

&nbsp;

![Exemple d'utilisation de l'application](https://www.adelie-ferre.miamo.fr/img/803z-02.gif)
&nbsp; *Exemple d'utilisation de l'application.*

&nbsp; 

## Fonctionnalités

- **Consultation du matériel disponible** : Les utilisateurs peuvent parcourir la liste du matériel et vérifier sa disponibilité.
- **Réservation en ligne** : Possibilité pour les membres de réserver du matériel directement via l'application.
- **Gestion administrative** : Les administrateurs peuvent ajouter, modifier ou supprimer des articles, ainsi que gérer les réservations en cours.
- **Authentification sécurisée** : Système de connexion pour différencier les droits des utilisateurs et des administrateurs.

&nbsp;

## Technologies utilisées

- **Back-end** : [Python](https://www.python.org/) avec le framework [Flask](https://flask.palletsprojects.com/)
- **Front-end** : [HTML](https://developer.mozilla.org/fr/docs/Web/HTML), [CSS](https://developer.mozilla.org/fr/docs/Web/CSS)
- **Base de données** : [SQLite](https://www.sqlite.org/)

&nbsp;

## Installation et lancement

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/L0R3Z/Location-materiel-803Z.git
   cd Location-materiel-803Z
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données** :
   ```bash
   python database.py
   ```

5. **Lancer l'application** :
   ```bash
   python app.py
   ```
   L'application sera accessible sur `http://127.0.0.1:5000/`.
   
&nbsp; 

## Structure du Projet

- `app.py` : Point d'entrée principal de l'application.
- `admin.py` : Gestion des routes et des fonctionnalités administratives.
- `reservation.py` : Gestion des réservations et des interactions utilisateur.
- `database.py` : Configuration et initialisation de la base de données.
- `templates/` : Dossiers contenant les templates HTML.
- `static/` : Dossier pour les fichiers statiques (CSS, JavaScript, images).

&nbsp;

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request pour proposer des améliorations ou signaler des problèmes.

&nbsp; 

## Remerciements

Merci à tous les membres de l'équipe projet et à l'association 803Z pour leur soutien et leurs retours constructifs.
