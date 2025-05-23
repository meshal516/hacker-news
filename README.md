# Hacker News Analytics Dashboard

This project provides a production-ready, distrubted full-stack application to fetch, analyze, and visualize data from the Hacker News API, focusing on AI-related topics and trends. It includes a Django backend API and a React frontend dashboard.

## Key Technologies

- **Backend:** Django, Django REST Framework, PostgreSQL, Redis, Kafka (confluent-kafka), django-cors-headers, drf-spectacular
- **Frontend:** React, TypeScript, Zustand, Axios, MUI (Material UI), Chart.js, react-chartjs-2, date-fns
- **Testing:** Pytest (backend), React Testing Library (frontend potentially)

## Architecture Overview (Simplified)

- **Data Fetching:** A background task (triggered via Kubernetes and Kafka) periodically fetches data from the Hacker News API, processes it (detects AI keywords, extracts domains), and stores it in the PostgreSQL database.
- **Caching:** Redis is used to cache API responses (stories, insights) for faster retrieval.
- **API:** The Django backend exposes RESTful API endpoints (`/api/stories/`, `/api/insights/`).
- **Frontend:** The React application consumes data from the backend API using Zustand for state management and displays it using MUI components and Chart.js.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python:** >= 3.10 (verify specific version if needed) & Pip
- **Node.js:** >= 16.x & Npm or Yarn
- **PostgreSQL:** A running instance for the database.
- **Redis:** A running instance for caching.
- **Kafka:** A running Kafka cluster (or a single node for local development). Confluent Kafka libraries are used.
- **Git:** For cloning the repository.
- **(Optional) Docker & Docker Compose:** Recommended for easily running Postgres, Redis, and Kafka locally.


## High Level Architechure
![High Level Architecture HN](https://raw.githubusercontent.com/meshal516/hacker-news/refs/heads/main/HL_Arch_HN.png)

## Backend Setup (Django)

1.  **Navigate to Backend Directory:**

    ```bash
    cd hacker-news/backend
    ```

2.  **Create & Activate Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the `hacker-news/backend/` directory. Copy the contents of `.env.example` (if provided) or create it with the following variables, adjusting values for your local setup:

    ```dotenv
    # .env file for backend

    # Django Core
    DJANGO_SECRET_KEY='your-strong-django-secret-key-here' # Generate a real secret key
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

    # Database (PostgreSQL) - Use ONE of the following formats
    # Option A: Full DATABASE_URL (often used by services like Heroku/Render)
    # DATABASE_URL='postgres://USERNAME:PASSWORD@HOST:PORT/DB_NAME'

    # Option B: Individual Components (used by settings.py directly)
    RDS_DB_NAME=hacker_news_db
    RDS_USERNAME=your_db_user
    RDS_PASSWORD=your_db_password
    RDS_HOSTNAME=localhost # Or your DB host
    RDS_PORT=5432         # Or your DB port

    # Redis Cache
    REDIS_URL='redis://localhost:6379/0' # /0 specifies database 0

    # Kafka Configuration (adjust based on your Kafka setup)
    KAFKA_BOOTSTRAP_SERVERS='localhost:9092' # Your Kafka broker(s)
    KAFKA_TOPIC_PREFIX='hackernews.dev.' # Prefix for Kafka topics
    # --- Optional Kafka Auth (if your cluster requires it) ---
    # KAFKA_SECURITY_PROTOCOL=SASL_SSL # or SASL_PLAINTEXT, etc.
    # KAFKA_SASL_MECHANISM=PLAIN # or SCRAM-SHA-512, etc.
    # KAFKA_SASL_USERNAME=your_kafka_user
    # KAFKA_SASL_PASSWORD=your_kafka_password
    ```

5.  **Apply Database Migrations:**
    Ensure your PostgreSQL server is running and accessible with the credentials in your `.env` file.  Then, run the command below to apply the migration script to the PostgreSQL database.

    ```bash
    python manage.py migrate
    ```

6.  **Manual Data Fetching (Optional):**
    While data fetching is typically handled automatically via the background kubernetes cron job, you can manually trigger a fetch and processing cycle using a management command. This is useful for initial population or debugging.
    ```bash
    # Ensure your backend virtual environment is active
    python manage.py fetch_hn_stories
    ```
    This command will:
    - Fetch the latest top story IDs from the Hacker News API.
    - Fetch details for each story.
    - Process stories (detect AI keywords, extract domains).
    - Save/update stories, keywords, and domain stats in the database.
    - Update the Redis cache for individual stories.
    - Clear relevant aggregate Redis cache keys (`stories_list_*`, `ai_keywords`, etc.).

## Frontend Setup (React)

1.  **Navigate to Frontend Directory:**

    ```bash
    cd hacker-news/frontend
    ```

2.  **Install Dependencies:**

    ```bash
    npm install
    # or if using yarn:
    # yarn install
    ```

3.  **Environment Variables (Optional):**
    The frontend uses the `proxy` setting in `package.json` during development to forward API requests to the backend running on port 8000.
    For production builds, you might need to create a `.env` file in `hacker-news/frontend/` and set the API base URL:
    ```dotenv
    # .env file for frontend (Optional for production build)
    REACT_APP_API_BASE_URL=https://your-deployed-api.com/api
    ```

## Running / Interacting with the Application

This application is designed to run in a containerized environment managed by Kubernetes (hosted on DigitalOcean) and utilizes managed cloud services for its dependencies.

1.  **Obtain Credentials & Access:**
    The repo needs access to the following services and their corresponding credentials/connection details:

    - **Kafka:** Obtain connection details (bootstrap servers, API keys/secrets if using SASL) for the project's Kafka cluster, hosted on **Confluent Cloud** in this project. These are needed for the `KAFKA_*` variables in the backend `.env` file.
    - **Redis:** Obtain the connection URL for the managed Redis instance, hosted on **DigitalOcean** in this project. This is needed for the `REDIS_URL` variable in the backend `.env` file.
    - **PostgreSQL:** Obtain connection details for the managed PostgreSQL instance, hosted in AWS in this project. These are needed for the `RDS_*` variables or `DATABASE_URL` in the backend `.env` file.
    - **Kubernetes:** Obtain `kubectl` configuration/access details for the project's Kubernetes cluster, hosted on **DigitalOcean** in this project.

2.  **Environment Variables:**
    Ensure your backend `.env` file (see Backend Setup) is configured with the correct credentials and endpoints for the managed **Confluent Kafka**, **DigitalOcean Redis**, and **PostgreSQL** instances mentioned above. The variables `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` should also be set appropriately for the target environment.

3.  **Deployment & Interaction:**
    - The backend API, frontend application, and Kafka consumer task are deployed as services within the **DigitalOcean Kubernetes** cluster.
    - To interact with the application, you will typically access the deployed frontend URL.
    - To view logs, manage deployments, or debug issues, use `kubectl` with the provided cluster access configuration. Refer to the project's Kubernetes configuration files (in the `k8s/` directory) for details on services, deployments, and pods.
    - Direct execution via `python manage.py runserver` or `npm start` is generally used for specific local debugging scenarios, but the primary interaction model is via the deployed Kubernetes environment.

