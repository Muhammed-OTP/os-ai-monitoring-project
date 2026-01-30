# Projet OS: IA dans Docker + Monitoring (Prometheus/Grafana)

## Lancer le projet
```bash
cd os-ai-monitoring-project

docker compose up --build
```

## URLs
- API (Swagger): http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Démo rapide
```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"this is awesome"}'
```

## Dashboard Grafana
Un dashboard "AI in Docker - Monitoring (CPU/Mem/Latency)" est provisionné automatiquement.

## GPU (optionnel)
Décommentez le service **dcgm-exporter** dans `docker-compose.yml` + le job Prometheus dans `monitoring/prometheus/prometheus.yml`.
Nécessite une machine avec GPU NVIDIA + `nvidia-container-toolkit`.
