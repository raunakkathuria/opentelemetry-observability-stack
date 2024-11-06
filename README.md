# OpenTelemetry Observability Stack

A minimal observability stack demonstrating distributed tracing, metrics, and logging using OpenTelemetry, Tempo, Prometheus, and Loki.

🔍 Complete observability stack demonstration using:
- OpenTelemetry for instrumentation
- Prometheus for metrics
- Loki for logs
- Tempo for distributed tracing
- Grafana for visualization

✨ Features:
- Docker Compose setup for quick deployment
- Python demo app generating sample telemetry
- Pre-configured collectors and exporters
- Unified visualization in Grafana
- Production-ready configurations

🎯 Perfect for:
- Learning observability concepts
- Testing OpenTelemetry setup
- Prototyping monitoring solutions
- Understanding telemetry pipelines

📚 Includes comprehensive documentation and best practices for observability implementation.

## Architecture

### Components

1. **Tempo**
   - Distributed tracing backend
   - Receives traces via OTLP/gRPC
   - Port 4317: OTLP gRPC receiver
   - Port 3200: Query frontend

2. **Prometheus**
   - Time-series database for metrics
   - Port 9090: HTTP API and UI

3. **Loki**
   - Log aggregation system
   - Port 3100: HTTP API

4. **Grafana**
   - Unified visualization platform
   - Port 3000: Web UI
   - Default access: Anonymous auth enabled

5. **Demo Application**
   - Python application generating:
     * Traces using OpenTelemetry
     * Metrics
     * Logs

### Data Flow

```
Traces:
Application → Tempo (4317/gRPC)

Metrics:
Application → Prometheus (9090)

Logs:
Application → Files → Promtail → Loki
```

## Setup

1. Start the stack:
```bash
mkdir -p logs
docker-compose up -d
```

2. Access Grafana at http://localhost:3000

3. Configure Data Sources in Grafana:

   **Tempo:**
   - URL: http://tempo:3200
   - No authentication required

   **Prometheus:**
   - URL: http://prometheus:9090
   - No authentication required

   **Loki:**
   - URL: http://loki:3100
   - No authentication required

## Viewing Data

1. **Traces**
   - Go to Explore → Tempo
   - Click Search
   - Filter by service name: "dummy-data-generator"

2. **Metrics**
   - Go to Explore → Prometheus
   - Query examples:
     * `request_count`
     * `processing_time_bucket`

3. **Logs**
   - Go to Explore → Loki
   - Query: `{job="dummy-data-generator"}`

## Configuration Files

- `tempo.yaml`: Tempo configuration
  * OTLP receiver settings
  * Storage configuration
  * Query frontend settings

- `prometheus.yml`: Prometheus configuration
  * Scrape configurations
  * Target endpoints

- `docker-compose.yml`: Service definitions
  * Container configurations
  * Port mappings
  * Volume mounts
  * Network settings

## Project Structure

```
.
├── docker-compose.yml      # Service definitions
├── tempo.yaml              # Tempo configuration
├── prometheus.yml          # Prometheus configuration
├── loki-config.yaml        # Loki configuration
├── promtail-config.yaml    # Promtail log collection config
├── Dockerfile              # Python application container
├── dummy_data_generator.py # Demo application
└── requirements.txt        # Python dependencies
```

## Features

- Distributed tracing with Tempo
- Metric collection with Prometheus
- Log aggregation with Loki
- Unified visualization in Grafana
- Demo application generating telemetry data
- Docker Compose for easy deployment

## Troubleshooting

1. **Missing Traces**
   - Verify Tempo is running: `docker-compose ps tempo`
   - Check application OTLP endpoint configuration
   - Verify Grafana Tempo data source configuration

2. **Missing Metrics**
   - Check Prometheus targets: http://localhost:9090/targets
   - Verify metric exposition
   - Check Grafana Prometheus data source

3. **Missing Logs**
   - Verify log file creation
   - Check Promtail configuration
   - Verify Loki ingestion
