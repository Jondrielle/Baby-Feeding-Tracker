# Baby-Feeding-Tracker
A simple and intuitive app to help parents and caregivers keep track of a baby’s feeding schedule. You can log new feedings, update or delete past entries, and view a history of feed events.

# Project Structure 

<details>
  <summary>Project Layout</summary>
    
  ``` 
    feedingTracker/
    ├── .github/workflow # Github workflow
    │
    │ ├── backend/ # Application source code
    │ ├── init.py
    │ ├── main.py # FastAPI entrypoint
    │ ├── models.py # SQLAlchemy models (Feed, etc.)
    │ ├── schemas.py # Pydantic schemas
    │ ├── enums.py # enum feeding method
    │ ├── config.py # 
    │ ├── utils.py # oz_to_ml and ml_to_oz conversion methods  
    │ ├── routes/ # API route definitions
    │ │ ├── init.py
    │ │ └── feed.py
    │ └── database.py # DB session & engine config
    │
    ├── backend_tests/ # Automated tests
    │ ├── init.py
    │ ├── test_models.py
    │ ├── test_routes.py
    │ └── test_schemas.py
    │
    ├── frontend/ # Frontend folder
    │ ├── App.vue
    │ ├── main.js
    │ └── src/
    │   ├── assets/
    │   ├── components/
    │   ├── views/
    │   └── router/
    │     └── index.js
    │
    ├── requirements.txt # Python dependencies
    ├── README.md # Project documentation
    ├── .gitignore 
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env
    └── alembic/ # (Optional) migrations folder if using Alembic
```
</details>

# Features
 **Add Feed Entries**: Log each feeding with time, type (bottle, breastfeeding, or food), and amount (ml or oz).  
- **Update Feed Entries**: Modify existing feed records if there’s a mistake or update needed.  
- **Delete Feed Entries**: Remove old or incorrect feed records easily.  
- **Feeding Notes**: Add optional notes for each feeding to track baby’s behavior, reactions, or other details.  
- **Filtered Feedings**: Able to filter feedings based on feeding method, amount and times. 
- **Unit Flexibility**: Enter feeding amounts in either milliliters (ml) or ounces (oz) — only one per entry.  
- **Feeding Type Validation**: Uses enums to ensure feeding type and units are consistent.  
- **History Tracking**: Review all past feedings for monitoring patterns and schedules.  
- **API-Driven**: Built with FastAPI for a clean REST API, easy integration with other tools.  
- **Test Coverage**: Includes automated backend tests to ensure stable functionality. 

# Deployment 

# Development - Project Docker Workflow
** This project uses Docker Compose to manage services including the app and database.

**Create your own `.env` file** in the project root with your local database variables:

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
** ⚠️ Important: Do not commit this file to Git. Add it to .gitignore to keep your credentials safe.

---

### Initial Setup / First Run

- Build all images and start containers in detached mode:

```bash
docker compose up --build -d
```

### Changing Code (Python files, endpoints, Pydantic models)

** Since the Dockerfile uses COPY for your source code, code changes won’t automatically appear in the container.

Workflow:
```
docker compose up --build -d <service_name>
```
Or rebuild all services:
```
docker compose up --build -d
```

### Changing Dependencies (requirements.txt, Dockerfile)

**Must rebuild the image to apply changes:
```
docker compose up --build -d
```

### Database Changes
** If the schema or DB setup changes, either:

Run migrations inside the container, or

Recreate the DB container if necessary:
```
docker compose down -v
docker compose up --build -d
```
** ⚠️ Use -v only if you want to remove volumes and start fresh.

### Stopping / Restarting Services
** Stop all services:
```
docker compose down
```
** Restart a single service:
```
docker compose restart <service_name>
```

### Developer Notes:
- If you **change code**: Rebuild image (`docker compose up --build`) or use volumes for live updates.
- If you **change dependencies**: Always rebuild the image.
- Database can be persisted with volumes; otherwise recreating the DB container will reset it.
- You can avoid rebuilding on every code change by using volumes in development:
```
volumes:
  - ./app:/app
```
- Using COPY is mainly recommended for production images to make them self-contained.