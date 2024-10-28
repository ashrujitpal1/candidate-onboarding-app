# Builder stage
FROM python:3.9.2 as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9.2

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Copy all files from the src directory
COPY src/ .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
