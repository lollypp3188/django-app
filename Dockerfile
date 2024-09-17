# Use the Python image
FROM python:3.11-alpine


# Set environment variable
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements files first to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the entire project
COPY . /app

# Add a new user and set up directories
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol /app && \
    chmod -R 755 /vol /app

# Expose the application port
EXPOSE 8000

# Argument to toggle development mode
ARG DEV=false

# Create a virtual environment and upgrade pip
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

# Install system dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev zlib-dev

# Install build dependencies, including linux-headers
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib-dev jpeg-dev linux-headers

# Install Python dependencies
RUN /py/bin/pip install -r /tmp/requirements.txt

# Install development dependencies if in DEV mode
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi

# Clean up temporary files and dependencies
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

# Set the virtual environment's path
ENV PATH="/py/bin:$PATH"

# Switch to non-root user
USER django-user

# Start the application
CMD ["run.sh"]


