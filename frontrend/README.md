# DocuMind AI — Frontend

DocuMind AI is an intelligent document processing application that uses AI to extract information from uploaded documents, validate the extracted data, and route documents for automatic approval or human review.

## Frontend Technology

- Python
- Streamlit
- Requests
- REST API integration

## Application Workflow

Upload Document  
↓  
Processing  
↓  
AI Results  
↓  
Validation  
↓  
Decision  
↓  
Human Review  
↓  
Dashboard

## Project Structure

```text
frontend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   └── backend_client.py
│   │
│   └── pages/
│       ├── 1_Upload.py
│       ├── 2_Processing.py
│       ├── 3_Results.py
│       ├── 4_Review.py
│       └── 5_Dashboard.py
│
├── requirements.txt
└── README.md
