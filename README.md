# TeachCraftAI: LLM-Powered Educational Content Creator

TeachCraftAI is a Streamlit web application designed to assist faculty and educators in rapidly generating high-quality study materials. By leveraging the power of Google's Gemini models via LangChain, this tool can create detailed study guides or complete PowerPoint presentations from a simple topic, a webpage URL, or an uploaded document.

## ✨ Features

* **Multiple Content Formats:** Generate either comprehensive raw text study guides or structured PowerPoint presentations (`.pptx`).
* **Flexible Input Sources:**
    * **Topic Only:** Create content using the LLM's extensive internal knowledge.
    * **From URL:** Scrape and summarize content from any webpage.
    * **From File:** Upload existing notes (`.txt`, `.doc`, `.docx`) to be repurposed.
* **Context-Aware Generation:** Tailors content based on faculty details like the student year, department, and subject.
* **Intuitive UI:** Simple and clean interface built with Streamlit for easy configuration.

## 📂 Project Structure

Here is the file structure for the project:
```ini
├── src/                           # Source code of the application
│   ├── core/                      # Core business logic and LLM interfaces
│   │   ├── llm_chain.py           # LangChain setup and prompt invocation
│   │   ├── content_loader.py      # Logic for fetching/parsing URL/File content
│   │   └── ppt_generator.py       # Logic for creating the PPT (e.g., using python-pptx)
│   ├── ui/                        # Streamlit components and main app logic
│   │   ├── init.py
│   │   ├── app.py                 # The main Streamlit entry point
│   │   └── sidebar.py             # Reusable UI component for the sidebar inputs (Optional, but good for structure)
│   └── init.py
├── data/                          # Placeholder for any sample files or temporary outputs
├── .env.example                   # Template for environment variables (e.g., GOOGLE_API_KEY)
├── .gitignore                     # Files and directories to exclude
├── requirements.txt               # List of all Python dependencies
└── README.md                      # Project description, setup, and usage instructions
```

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### 1. Prerequisites

* Python 3.8+
* Git

### 2. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/TeachCraftAI.git](https://github.com/your-username/TeachCraftAI.git)
    cd TeachCraftAI
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

The application requires a Google API key to function.

1.  **Create a `.env` file** in the root directory by copying the example:
    ```bash
    cp .env.example .env
    ```

2.  **Add your API key** to the new `.env` file. You can get your key from [Google AI Studio](https://aistudio.google.com/).
    ```ini
    GOOGLE_API_KEY="your_api_key_here"
    ```

3.  **Create the `data` directory** if it doesn't exist. This is used for temporary file uploads and outputs.
    ```bash
    mkdir data
    ```

### 4. Running the Application

1.  From the **root directory** of the project, run the Streamlit app:
    ```bash
    streamlit run src/ui/app.py
    ```

2.  Open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

## 💻 Technology Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Framework:** [LangChain](https://www.langchain.com/)
* **LLM:** Google Gemini (via `langchain-google-genai`)
* **Web Scraping:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/), [Requests](https://requests.readthedocs.io/en/latest/)
* **PowerPoint Generation:** [python-pptx](https://python-pptx.readthedocs.io/en/latest/)
