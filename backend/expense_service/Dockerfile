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

# Copy only expense service code
COPY backend/expense_service /app
# Expose port
EXPOSE 8001

# Run FastAPI
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]