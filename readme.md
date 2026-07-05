# 🎵 Album Cover Studio (PDA-226)

**Album Cover Studio** is a multimodal Python desktop application that bridges the gap between personal emotional expression and musical discovery. By leveraging state-of-the-art Generative AI and real-world music databases, the application transforms a user's subjective mood or journal entry into a cohesive, high-fidelity fictional album concept.

Developed as the final project for **SE 226: Advanced Programming** at İzmir University of Economics.

## ✨ The Concept of "Duality"

Central to the project is the "Concept of Duality"—where imagination meets reality:

* **The Fictional Layer:** Album Name, Artist Persona, Release Year, and Cover Art are completely original and synthesized by AI.
* **The Real-World Layer:** The generated tracklist consists of *real* songs fetched dynamically from the Last.fm database, allowing users to actually listen to music that matches their mood.

## 🚀 Key Features

* **Semantic Mood Analysis:** Powered by **Google Gemini 2.5 Flash**, it extracts emotional nuances from free-form text to generate structured album metadata.
* **Acoustic Discovery:** Queries the **Last.fm API** to find authentic tracks, using a proprietary de-duplication algorithm to ensure a unique tracklist.
* **AI Visual Synthesis:** Generates high-resolution, logo-free cover art using the **Pollinations.ai** engine.
* **Modern Spotify-Style UI:** Built entirely with **Tkinter** and `ttk` widgets using a custom "Clam" dark theme, responsive layout, and clickable "Listen" buttons.
* **Non-Blocking Architecture:** Implements `threading.Thread` and safe `.after()` callbacks to keep the UI perfectly responsive at 60fps during heavy API calls.
* **Media Export:** Save your creation locally. Exports a `.json` file containing all metadata/track URLs and a `.png` file of the AI cover art.


## 🛠️ Prerequisites

Before you begin, ensure you have the following installed and set up:

1. **Python 3.8 or higher:** [Download Python](https://www.python.org/downloads/)

2. **Free Gemini API Key:** Get it from [Google AI Studio](https://aistudio.google.com/apikey).

3. **Free Last.fm API Key:** Create an API account at [Last.fm](https://www.last.fm/api/account/create). *(Note: Only the API Key is needed, not the shared secret).*


## ⚙️ Step-by-Step Installation & Setup


### 1. Clone the Repository


Download the project files to your local machine:

```bash
git clone https://github.com/yourusername/album-cover-studio.git
cd album-cover-studio

```

### 2. Set Up a Virtual Environment (Recommended)

It is best practice to use a virtual environment to manage dependencies.

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Required Dependencies

Install the necessary Python libraries required for API communication, image processing, and AI generation:

```bash
pip install requests Pillow google-generativeai python-dotenv

```

*(Alternatively, if you have a `requirements.txt` file, run `pip install -r requirements.txt`)*

### 4. Configure Environment Variables

To keep your API keys secure, the application uses environment variables.

1. Create a new file in the root directory named exactly `.env`.

2. Open the `.env` file and add your API keys in the following format:


```env

GEMINI_API_KEY=your_gemini_api_key_here
LASTFM_API_KEY=your_lastfm_api_key_here

```

### 5. Run the Application

Launch the Tkinter GUI by running the main entry point of the application:

```bash
python main.py
```

## Project Architecture (MVVM)

The project strictly follows the **Model-View-ViewModel (MVVM)** design pattern to separate the Tkinter GUI from the business logic:

* **`/views`**: Contains `main_page.py`. Handles the Tkinter layout, Custom TTK Styling, and UI updates.

* **`/viewmodels`**: Contains `album_view_model.py`. Manages the background threads, state machine, and communication between the UI and backend services.

* **`/features`**: Contains the core logic services:

* `gemini_service.py`: LLM prompting and regex-based Markdown sanitization.

* `lastfm_service.py`: Multi-tag aggregation and Set-based track de-duplication.

* `image_service.py`: URL encoding, byte-stream fetching, and PIL image conversion.

* `save_manager.py`: Split-save serialization handling JSON and PNG exports securely.


## 📄 Academic Integrity & License

This project was developed for the SE 226 Advanced Programming course at İzmir University of Economics. The codebase relies on publicly available APIs (Gemini, Last.fm, Pollinations.ai).

*Note: Generated album metadata and cover art are purely fictional and created by AI. The tracklists are real songs fetched from Last.fm. Please respect API rate limits and terms of service when using this software.*
