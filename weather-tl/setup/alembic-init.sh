#!/bin/bash

if [ -d "./alembic" ]; then
  echo "[wtl] Existing 'alembic' path detected. Skipping."
else
  echo "[wtl] Initializing alembic"
  ${VENV}/bin/alembic init alembic

  init_status=$?

  if [ "${init_status}" -eq 0 ]; then
    # Update alembic/env.py to include the models for our db
    sed -e '/^target_metadata = None$/r setup/alembic_env_metadata.txt' \
        -e 's/^target_metadata = None$/# target_metadata = None/' \
        alembic/env.py > /tmp/alembic-env.py
    mv /tmp/alembic-env.py alembic/env.py

    echo "[wtl] Finished setting up alembic. Continue with initial schema setup"
    ${VENV}/bin/alembic revision --autogenerate -m "Initial schema setup"
  fi
fi

