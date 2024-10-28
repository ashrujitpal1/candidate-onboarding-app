# Builder stage
FROM library/python:3.9-stretch as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM library/python:3.9-stretch

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Copy all files from the src directory
COPY src/ .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
