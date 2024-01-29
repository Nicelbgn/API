# ProtoRH

### Introduction 

Ce projet est une API qui a pour but de mettre en place un nouvel outil pour la gestion de ses ressources humaines. Il s'agit d'un intermédiaire permettant au serveur frontal (front-end) et à la base de données (back-end) de travailler ensemble de manière harmonieuse.

### Installation Guide

Après avoir clone le projet :
   * Il faut creer la database qui sera lié au project
   * Remplacer les information de connexion dans le fichier protorh.env
   * Executer le fichier build.sh pour installer les packages du project et migrer ls tables dans la base de données
   * Après cela vous pouvez éxécuter le fichier run.sh pour lancer le project

### Use

   * le site est héberger sur le port 4242
   * Voici le lien pour faire les requetes en ajoutant les endpoints correspondants http://localhost:4242

### API Endpoints

### Users

| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /user/create | To return a new user|
| GET | /user/{id_user} | To return a intended user |
| POST | /connect | To return a token JWT |
| POST | /user/update | To return a update of user or admin |
| POST | /user/password | To return a new password |
| POST | /upload/{user_id} | To return a profil picture |


### RequestRH

| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /rh/msg/add | To return if the HR request was made|
| POST | /rh/msg/remove | Allows you to close the HR request |

### Department 

This is the set of endpoints that allow you to retrieve, add or remove a user from a group.

| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /id_departement/users/add | Adding user(s) to a department|
| POST | /id_departement/users/remove | Removing user(s) from a departmen |
| GET  | /id_departement/users/ | Retrieving users from a department |




### Technologies Used

   * Un environnement d'installation réalisé à l'aide de script shell
   * une base de donnée réalisée en Postgresql
   * Utilisation de SQLAlchemy pour liée des endpoints API et une base de données
   * Utilisation pydantic pour réaliser des models
   * Utilisation de fastapi pour réaliser une API
   * Utilisation d' uvicorn pour lancer son API
   * Utilisaation des JWT avec PyJWT
