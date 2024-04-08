## Pantry AI Assistant

An AI assistant that helps manage a kitchen pantry.

This project is work in progress. So far I have created a basic interface and connected an LLM which is run locally using `Ollama`. See below.

[app · Streamlit.webm](https://github.com/jhicks2306/ai-assistant/assets/45722942/cf3a356b-e26e-44a0-9c91-9c90110d7539)



### Skills and technologies used.
- `Ollama` used to run open source large language model locally.
- `Streamlit` for main chat app and interface.
- `Langchain` for building the flow of interaction with the llm.
- `SQLite3` for creating a simple database for a kitchen pantry.
- `speech-recognition` package for testing voice to speech.
- `gTTs` for testing text to speech.

### Features
- [x] Add/remove items to pantry via chat.
- [x] Check whether an item is in the pantry via chat.
- [x] Get recipe suggestions based on ingredients from the pantry.
- [ ] View pantry in separate page.
- [ ] Add/remove items to shopping list via chat.
- [ ] View shopping list in separate page.
- [ ] Add items using image recognition.
- [ ] Manage interactions with voice.
- [ ] Add more...

### Notes
Homebrew installs needed for the project.
- ffmpeg
- portaudio
