# LLM Chat System

This project allows you to interact with a large language model (LLM) locally through a chat interface. It uses a local instance of an LLM server, which can be set up using LM Studio, and facilitates communication with the model via Python scripts.

## Prerequisites

Before running the project, ensure you have the following:

- **LM Studio** installed on your local machine.
- A selected LLM model from LM Studio.
- Python 3.x installed.

### Steps

1. **Download LM Studio:**
   - Download and install [LM Studio](https://lmstudio.com) on your local machine.
   - Choose a model that fits your needs from LM Studio and start the server.

2. **Configure the Model:**
   - Once the server is running, get the model name you're using.
   - Navigate to the `llm-api-collector` directory and open the `config.json` file.
   - Update the `"model"` field with the name of the model you selected.

   ```json
   {
     "model": "<your-selected-model-name>"
   }

# Run the program
python src/llm_chat_system.py
