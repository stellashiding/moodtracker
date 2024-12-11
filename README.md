# Mood Tracker for Mental Health

A web application designed to help users monitor their mood through journal entries. It leverages machine learning for sentiment analysis, generates corresponding visuals, and recommends music playlists based on the detected mood. The application aims to support mental well-being by providing personalized feedback and coping strategies.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Navigate to the Backend Directory](#2-navigate-to-the-backend-directory)
    - [3. Create a Virtual Environment](#3-create-a-virtual-environment)
    - [4. Activate the Virtual Environment](#4-activate-the-virtual-environment)
    - [5. Install Dependencies](#5-install-dependencies)
    - [6. Configure Environment Variables](#6-configure-environment-variables)
    - [7. Run the Backend Server](#7-run-the-backend-server)
  - [Frontend Setup](#frontend-setup)
    - [1. Navigate to the Frontend Directory](#1-navigate-to-the-frontend-directory)
    - [2. Build the Docker Image](#2-build-the-docker-image)
    - [3. Run the Docker Container](#3-run-the-docker-container)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- **Sentiment Analysis:** Analyzes journal entries to detect the user's mood using Hugging Face's sentiment analysis model.
- **Personalized Messages:** Generates supportive messages based on the detected mood using OpenAI's language models.
- **Music Recommendations:** Suggests Spotify playlists that align with the user's current mood.
- **Visualizations:** Displays mood-based visual representations using p5.js.
- **Dockerized Frontend:** Frontend is containerized using Docker for easy deployment.


## Project Structure

```
project_root/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── ai_models.py
│   ├── routes.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

- **backend/**: Contains the Flask backend application.
  - **app.py**: Initializes the Flask app and registers routes.
  - **ai_models.py**: Handles AI models and related functions.
  - **routes.py**: Defines API endpoints.
  - **requirements.txt**: Lists Python dependencies.
  - **.env.example**: Example environment variables file.
  
- **frontend/**: Contains the frontend application.
  - **Dockerfile**: Docker configuration for the frontend.
  - **nginx.conf**: Nginx configuration file.
  - **index.html**: Main HTML file.
  - **styles.css**: CSS styles.
  - **script.js**: JavaScript logic using p5.js.

## Prerequisites

- **Docker**: Ensure Docker is installed for containerizing the frontend.
- **Python 3.12**: Required for running the Flask backend.
- **Git**: To clone the repository.
- **Spotify Developer Account**: To obtain `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.
- **OpenAI API Key**: To access OpenAI's language models.

## Setup Instructions

### Backend Setup

#### 1. Clone the Repository

```bash
git clone git@github.com:stellashiding/moodtracker.git
```

#### 2. Navigate to the Backend Directory

```bash
cd backend
```

#### 3. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

#### 4. Activate the Virtual Environment

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

#### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Configure Environment Variables

Create a `.env` file in the `backend/` directory by copying the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file to include your API keys:

```dotenv
OPENAI_API_KEY=your_openai_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

**Note:** Ensure that the `.env` file is **not** committed to version control for security reasons.

#### 7. Run the Backend Server

```bash
python app.py
```

The backend server will start on `http://127.0.0.1:5000/`.

### Frontend Setup

#### 1. Navigate to the Frontend Directory

Open a new terminal window/tab and navigate to the `frontend/` directory:

```bash
cd frontend
```

#### 2. Build the Docker Image

Build the Docker image using the provided `Dockerfile`:

```bash
docker build -t mood-tracker-frontend .
```

#### 3. Run the Docker Container

Run the Docker container, mapping port `80` of the container to port `8080` on your host machine:

```bash
docker run -d -p 8080:80 --name mood-tracker-frontend-container mood-tracker-frontend
```

- **Access the Frontend:**

  Open your browser and navigate to `http://localhost:8080/` to access the frontend application.

**Note:** The frontend is configured to proxy API requests to the backend server running on `http://host.docker.internal:5000`. Ensure that the backend server is running and accessible.

## Usage

1. **Access the Application:**
   - Open your browser and navigate to `http://localhost:8080/`.

2. **Compose a Journal Entry:**
   - Click the "Compose" button.
   - Fill in the title, location, weather, and journal entry body.
   - Submit the journal.

3. **View Results:**
   - Your journal entry will be displayed.
   - The application will analyze the sentiment of your entry.
   - A corresponding visualization will be shown based on your mood.
   - Personalized supportive messages and coping strategies will be provided.
   - Recommended Spotify playlists will be listed with clickable links to listen.

## Troubleshooting

- **Backend Not Running:**
  - Ensure that the backend server is running on `http://127.0.0.1:5000/`.
  - Check for any error messages in the terminal where the backend is running.

- **Frontend Unable to Connect to Backend:**
  - Ensure that the backend server is accessible from within the Docker container.
  - Verify that the backend is running and that `host.docker.internal` correctly points to the host machine.

- **Docker Issues:**
  - Ensure Docker is installed and running on your system.
  - Check Docker container logs for any errors:

    ```bash
    docker logs mood-tracker-frontend-container
    ```

- **API Key Errors:**
  - Verify that the `.env` file contains the correct `OPENAI_API_KEY`, `SPOTIFY_CLIENT_ID`, and `SPOTIFY_CLIENT_SECRET`.
  - Ensure there are no extra spaces or hidden characters in the `.env` file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Changes and Commit**

   ```bash
   git commit -m "Add your message"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Create a Pull Request**

---

**Disclaimer:** This application is intended for educational and supportive purposes. It is not a substitute for professional mental health services.
```

**Additional Notes:**

1. **`.env.example` File:**
   
   Ensure you have a `.env.example` file in your `backend/` directory as shown in the project structure. This file should contain placeholder values for the required environment variables. Here's an example:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret


2. **Docker and Nginx Configuration:**
   
   Make sure your `frontend/Dockerfile` and `frontend/nginx.conf` are correctly set up as per your project's requirements. The provided README assumes these files are already correctly configured.

3. **Running the Application:**
   
   - Start the backend server first to ensure the API is available.
   - Then, start the frontend Docker container to serve the web application.
   - Access the application via `http://localhost:8080/`.

4. **Environment Variables Security:**
   
   Never commit your `.env` file to version control. Ensure it's listed in your `.gitignore` file to prevent accidental exposure of sensitive information.

If you need further assistance or additional sections in the `README.md`, feel free to ask!