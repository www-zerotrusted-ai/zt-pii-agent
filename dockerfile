FROM python:3.13

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="$HOME/.local/bin:$PATH"

# Set path
ENV PATH="/root/.local/bin:$PATH"

# Create app directory
WORKDIR /app

# Copy and install
COPY . .

RUN poetry install

CMD ["python", "main.py"]
