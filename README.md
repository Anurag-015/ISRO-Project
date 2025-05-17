# 🚀 ISRO Project - Item Tracking and Management System

This project is a **web-based tracking and item management system**, built using Python, HTML, JavaScript, and Docker. Designed with modularity and ease-of-use in mind, it can be used in scenarios like warehouse inventory, logistics, or even space agency equipment monitoring.

---

## 🧰 Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask likely)
- **Deployment**: Docker
- **Database**: (Assumed local file or SQLite — check `logs.py`)
- **Others**: Modular Python scripts for placement, retrieval, and logging

---

## 📂 Project Structure

```plaintext
ISRO-Project/
├── static/                  # Static assets like CSS, JS
├── templates/               # HTML pages
│   ├── add_items.html
│   ├── activity.html
│   ├── dashboard.html
│   └── login.html
├── app.py                   # Main Flask app (entry point)
├── placement.py             # Handles item placement logic
├── retrieval.py             # Handles item retrieval logic
├── logs.py                  # Logging system
├── config.py                # Configurations
├── container.py             # Container functions (possibly Docker simulation)
├── requirements.txt         # Python dependencies
├── Dockerfile               # For containerizing the app
└── README.md
````

---

## 🚀 Features

* 🔐 **User Login**: Secure login system
* 📦 **Add Items**: Add new items to the system via a user-friendly form
* 📊 **Dashboard**: Overview of items and status
* 📁 **Activity Logs**: Track placements, retrievals, and system events
* 🧠 **Container Simulation**: Supports logical containers for item grouping
* 🐳 **Docker Support**: Easily containerize and deploy the application

---

## 🛠️ Installation

### 🔧 Prerequisites

* Python 3.x
* pip (Python package manager)
* Docker (optional but recommended)

### 📥 Clone the repository

```bash
git clone https://github.com/Anurag-015/ISRO-Project.git
cd ISRO-Project
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🐳 Docker Setup (Optional)

To run the app in Docker:

```bash
# Build the Docker image
docker build -t isro-project .

# Run the Docker container
docker run -d -p 5000:5000 isro-project
```

Then go to [http://localhost:5000](http://localhost:5000)

---

## 📸 Screenshots (Optional)

Add screenshots of:

* Login Page
* Dashboard
* Add Items Page
* Activity Logs

---

## 👨‍💻 Author

**Anurag Gupta**
[GitHub Profile](https://github.com/Anurag-015)

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


