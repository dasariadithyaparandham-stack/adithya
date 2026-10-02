# Database

The ORM schema includes users, resumes, skills, skill aliases, job roles, weighted job skills, resume skills, analyses, and per-analysis skills. Canonical skills and job roles are unique; relationship rows have uniqueness constraints. Startup seeding adds the controlled taxonomy and 15 target roles.

SQLite is the default local database. Production should use PostgreSQL and a migration tool rather than `create_all` startup initialization.
