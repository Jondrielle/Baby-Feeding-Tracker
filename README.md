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
    │ ├── enums.py # enum 
    │ ├── routes/ # API route definitions
    │ │ ├── init.py
    │ │ └── feed.py
    │ ├── crud.py # Database operations (create, update, delete, fetch)
    │ └── database.py # DB session & engine config
    │
    ├── backend_tests/ # Automated tests
    │ ├── init.py
    │ └── test_routes.py
    │
    ├── requirements.txt # Python dependencies
    ├── README.md # Project documentation
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
- **Unit Flexibility**: Enter feeding amounts in either milliliters (ml) or ounces (oz) — only one per entry.  
- **Feeding Type Validation**: Uses enums to ensure feeding type and units are consistent.  
- **History Tracking**: Review all past feedings for monitoring patterns and schedules.  
- **API-Driven**: Built with FastAPI for a clean REST API, easy integration with other tools.  
- **Test Coverage**: Includes automated backend tests to ensure stable functionality. 

# Deployment 

# Development 
