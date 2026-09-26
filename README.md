# 🧠 Quiz Fullstack

A fullstack quiz application built with **Vue 3** on the frontend and **FastAPI** + **MongoDB** on the backend.

> Register, browse quizzes, and take them — with a JWT-authenticated API behind the scenes.

## Screenshots

**Homepage**
![Homepage](frontend/src/assets/images/Screenshot%202026-09-22%20233205.png)

**Quiz Browsing**
![Quiz Browsing](frontend/src/assets/images/Screenshot%202026-09-22%20233449.png)

## Tech Stack

**Frontend**
- Vue 3
- Pinia (state management)
- Axios (HTTP client)
- jwt-decode

**Backend**
- FastAPI
- MongoDB (via PyMongo)
- PyJWT (authentication)
- bcrypt (password hashing)
- Starlette
- python-dotenv

## Project Structure

```
quiz-fullstack/
├── frontend/     # Vue 3 client
└── quiz/         # FastAPI backend
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (LTS recommended)
- [Python 3.10+](https://www.python.org/)
- A running [MongoDB](https://www.mongodb.com/) instance (local or Atlas)

### Backend Setup

```bash
cd quiz
pip install PyJWT fastapi python-dotenv starlette pymongo bcrypt
```

Create a `.env` file inside `quiz/` with your configuration, for example:

```env
MONGO_URI=mongodb://localhost:27017
JWT_SECRET=your-secret-key
```

> Adjust the variable names above to match what `quiz/` actually reads via `python-dotenv` — update this section once confirmed.

Start the API:

```bash
uvicorn main:app --reload
```

By default this serves the API at `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm install axios jwt-decode pinia
npm run dev
```

This starts the Vue dev server (Vite), typically at `http://localhost:5173`.

## Usage

1. Start MongoDB.
2. Start the backend (`uvicorn main:app --reload`).
3. Start the frontend (`npm run dev`).
4. Open the frontend URL in your browser, register/log in, and browse quizzes.

## Roadmap / Ideas

- [ ] Add API documentation with example requests
- [ ] Add tests (backend and frontend)
- [ ] Add deployment instructions (Docker, hosting)

## License

No license specified yet — consider adding one (e.g., MIT) if you plan to share this publicly.
