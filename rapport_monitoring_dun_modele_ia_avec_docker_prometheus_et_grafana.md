# Rapport de Projet

## Monitoring d’un modèle d’Intelligence Artificielle avec Docker, Prometheus et Grafana

---

### Présenté par
- **Mariem Mohamed El Bechir** – C34606  
- **Mohamed Salem Ebnou Echvagha Oubeid** – C34613

### Encadré par
- **Dr. Yacoub Maiga**

---

## 1. Introduction

Dans le cadre du module *Systèmes d’Exploitation*, ce projet vise à concevoir et déployer une architecture complète permettant le **monitoring en temps réel d’un service d’Intelligence Artificielle**. L’objectif principal est de mettre en pratique les concepts fondamentaux des systèmes d’exploitation (gestion des ressources, isolation, performance, supervision) à travers des technologies modernes telles que **Docker**, **Prometheus**, **Grafana**, **cAdvisor** et **WSL**.

Le système développé expose une **API IA** (FastAPI) instrumentée avec des métriques Prometheus, puis surveillée via des dashboards Grafana.

---

## 2. Architecture Générale du Système

L’architecture du projet repose sur les composants suivants :

- **API IA (FastAPI)** : service exposant un endpoint `/predict`
- **Prometheus** : collecte des métriques
- **Grafana** : visualisation des métriques
- **cAdvisor** : surveillance des conteneurs Docker
- **Docker & Docker Compose** : orchestration
- **WSL 2** : couche de virtualisation Linux sous Windows

Flux général :

Client → API IA → Métriques → Prometheus → Grafana

---

## 3. Environnement de Développement

### 3.1 Système
- Windows 11
- **WSL 2** (Windows Subsystem for Linux)
- Docker Desktop

### 3.2 Rôle de WSL

WSL permet d’exécuter un noyau Linux réel sous Windows, indispensable pour le bon fonctionnement de Docker Desktop.

Commandes de vérification utilisées :
- `wsl --status`
- `docker ps`
- `docker compose version`

---

## 4. Structure du Projet (VS Code)

```
os-ai-monitoring-project/
├── ai-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── model.py
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   └── ai-monitoring.json
│   │   └── provisioning/
│   │       ├── dashboards.yml
│   │       └── datasource.yml
│
├── docker-compose.yml
└── README.md
```

---

## 5. Mise en place de Docker

### 5.1 Installation

- Installation de Docker Desktop via navigateur
- Activation du backend WSL 2

### 5.2 Difficultés rencontrées

❌ **Erreur** : Docker ne démarrait pas correctement  
✔️ **Solution** : Activation de WSL et redémarrage du système

---

## 6. Déploiement des Conteneurs

Les services suivants sont lancés via `docker-compose` :

- ai-service
- prometheus
- grafana
- cadvisor

Commande utilisée :
```
docker compose up -d
```

Vérification :
```
docker compose ps
```

Tous les services sont en état **UP**.

---

## 7. API IA et Swagger

### 7.1 Description

L’API IA est développée avec **FastAPI** et expose :
- `/health`
- `/predict`
- `/metrics` (Prometheus)

### 7.2 Swagger UI

Accessible via :
```
http://localhost:8000/docs
```

Cela permet de tester manuellement les requêtes POST `/predict`.

---

## 8. Prometheus

### 8.1 Rôle

Prometheus collecte périodiquement les métriques exposées par :
- API IA
- cAdvisor
- Prometheus lui-même

### 8.2 Vérification

Dans l’interface Prometheus :
- Status → Targets
- Tous les targets sont **UP**

Exemples de métriques :
- `api_requests_total`
- `api_request_latency_seconds_bucket`
- `container_memory_working_set_bytes`

---

## 9. cAdvisor

cAdvisor fournit des métriques détaillées sur :
- CPU
- Mémoire
- Conteneurs Docker

Accessible via :
```
http://localhost:8080
```

Il permet de visualiser l’impact réel de la charge sur les ressources système.

---

## 10. Grafana Dashboard

### 10.1 Dashboards

Un dashboard personnalisé a été créé avec les panels suivants :

- API request rate (/predict)
- p95 API latency
- Container CPU usage
- Container memory working set

### 10.2 Génération de charge

Une charge a été générée via PowerShell :

```
for ($i=0; $i -lt 200; $i++) {
  Invoke-RestMethod -Method POST "http://localhost:8000/predict" \
    -ContentType "application/json" \
    -Body '{"text":"great work"}' | Out-Null
}
```

Les graphiques montrent clairement :
- Augmentation du débit
- Hausse de la latence p95
- Pics CPU
- Mémoire stable

---

## 11. Difficultés Rencontrées et Solutions

### 11.1 Problème scikit-learn / numpy dans VS Code

❌ Imports non résolus dans l’éditeur  
✔️ Résolu en déléguant l’exécution réelle à Docker (environnement isolé)

---

### 11.2 `curl` non disponible dans Git Bash

❌ Commande `curl` non reconnue  
✔️ Utilisation de PowerShell (`Invoke-RestMethod`)

---

### 11.3 Grafana affichait “No data”

❌ Requêtes PromQL incorrectes  
✔️ Correction des métriques et labels

---

## 12. Apports du Projet (Lien avec les OS)

Ce projet illustre concrètement :

- Isolation des processus (Docker)
- Gestion CPU et mémoire
- Supervision système
- Performance sous charge
- Virtualisation (WSL)

---

## 13. Perspectives et Améliorations Futures

Ce projet servira de base pour :

- Monitoring de modèles IA plus complexes
- Ajout d’alertes Grafana
- Déploiement cloud
- CI/CD
- Tests de charge avancés

Un dépôt **GitHub** sera créé pour continuer l’évolution du projet.

---

## 14. Conclusion

Ce projet démontre l’intégration réussie des concepts des systèmes d’exploitation avec des outils modernes de monitoring afin d’analyser les performances d’un service d’intelligence artificielle dans un environnement conteneurisé.

Il constitue une base solide pour des projets IA industriels et académiques.

---

**Fin du rapport**

