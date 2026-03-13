# 📄 Legal / Policy Document Summarization & Q&A System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![NLP](https://img.shields.io/badge/NLP-Text%20Processing-green)
![License](https://img.shields.io/badge/License-Academic-orange)

---

# 🚀 Project Overview

The **Legal / Policy Document Summarization and Question Answering System** is an AI-powered web application designed to simplify the process of understanding complex legal and policy documents.

The system allows users to **upload lengthy documents**, automatically **generate concise summaries**, and **ask questions related to the document**. Using **Natural Language Processing (NLP)** techniques, the system extracts important information and provides accurate responses based on document content.

This project helps users quickly understand complex documents without reading the entire text.

---

# 🎯 Objectives

* Automatically **summarize long legal documents**
* Enable **question answering from uploaded documents**
* Reduce **manual document reading effort**
* Provide **accurate information retrieval using NLP**
* Create a **simple and user-friendly document analysis platform**

---

# ✨ Key Features

📄 **Document Upload**
Upload legal or policy documents in **PDF or TXT format**.

🧠 **Automatic Summarization**
Generate summaries using **extractive NLP summarization techniques**.

❓ **Question Answering**
Ask questions related to the document and receive relevant answers.

📚 **Document Management**
Store uploaded documents and summaries.

⚡ **Fast NLP Processing**
Uses efficient NLP libraries for fast processing.

🔐 **Secure Data Handling**
Documents and user data are handled securely.

---

# 🛠 Technology Stack

| Technology              | Purpose                     |
| ----------------------- | --------------------------- |
| Python                  | Backend development         |
| Flask                   | Web framework               |
| spaCy                   | Natural Language Processing |
| NLTK                    | Text preprocessing          |
| Scikit-learn            | TF-IDF vectorization        |
| PyPDF2                  | Extract text from PDF       |
| SQLite                  | Database                    |
| HTML / CSS / JavaScript | Frontend interface          |

---

# 🏗 System Architecture

```
User
  │
  ▼
Web Interface (HTML / CSS / JS)
  │
  ▼
Flask Backend Server
  │
  ├── Document Upload Module
  ├── Text Extraction Module
  ├── NLP Processing
  │      ├ Tokenization
  │      ├ Stopword Removal
  │      └ TF-IDF Similarity
  │
  ├── Summarization Engine
  └── Question Answering Module
  │
  ▼
Database (SQLite)
```

---

# 📂 Project Structure

```
legal-doc-summarizer
│
├── app.py
├── main.py
│
├── routes
│   ├── upload.py
│   ├── summarize.py
│   └── qa.py
│
├── models
│
├── static
│   ├── css
│   ├── js
│   └── uploads
│
├── templates
│
└── database
    └── sqlite.db
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/legal-doc-summarizer.git
```

```
cd legal-doc-summarizer
```

---

## 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 3️⃣ Run the Application

```
python app.py
```

Application will run on:

```
http://localhost:5000
```

---

# 💻 Usage

1️⃣ Open the web application in your browser.

2️⃣ Upload a **legal or policy document**.

3️⃣ Click **Generate Summary**.

4️⃣ Ask questions related to the document.

5️⃣ The system returns the **most relevant answers**.

---

# 📊 Advantages

✔ Saves time by summarizing lengthy documents
✔ Helps understand complex legal text
✔ Easy-to-use interface
✔ Quick information retrieval
✔ Reduces manual document analysis

---

# 🔮 Future Improvements

* Deep learning based summarization
* Support for scanned documents using OCR
* Multilingual document support
* Cloud deployment
* Advanced legal NLP models

---

# 🖼 Screenshots

*(Add screenshots of your application here)*

Example:

```
/screenshots/homepage.png
/screenshots/upload.png
/screenshots/summary.png
```

---

# 🎥 Demo

You can add a demo video or GIF of the project here.

Example:

```
https://github.com/your-username/project-demo
```

---

# 📜 License

This project is developed for **academic and educational purposes**.
