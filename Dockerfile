# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies needed for OpenCV, YOLOv8, and matplotlib
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user with UID 1000 (standard for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory in the container
WORKDIR $HOME/app

# Copy the requirements file and install python packages
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application code and set ownership to user
COPY --chown=user . .

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"]
