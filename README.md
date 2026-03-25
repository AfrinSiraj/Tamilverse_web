# 🌍 Tamilverse – Intelligent Travel Assistant for Tamil Nadu

Tamilverse is a full-stack web application built using Django that helps users explore, plan, and experience tourism across Tamil Nadu. It provides smart travel guidance through an interactive chatbot and structured place-based information.

---

## 🎯 Objective

To build a smart tourism platform that:

* Helps users discover places across Tamil Nadu
* Provides personalized travel suggestions
* Answers user queries in a simple and interactive way
* Combines clean UI with powerful backend logic

---

## 🚀 Key Features

### 🗺️ Explore Places

* Browse popular tourist destinations
* Clean and minimal UI
* Dedicated pages for each place
* Dynamic routing using slugs

---

### 📍 Place Detail Pages

* Description of each place
* Image display
* Nearby places suggestions
* Like and review system

---

### 🤖 Smart Chatbot (Core Feature)

An interactive chatbot that responds to user queries related to travel.

#### 🔥 Capabilities:

* 📍 Nearby places
* 🍽️ Food suggestions
* 🚗 Transport guidance
* 🎉 Best time to visit
* 📅 Travel plans

#### 🧠 Example Queries:

* "Places near Madurai"
* "What to eat in Chennai"
* "3 day plan in Ooty"
* "Best time to visit Kodaikanal"
* "How to travel in Rameswaram"

---

### 👤 User System

* User registration and login
* Profile management
* Like places
* Add reviews

---

### 📊 Data Handling

* Uses database (Place model)
* Stores place details and categories
* Dynamic suggestions based on data

---

## 🛠️ Tech Stack

| Layer          | Technology            |
| -------------- | --------------------- |
| Backend        | Django (Python)       |
| Frontend       | HTML, CSS, JavaScript |
| Database       | SQLite                |
| Authentication | Django Auth           |

---

## 🏗️ Project Architecture

```id="arch2"
Frontend (HTML/CSS/JS)
        ↓
Django Views
        ↓
Database (Place Model)
        ↓
Dynamic Response (Chatbot + Pages)
```

---

## 📂 Project Structure

```id="structure2"
Tamilverse_app/
│
├── accounts/           # Authentication system
├── places/             # Place data + chatbot logic
├── interactions/       # Likes and reviews
├── templates/          # HTML pages
├── static/             # CSS, JS, images
├── config/             # Settings and URLs
├── manage.py
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash id="c1"
git clone https://github.com/your-username/tamilverse.git
cd tamilverse
```

### 2️⃣ Create Virtual Environment

```bash id="c2"
python -m venv venv
```

### 3️⃣ Activate Environment

```bash id="c3"
venv\Scripts\activate   # Windows
```

### 4️⃣ Install Dependencies

```bash id="c4"
pip install -r requirements.txt
```

### 5️⃣ Apply Migrations

```bash id="c5"
python manage.py migrate
```

### 6️⃣ Run Server

```bash id="c6"
python manage.py runserver
```

### 7️⃣ Open Browser

```text id="c7"
http://127.0.0.1:8000
```

---

## 🧪 Sample Queries

* "Places near Madurai"
* "What to eat in Madurai"
* "Best time to visit Ooty"
* "3 day travel plan in Kodaikanal"
* "How to travel in Chennai"

---

## ⚠️ Challenges Faced

* Connecting frontend chatbot with backend
* Handling CSRF issues in requests
* Managing dynamic place routing
* Avoiding crashes due to missing data

---

## 💡 Solutions Implemented

* Used safe backend logic to avoid errors
* Added CSRF handling in frontend requests
* Implemented slug-based routing
* Built structured chatbot logic

---

## 🚀 Future Enhancements

* AI-based chatbot
* Voice interaction
* Google Maps integration
* Multi-language support
* Mobile application version

---

## 👨‍💻 Author

Afrin S
Harshini G
Johnshi Elena A
B.E CSE (AI & ML)

---

## 📌 Conclusion

Tamilverse is a clean and scalable travel assistant that demonstrates full-stack development using Django. It provides a smooth user experience with intelligent responses and structured data handling.

---
