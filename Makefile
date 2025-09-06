.PHONY: setup dev run api ui test fmt lint

setup:
	cd apps/backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api:
	uvicorn app.main:app --reload --app-dir apps/backend/app --port 8080

ui:
	cd apps/ui && corepack enable && pnpm dev

fmt:
	cd apps/backend && ruff check --fix app && black app

test:
	cd apps/backend && pytest -q
