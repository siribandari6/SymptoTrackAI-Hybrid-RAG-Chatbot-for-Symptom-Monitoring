# SymptoTrackAI Hybrid RAG Chatbot for Symptom Monitoring

## Overview
SymptoTrackAI is an intelligent chatbot system that uses Hybrid RAG (Retrieval-Augmented Generation) architecture to provide symptom monitoring and health advice recommendations. The system combines deep learning models with efficient vector search to deliver accurate symptom-to-disease predictions.

## Features
- **Hybrid RAG Architecture**: Combines retrieval-based and generation-based approaches
- **Symptom Analysis**: Processes natural language symptom descriptions
- **User Management**: Registration and login system
- **Symptom Logging**: Tracks user symptoms and predictions over time
- **FAISS Vector Search**: Efficient similarity search for symptom matching
- **Web Interface**: User-friendly Django-based web application

## Technology Stack
- **Backend**: Django 2.1.7, Python
- **Database**: MySQL 
- **AI/ML**: Transformers (Hugging Face), PyTorch, FAISS
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites
- Python 3.7+
- MySQL Server
- Git (for cloning repository)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "SymptoTrackAI Hybrid RAG Chatbot for Symptom Monitoring"
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Dependencies:**
- numpy==1.21.6
- pandas==1.3.5
- Django==2.1.7
- PyMySQL==0.9.3
- torch==1.13.1
- torchvision==0.14.1
- transformers==4.30.2
- faiss-cpu==1.7.4
- safetensors==0.3.3.post1
- datasets==2.13.2
- sentence-transformers==2.2.2
- sentencepiece==0.1.96

### 4. Database Setup

#### Option A: Using Setup Script (Recommended)
```bash
python setup_database.py
```

#### Option B: Manual MySQL Setup
1. **Start MySQL Server** and ensure it's running on port 3306
2. **Create Database** using MySQL client:
   ```sql
   CREATE DATABASE IF NOT EXISTS symptoms;
   USE symptoms;
   
   CREATE TABLE IF NOT EXISTS register(
       username VARCHAR(50) PRIMARY KEY,
       password VARCHAR(50),
       contact_no VARCHAR(20),
       email VARCHAR(50), 
       address VARCHAR(80)
   );
   
   CREATE TABLE IF NOT EXISTS log(
       username VARCHAR(50),
       symptoms_text VARCHAR(400),
       predicted_advice VARCHAR(60),
       checked_date VARCHAR(40)
   );
   ```

3. **Update Database Configuration** in `Symptoms/settings.py` if needed:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'symptoms',
           'USER': 'root',
           'PASSWORD': 'root',  # Update with your MySQL password
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

### 5. Django Setup
```bash
# Apply Django migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Download Dataset
The project uses the Symptom2Disease dataset. Download it from:
```
https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
```
Place the `Symptom2Disease.csv` file in the `Dataset/` directory.

## Running the Application

### Method 1: Using Python Command
```bash
python manage.py runserver
```

### Method 2: Using Batch Script (Windows)
```bash
run.bat
```

### Method 3: Custom Port
```bash
python manage.py runserver 8080
```

The application will be available at: `http://127.0.0.1:8000`

## Model Initialization

### Warm-up Models (Optional but Recommended)
To pre-load models and improve first-request performance:
```bash
python manage.py warmup_models
```

This command will:
- Initialize RAG models from Facebook's `rag-sequence-nq` and `rag-token-nq`
- Load or create FAISS index for vector similarity search
- Process the symptom dataset and create embeddings

## Usage

### 1. Access the Application
Navigate to `http://127.0.0.1:8000` in your web browser

### 2. User Registration
- Click on "Register" to create a new account
- Fill in required information: username, password, contact, email, address

### 3. User Login
- Use your credentials to log into the system

### 4. Symptom Checking
- Navigate to the chatbot interface
- Enter your symptoms in natural language
- Receive AI-powered health advice and disease predictions

### 5. View Symptom History
- Access your symptom log to track previous consultations
- Monitor patterns and changes over time

## API Endpoints

### Main Application Routes
- `/` - Home page
- `/UserLogin/` - User login page
- `/Register/` - User registration page
- `/UserScreen/` - User dashboard
- `/Chatbot/` - Chatbot interface
- `/ChatData/` - API endpoint for symptom processing
- `/ViewLog/` - View symptom history

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Issues
```bash
# Check MySQL service status
# On Windows:
sc query mysql
# On macOS/Linux:
sudo systemctl status mysql

# Verify database credentials in settings.py
```

#### 2. Model Loading Issues
```bash
# Clear model cache
rm -rf model/faiss.pckl model/Y.npy

# Re-run the application to regenerate models
python manage.py runserver
```

#### 3. Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version compatibility
python --version
```

#### 4. Memory Issues
```bash
# For systems with limited RAM, consider using CPU-only versions
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### 5. Permission Errors
```bash
# On Windows, run as administrator
# On macOS/Linux, check file permissions
chmod +x manage.py
```

## Project Structure
```
SymptoTrackAI/
├── Dataset/
│   └── Symptom2Disease.csv
├── model/
│   ├── faiss.pckl
│   └── Y.npy
├── Symptoms/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── SymptomsApp/
│   ├── management/
│   │   └── commands/
│   │       └── warmup_models.py
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── setup_database.py
├── create_database.sql
├── run.bat
└── README.md
```

## Development

### Adding New Features
1. **Models**: Add new database models in `SymptomsApp/models.py`
2. **Views**: Implement new functionality in `SymptomsApp/views.py`
3. **Templates**: Create HTML templates in `SymptomsApp/templates/`
4. **URLs**: Configure routing in `SymptomsApp/urls.py`

### Testing
```bash
# Run Django tests
python manage.py test

# Test specific app
python manage.py test SymptomsApp
```

## Performance Optimization

### For Production Deployment
1. **Database Optimization**:
   - Use connection pooling
   - Optimize database queries
   - Consider database indexing

2. **Model Caching**:
   - Implement Redis for model caching
   - Use CDN for static files

3. **Security**:
   - Update `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is for educational and research purposes. Please ensure compliance with the licenses of all used datasets and models:
- **Dataset**: [Symptom2Disease Dataset](https://www.kaggle.com/datasets/niyarrbarman/symptom2disease)
- **Models**: Facebook RAG models from Hugging Face

## Support
For issues and questions:
1. Check the troubleshooting section above
2. Review Django and PyTorch documentation
3. Consult the Hugging Face Transformers documentation

## Disclaimer
This application is for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.
