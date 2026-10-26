# AutoGen HR Assistant Agent

A simple HR assistant built with **Microsoft AutoGen**, **OpenAI**, and **Streamlit**. It generates a five-line job description for a Junior Python Developer (or responds to an editable HR prompt). All Python application code is in **`hr_agent.py`**.

## Features

- Streamlit frontend with an editable HR request and a Generate button.
- AutoGen `AssistantAgent` named `hr_assistant`.
- Exact agent system message: `You are an HR assistant.`
- OpenAI model via `OpenAIChatCompletionClient`.
- Async execution with `asyncio.run()`.
- Streams the agent's messages to the terminal with AutoGen `Console`.
- Displays the response in Streamlit and offers a TXT download.
- Loads API credentials from a local `.env` file with `python-dotenv`.
- Closes the model client in a `finally` block to prevent resource leaks.

## Architecture

```text
User
  |
  v
Streamlit UI (hr_agent.py)
  |
  v
asyncio.run(generate_description(...))
  |
  v
AutoGen AssistantAgent (hr_assistant)
  |
  v
OpenAIChatCompletionClient
  |
  v
LLM-generated job description
  |                  |
  v                  v
Console (terminal)   Streamlit output + TXT download

Finally: await model_client.close()
```

## Requirements

- Python 3.10 or newer (use a supported Python version for your installed AutoGen and Streamlit releases).
- An OpenAI API key with access to the configured model.
- Internet access to call the OpenAI API.

## Project structure

```text
AutoGen-HR-Assistant/
├── hr_agent.py    # All Python application code
├── .env           # Local API configuration; do not commit
├── .gitignore     # Recommended secret exclusions
└── README.md      # This guide
```

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -U streamlit python-dotenv autogen-agentchat "autogen-ext[openai]"
```

### 3. Configure `.env`

Create a `.env` file next to `hr_agent.py`:

```dotenv
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

`hr_agent.py` calls `load_dotenv()` and reads `OPENAI_API_KEY` and `OPENAI_MODEL` from the environment. Never hard-code or publish your real API key.

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

### 4. Run the app

```bash
python -m streamlit run hr_agent.py
```

Open the URL printed by Streamlit, usually **http://localhost:8501**.

## How to use

1. Launch the Streamlit application.
2. Leave the default request, **“Write exactly 5 lines of a job description for a Junior Python Developer.”**, or edit it.
3. Click **Generate job description**.
4. View the response in Streamlit and the streamed messages in the terminal.
5. Optionally click **Download as TXT**.

## Implementation notes

The application creates an `OpenAIChatCompletionClient`, passes it to `AssistantAgent(name="hr_assistant", system_message="You are an HR assistant.", ...)`, and streams the agent response through `Console(agent.run_stream(...))`. The Streamlit handler calls `asyncio.run(generate_description(...))`. A `finally` block calls `await model_client.close()` even if generation fails.

The five-line requirement is specified in the task prompt; the code **does not enforce** the exact line count after generation, so the model may occasionally produce a different number of lines.

## Troubleshooting

| Issue | Solution |
| --- | --- |
| `No module named streamlit` | Activate the intended virtual environment and rerun the dependency installation command. |
| `No module named dotenv` | Run `python -m pip install python-dotenv`. |
| Missing `OPENAI_API_KEY` | Check that `.env` is in the app's working directory and contains a valid key. |
| Authentication error | Check your OpenAI API key and API access. |
| Model unavailable | Change `OPENAI_MODEL` to a model enabled for your account. |
| Browser page is blank | Inspect the Streamlit terminal output and refresh the app. |

## Example output (illustrative)

```text
1. Develop and maintain Python applications and backend services.
2. Write clean, readable, and well-tested Python code.
3. Work with REST APIs, SQL databases, and Git.
4. Debug issues and collaborate with senior engineers.
5. Requirements: Python fundamentals, problem-solving skills, and willingness to learn.
```

Actual output depends on the model response.


