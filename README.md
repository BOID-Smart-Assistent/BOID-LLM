# LLM Chat System

This project allows you to interact with a large language model (LLM) locally through a chat interface. It uses a local instance of an LLM server, which can be set up using LM Studio, and facilitates communication with the model via Python scripts.

## Prerequisites

Before running the project, ensure you have the following:

- **LM Studio** installed on your local machine.
- A selected LLM model from LM Studio.
- Python 3.12 installed.
- Install the requirement
```python
   pip install -r requirement.txt
```
### Steps

1. **Download LM Studio:**
   - Download and install [LM Studio](https://lmstudio.com) on your local machine.
   - Choose a model that fits your needs from LM Studio and start the server.

2. **Configure the Model:**
   - Once the server is running, get the model name you're using.
   - Navigate to the `llm-api-collector` directory and open the `.env` file.
   - Update the `LLM_API_COLLECTOR_MODEL` field with the name of the model you selected.

   ```ini
      LLM_API_COLLECTOR_MODEL: <your-selected-model-name>
   ```
3. **Run the program:**
   python src/main.py
4. **Access the API:**
   
   From local gitbash: ``` curl -X GET  http://localhost:<your port setting in ".env" file, default value is 80>/userid/<userid>```
   
   From local browser: ``` http://localhost:<your port setting in ".env" file, default value is 80>/userid/<userid>```

Environment Configuration:

To change port, IP, the model name, etc., you can edit ".env" file directly.
