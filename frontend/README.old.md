# 🎨 Frontend – React.js + Bootstrap

This is the frontend for the Gemini-powered Quiz Generator.

---

## Purpose
React.js frontend that allows users to upload files, take quizzes, and view results.

---

## ✅ Features Implemented

- File upload (PDF/DOCX)
- Dynamic quiz rendering
- Results page with answer explanations
- Dark mode toggle (theme-aware styling)
- Navigation using React Router
- Bootstrap styling for all components

---

## 🛠️ Getting Started

```bash
cd frontend
npm install
npm start
```
---

## 📁 Folder Structure

- components/ – Reusable pages and UI components
- api/api.js – Axios instance for backend communication
- App.js – Main routing logic
- Navbar.js – Top-level navigation with dark mode toggle

---

## 💡 Notes

- Dark mode state is passed as props to all major pages.
- Components adapt using Bootstrap class variants.
- The app currently uses mocked quiz data until backend integration.

---

## Dependencies
- React.js
- Bootstrap
- Axios

---

## Related Docs
- [System Overview](../docs/architecture/overview.md)

