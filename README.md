# 👶 Baby-Feeding-Tracker

A simple and intuitive app designed for parents and caregivers to **track a baby’s feeding schedule**.  
With Baby-Feeding-Tracker, you can:  

- **🆕 Log new feedings**  
- **✏️ Update or delete past entries**  
- **📊 View a history of feed events**  

Keep your baby’s feeding routine organized and easy to monitor!
 

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

# ✨ Features

- **📝 Add Feed Entries**: Log each feeding with time, type (bottle, breastfeeding, or food), and amount (ml or oz).  
- **✏️ Update Feed Entries**: Modify existing feed records if there’s a mistake or update needed.  
- **🗑️ Delete Feed Entries**: Remove old or incorrect feed records easily.  
- **📝 Feeding Notes**: Add optional notes for each feeding to track baby’s behavior, reactions, or other details.  
- **🔍 Filtered Feedings**: Filter feedings based on method, amount, or time.  
- **⚖️ Unit Flexibility**: Enter feeding amounts in either milliliters (ml) or ounces (oz) — only one per entry.  
- **✅ Feeding Type Validation**: Uses enums to ensure feeding type and units are consistent.  
- **📊 History Tracking**: Review all past feedings to monitor patterns and schedules.  
- **🌐 API-Driven**: Built with FastAPI for a clean REST API, making integration with other tools easy.  
- **🧪 Test Coverage**: Includes automated backend tests to ensure stable functionality.  


# Development - Project Docker Workflow
This project uses Docker Compose to manage services including the app and database.

<details>
  <summary>📄 Set Up</summary>

Create your own `.env` file in the project root with your local database variables:

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> ⚠️ Important: Do not commit this file to Git. Add it to .gitignore to keep your credentials safe.
</details> 
  <details> <summary>🚀 Building</summary>

Build images and start services in detached mode:
  
```
docker compose up --build -d
```

</details> <details> <summary>🖥 Running the App</summary>
  
Start the FastAPI app:
 
```
docker compose up -d app
```

Access Swagger docs at:
  
http://localhost:8000/docs

</details> <details> <summary>🧪 Running Tests</summary>
  
Run tests in the test container:

```
docker compose run --rm test
```

</details> <details> <summary>✏️ Making Changes</summary>
  
Code Changes (Python files, endpoints, Pydantic models):

  * If using volumes, changes appear automatically.
  
  *  If not using volumes, rebuild the image:
    
```
docker compose up --build -d
```

Dependencies Changes (requirements.txt or Dockerfile):

  * Must rebuild the image:
    
```
docker compose up --build -d
```

Database Changes:

  * Run migrations inside the container, or

  * Recreate the DB container if schema changes:
    
```
docker compose down -v
docker compose up --build -d
```

> ⚠️ -v removes volumes, so all data will be lost. Use only if starting fresh.

</details> <details> <summary>⏹ Stopping / Restarting Services</summary>
  
Stop all services:
  
```
docker compose down
```

Restart a single service:
  
```
docker compose restart <service_name>
```

</details>
<details>
  <summary>🚀 GitHub Actions CI/CD Workflow</summary>
  
Pushes to the `master` branch trigger this CI workflow:

### Workflow Steps
1. **Build & start services** 🏗️  
2. **Run tests** in a temporary container 🧪  
3. **Tear down services** 🧹  

### 🔐 Secrets used in CI/CD
- `POSTGRES_USER`  
- `POSTGRES_PASSWORD`  
- `POSTGRES_DB`  

> ⚠️ Make sure to set these secrets in your **GitHub repository settings** under _Settings → Secrets and variables → Actions_.

</details>


#### Developer Notes:
- Local development does not require changing your config file (env_file=None).
- CI workflow uses secrets for database credentials, so no .env.ci is needed in the repository.
- Database runs in the background; FastAPI Swagger (/docs) works normally while services are running.
- Using COPY is mainly recommended for production images to make them self-contained.
