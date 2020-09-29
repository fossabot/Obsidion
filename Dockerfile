FROM python:3.8-slim

# Create the working directory
WORKDIR /obsidion

# Install project dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the source code in last to optimize rebuilding the image
COPY . .

ENTRYPOINT ["python3"]
CMD ["-m", "obsidion"]