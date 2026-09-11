from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_docker_compose_defines_core_services():
    compose_path = PROJECT_ROOT / "docker-compose.yml"
    assert compose_path.exists()

    with compose_path.open(encoding="utf-8") as handle:
        compose = yaml.safe_load(handle)

    services = compose["services"]
    assert "redis" in services
    assert "backend" in services
    assert "frontend" in services
    assert services["backend"]["environment"]["REDIS_URL"] == "redis://redis:6379/0"


def test_backend_and_frontend_dockerfiles_exist():
    assert (PROJECT_ROOT / "backend" / "Dockerfile").exists()
    assert (PROJECT_ROOT / "frontend" / "phase4" / "Dockerfile").exists()
    assert (PROJECT_ROOT / "frontend" / "phase4" / "nginx.conf").exists()
