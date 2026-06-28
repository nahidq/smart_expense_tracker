#Use  official Python image

FROM python:3.11-slim

#Set working directory inside container
WORKDIR /app

RUN pip install poetry
#Add Poetry to PATH
#ENV PATH="/root/.local/bin:$PATH"

#Copy dependency files(from root)
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy only auth service code (includes alembic/, alembic.ini, entrypoint.sh)
COPY backend/auth_service /app
# Normalize line endings in case the script was checked out with CRLF on Windows.
RUN sed -i 's/\r$//' /app/entrypoint.sh
# Expose port
EXPOSE 8000

# Migrate the database, then run FastAPI (see entrypoint.sh)
CMD ["sh", "/app/entrypoint.sh"]