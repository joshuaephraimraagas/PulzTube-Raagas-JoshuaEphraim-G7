# PulzTube: Your Personal YouTube Growth and Content Management Assistant
 
**Course:** IT317 (Project Management) - Section G9  
**Product Owner:** Joshua Ephraim Raagas  
**Institution:** Cebu Institute of Technology - University (CIT-U)  
**Project Sponsor:** Joemarie Amparo  

---

## 1. Project Overview
PulzTube is a full-stack Django web application designed to help aspiring YouTubers improve their content strategy through structured evaluation, workflow organization, and automated channel growth tracking.

---

## 2. Technology Stack
* **Backend & Frontend:** Full-Stack Django 6.1 (with Django Templates & Bootstrap 5)
* **Database:** PostgreSQL / Supabase (configured via `.env` with local SQLite fallback for development)
* **Authentication:** Custom User model (`accounts.CustomUser`) with Django built-in password hashing

---

## 3. Implemented Features (Phase 1: Account Feature)

### A. Account Registration (`/accounts/signup/`)
* Input validation for required fields, valid email format, matching password confirmation.
* **Strict Unique Email & Username Validation** (custom clean validation rejecting duplicate emails).
* Secure password hashing using Django's auth system.
* Clear feedback messages via `django.contrib.messages`.

### B. Login / Logout (`/accounts/login/`, `/accounts/logout/`)
* Custom authentication form with invalid credentials feedback.
* Session termination on logout.
* `@login_required` / `LoginRequiredMixin` protecting all private views.

### C. Role-Based User Dashboard
* **Two Roles:** `CREATOR` (Content Creator) and `ADMIN` (Administrator).
* **Automatic Role Dispatch:** Users are automatically redirected to their specific dashboard upon login:
  * Creator $\rightarrow$ `/creator/`
  * Admin $\rightarrow$ `/admin-panel/`
* **Strict URL Security:** Users cannot bypass roles by typing URLs:
  * If a Creator attempts to access `/admin-panel/`, access is denied and they are redirected back with a warning alert.
  * If an Admin accesses `/creator/`, they are redirected to `/admin-panel/`.

### D. User Profile (`/accounts/profile/`, `/accounts/profile/edit/`)
* Logged-in users can view their profile and channel preferences.
* Update profile details (first name, last name, email, channel name, channel handle/ID, niche, content interests, contact number, profile photo).
* **Strict Privacy:** Users can **only** view and edit their own profile (`request.user`).

---

## 4. Getting Started

### Local Setup Instructions:
1. **Activate virtual environment:**
   ```bash
   ..\campusconnectg7\.venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   * Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   * Add your Supabase / PostgreSQL database connection string into `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```
4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the Automated Test Suite:**
   ```bash
   python manage.py test
   ```
6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
"# PulzTube-Raagas-JoshuaEphraim-G7" 
