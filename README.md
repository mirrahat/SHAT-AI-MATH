
# SHAT-FLUSK: SHSAT Fine-Tuned GPT with Flask Web Interface

This project focuses on fine-tuning OpenAI's GPT-3.5 Turbo model using a custom SHSAT dataset. It includes a simple Flask web interface that allows users to interact with the fine-tuned model to generate SHSAT-style questions.

## Features

- Fine-tune GPT-3.5 Turbo on custom SHSAT questions
- Flask web app interface for testing the model
- Secure handling of the API key through a .env file
- Dataset and API key stored in Google Drive
- Script to monitor fine-tuning job status
- Includes Docker support for containerization
- Instructions for deployment to Azure App Service

## Project Structure

```
SHAT-FLUSK/
├── app.py
├── templates/
│   └── index.html
├── shsat_finetune_data.jsonl
├── fine_tune_train.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/mirrahat/SHAT-FLUSK.git
cd SHAT-FLUSK
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory or in  Google Drive. It should include  OpenAI API key:

```
OPENAI_API_KEY=openai_api_key_here
```

## Dataset Format

 JSONL file should follow this format:

```json
{
  "messages": [
    {"role": "system", "content": "You are a SHSAT question generator."},
    {"role": "user", "content": "Generate a math word problem."},
    {"role": "assistant", "content": "If 3x + 4 = 16, what is x?"}
  ]
}
```

## Fine-Tuning Script

Here is the basic script used to upload the dataset and fine-tune the model:

```python
import openai, os, time
from dotenv import load_dotenv

load_dotenv("/content/drive/MyDrive/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

upload_response = openai.files.create(
    file=open("/content/drive/MyDrive/shsat_finetune_data.jsonl", "rb"),
    purpose="fine-tune"
)
file_id = upload_response.id

fine_tune_response = openai.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)
job_id = fine_tune_response.id

while True:
    job = openai.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    if job.status in ["succeeded", "failed", "cancelled"]:
        break
    time.sleep(15)

if job.status == "succeeded":
    print(f"Fine-tuned model ID: {job.fine_tuned_model}")
```

## Running the App Locally

```
python app.py
```

The app will be available at http://127.0.0.1:5000

## Docker Deployment

To build and run the application using Docker:

```
docker build -t shsat-flusk .
docker run -p 5000:5000 --env-file .env shsat-flusk
```

## Azure App Service Deployment

1. Create a Python Web App in Azure.
2. Zip your application files (excluding virtual environments).
3. Deploy using the Azure CLI:

```
az webapp up --name AppName --resource-group ResourceGroup --plan AppPlan --runtime "PYTHON:3.10" --src-path shsat-app.zip
```

4. In Azure portal, go to Configuration > Application Settings and add:

```
OPENAI_API_KEY=_key_here
```

5. Restart the app after saving the settings.

## Using the Fine-Tuned Model

Once  model is trained, use its ID in  Flask app like this:

```python
response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo-<your-id>",
    messages=[...]
)
```

## Author

Mir Hasibul Hasan Rahat  
GitHub: https://github.com/mirrahat  
LinkedIn: www.linkedin.com/in/mir-rahat-2b2108147

## License

This project is released under the MIT License.

## Future Improvements

- Add English section question generation
- Collect user feedback for further fine-tuning
- Deploy via Azure Functions for better scalability
