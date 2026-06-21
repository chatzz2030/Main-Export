# Module 6 — Document Export Engine

Converts a video synopsis (JSON produced by the AI Summarization Engine — Module 5) into a downloadable, branded **PDF** or **DOCX** file.

Part of the **Video Synopsis AI** project — Symbiosys Technologies internship, 7-module system.

---

## What this module does

- Pulls a synopsis document from **MongoDB** by ID and exports it (production route)
- Accepts a raw synopsis JSON directly and exports it (testing/QA route — no DB needed)
- Renders both formats from the same data using Jinja2 (PDF) and python-docx (DOCX), styled with the project's brand color (`#1a73e8`)

---

## Tech stack

| Purpose | Library |
|---|---|
| API framework | FastAPI + Uvicorn |
| PDF rendering | WeasyPrint (HTML/CSS → PDF) |
| DOCX rendering | python-docx |
| Templating | Jinja2 (autoescaped) |
| Database | MongoDB via Motor (async driver) |
| Containerization | Docker + Docker Compose |

---

## Project structure

```
.
├── main.py               # FastAPI app — all routes, schema, rendering logic
├── requirements.txt      # Python dependencies (pinned)
├── Dockerfile            # Builds the API image
├── docker-compose.yml    # Runs the API + a local MongoDB together
└── sample_input.json     # Example synopsis matching Module 5's exact output schema
```

All five files must sit in the **same folder** — Docker Compose looks for `docker-compose.yml` in the current directory.

---

## Prerequisites

- **Docker Desktop** installed and running — [docker.com/get-started](https://www.docker.com/get-started)
- That's it. Python, MongoDB, and all dependencies run inside containers — nothing else needs to be installed on your machine.

---

## Running it

**1. Open a terminal in this folder.**

**2. Build and start everything:**
```bash
docker compose up --build
```
This builds the API image (Python + WeasyPrint's system libraries), pulls and starts a MongoDB container, and starts the FastAPI app. First run takes a few minutes; later runs are fast since layers are cached.

**3. Confirm it's running.**
Logs should end with:
```
Uvicorn running on http://0.0.0.0:8000
```
Leave this terminal open — closing it stops the containers.

**4. Open the interactive API docs:**
```
http://localhost:8000/docs
```

**5. Stop everything when done** (new terminal tab, same folder):
```bash
docker compose down
```
Add `-v` at the end (`docker compose down -v`) if you also want to wipe the MongoDB data volume.

---

## Environment variables

Set in `docker-compose.yml` under `export-api: environment:`. Override them there if your setup differs.

| Variable | Default | Purpose |
|---|---|---|
| `MONGO_URI` | `mongodb://mongo:27017` | Connection string (points at the `mongo` container by service name) |
| `MONGO_DB_NAME` | `video_synopsis_ai` | Database name — confirm with Module 1/4 |
| `MONGO_COLLECTION` | `synopses` | Collection name — confirm with Module 1/4 |

---

## API endpoints

| Method | Route | Use case |
|---|---|---|
| `GET` | `/api/v1/synopsis/{synopsis_id}/download?format=pdf\|docx` | **Production.** Fetches the document from MongoDB by `_id` and exports it. This is what the frontend calls. |
| `POST` | `/api/export/pdf` | **Testing.** Send the raw synopsis JSON directly (see `sample_input.json`). No database needed. |
| `POST` | `/api/export/docx` | Same as above, returns a `.docx` instead. |

### Expected input schema (from Module 5)

```json
{
  "video_metadata": {
    "title": "string",
    "video_url": "string",
    "channel_name": "string (optional)",
    "thumbnail_url": "string (optional)"
  },
  "summary": {
    "basic_summary": { "overall_synopsis": "string" },
    "topics_covered": { "title": "string", "topics": ["string"] },
    "detailed_summary": {
      "key_insights": ["string"],
      "action_items": ["string"],
      "topic_breakdown": [{ "topic": "string", "explanation": "string" }]
    },
    "closing_note": "string"
  }
}
```

If a stored MongoDB document doesn't match this shape, the route returns a `500` with a clear message naming the missing/invalid field — it won't silently produce a broken file.

---

## Testing without Postman

1. Go to `http://localhost:8000/docs`
2. Expand `POST /api/export/pdf` → **Try it out**
3. Paste the contents of `sample_input.json` into the request body
4. **Execute** → scroll down to the response → click the download link

Repeat for `/api/export/docx`.

To test the MongoDB-backed route, insert `sample_input.json` as a document into the `synopses` collection (e.g. via MongoDB Compass connected to `mongodb://localhost:27017`), copy its `_id`, then try `GET /api/v1/synopsis/{synopsis_id}/download?format=pdf` with that id.

---

## Troubleshooting

**`no configuration file provided: not found`**
`docker-compose.yml` isn't in your current folder, or got saved as `docker-compose.yml.txt`. Run `dir` (Windows) / `ls` (Mac/Linux) and check the exact filename; rename if needed.

**`Package 'libgdk-pixbuf2.0-0' has no installation candidate`**
Newer Debian base images renamed this package. The `Dockerfile` in this repo already uses the correct name (`libgdk-pixbuf-2.0-0`) — make sure you're using the latest version of it.

**`'super' object has no attribute 'transform'` during PDF generation**
A known WeasyPrint bug: older WeasyPrint versions don't cap their internal `pydyf` dependency, so a fresh `pip install` can grab an incompatible `pydyf` release. Fixed by pinning `weasyprint==69.0` in `requirements.txt` (already done in this repo).

**Port 8000 already in use**
Something else on your machine is using that port. Either stop it, or change the left-hand side of the port mapping in `docker-compose.yml` (e.g. `"8001:8000"`) and use `http://localhost:8001` instead.

**Changes to `main.py` aren't showing up**
The container mounts your local folder and runs Uvicorn with `--reload`, so edits should reflect automatically. If they don't, run `docker compose restart export-api`.

---

## Notes for integration with other modules

- **Module 1 / 4 (Infra/DB):** confirm the real `MONGO_DB_NAME` / `MONGO_COLLECTION` values for production and update the environment variables above accordingly.
- **Module 5 (AI Engine):** `channel_name` and `thumbnail_url` are currently treated as optional since they weren't always present in sample data — confirm whether they'll be consistently populated in production.
- **Module 7 (QA):** the `POST /api/export/pdf` and `/api/export/docx` routes are the ones to hit directly in Postman/pytest — they don't require a live MongoDB connection.
