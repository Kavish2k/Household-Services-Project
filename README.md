# 🏠 Household Services Application

## 🚀 Project Title: 
**Abode Mantra: Your A-Z Cleaning Experts**

## Project Demo Video: https://drive.google.com/file/d/1Kd8GeC4Gw6U379XNQ8HrCnM6g1parl2P/view?usp=sharing

---

## 📚 Frameworks and Libraries Used:
- **Python**: 3.11.9 🐍
- **SQLite**: 3.46.1 💾
- **Flask**: 3.0.2 🌐
- **Flask-SQLAlchemy**: 3.1.1 🛠️
- **Bootstrap**: 5.3.3 🎨
- **Jinja2**: 3.1.3 🔗
- **bcrypt**: 4.2.0 🔒
- **ChartJS**: 4.4.4 📊
- **datetime**: Python’s Inbuilt Library ⏰
- **HTML, CSS, JavaScript**: Used for creating the frontend. 🖼️
- **Frontend Validation**: Added validation on forms to ensure proper data input before submission. ✅

---

## 📝 Abstract:
This project is a multi-user application designed for **Admin**, **Customers**, and **Professionals**, providing comprehensive home servicing and solutions. The development was structured in phases:

1. **Database Initialization**: Created tables for users, services, and requests with SQLite3, incorporating password hashing with bcrypt.
2. **Coding Environment Setup**: Modularized code and implemented Bootstrap for UI and Jinja2 for templates.
3. **Frontend Development**: Leveraged HTML, CSS, and JavaScript to create an intuitive and responsive user interface, including **frontend validation on forms** for better user experience and data integrity.
4. **Controllers Development**: Handled different user roles using Flask and Flask-SQLAlchemy.
5. **Testing**: Utilized dummy data to verify the backend and frontend functionality.

---

## 🌟 Core Functionalities:

### 👨‍💼 Admin:
1. Manage services (Create, Edit, Delete).
2. Cascade delete service-related records upon service deletion.
3. Approve/Reject new professionals.
4. Monitor all service requests.
5. Search and block/unblock users with restricted access post-blocking.
6. Summarize service ratings and statuses.

### 🧍 Customer:
1. Book, close, or cancel services by pin code.
2. Book different service types simultaneously.
3. View and rate services/professionals.
4. Edit profile and search past/current requests.
5. Summarize ratings for services and professionals.

### 🛠️ Professional:
1. Accept requests based on pin code and service type.
2. Handle one request at a time, allowing subsequent requests post-completion.
3. View past/current requests and edit profile.
4. Summarize customer ratings and request statuses.

---

## 📌 ER Diagram:
![ER Diagram](MAD-1-Household%20Services%20Project/ER%20DIAGRAM.png)

---
