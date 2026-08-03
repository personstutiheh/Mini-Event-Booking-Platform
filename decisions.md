# Decisions 

## Phase 0 

I built the backend base with SQLAlchemy, PostgreSQL, FastAPI, and alembic. The issues i faced were : 
- I missed a SQLAlchemy relationship causing the nested ticket_types to break while running backend. 
- A Postgres 15 permissions issue blocking table creation, had to grant all permissions for the schemas for it to work 
- Alembic was a new topic to learn thus had to refer the official document and tutorials.

## Phase 2
