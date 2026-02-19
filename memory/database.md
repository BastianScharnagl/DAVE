# Database Memory

This file stores structured data for the system.

## Tables
- users
- tasks
- knowledge
- logs
- system_config

## Schema

### users
- id (int, primary key)
- name (str)
- role (str)
- created_at (datetime)
- updated_at (datetime)
- status (str)

### tasks
- id (int, primary key)
- title (str)
- description (str)
- status (str)
- priority (int)
- created_at (datetime)
- updated_at (datetime)
- completed_at (datetime)
- parent_id (int, foreign key)

### knowledge
- id (int, primary key)
- title (str)
- content (str)
- category (str)
- tags (list)
- created_at (datetime)
- updated_at (datetime)
- version (int)
- source (str)

### logs
- id (int, primary key)
- level (str)
- message (str)
- timestamp (datetime)
- source (str)
- metadata (dict)

### system_config
- id (int, primary key)
- key (str)
- value (str)
- type (str)
- description (str)
- updated_at (datetime)

Last updated: 2026-02-18