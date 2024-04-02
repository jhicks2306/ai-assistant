## Pantry AI Assistant

An AI assistant that helps manage a kitchen pantry.

This project is work in progress. So far I have created a basic interface and connected an LLM which is run locally using `Ollama`. See below.

[app · Streamlit.webm](https://github.com/jhicks2306/ai-assistant/assets/45722942/cf3a356b-e26e-44a0-9c91-9c90110d7539)



### Skills and technologies used so far.
- `Ollama` used to run open source large language model locally.
- `Streamlit` for main chat app and interface.
- `Langchain` for building the flow of interaction with the llm.
- `SQLite3` for creating a simple database for a kitchen pantry.
- `speech-recognition` package for testing voice to speech.
- `gTTs` for testing text to speech.

### Todos
- [x] Set up Ollama and get llm running locally.
- [x] Create streamlit UI.
- [x] Add chat history.
- [x] Test formats for storing pantry data.
- [x] Create a simple SQL database for kitchen pantry.
- [x] Experiment with a text2speech module.
- [x] Experiment with a speech2text module.
- [x] Create chain that can use llm to query SQL database.
- [x] Create a chain to extract ingredients from user input.
- [x] Experiment with function calling and Langchain agents for directing interaction.
- [ ] Create second streamlit page to present pantry data.
- [x] Create a chain which adds ingredients to pantry.
- [x] Create a chain which removes ingredients from pantry.
- [ ] Turn Ollama LLM into an Agent which dynamically select correct tool.
- [ ] Add more...

### Notes
Homebrew installs needed for the project.
- ffmpeg
- portaudio
