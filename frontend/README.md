# 🎨 Frontend – React.js + Bootstrap

This is the frontend for the Gemini-powered Quiz Generator.

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

Runs the app in development mode.
Open `http://localhost:3000` to view it in your browser.

---

## 📁 Folder Structure

- `components/` – Reusable pages and UI components
- `api/api.js` – Axios instance for backend communication
- `App.js` – Main routing logic
- `Navbar.js` – Top-level navigation with dark mode toggle

--- 

## 💡 Notes

- Dark mode state is passed as props to all major pages.
- Components adapt using Bootstrap class variants.
- The app currently uses mocked quiz data until backend integration.

---

## 🔧 Available Scripts (via Create React App)

-- In the `frontend/` directory, you can run:
```bash
npm start
```
Runs the app in development mode.
```bash
npm test
```
Launches the test runner in interactive watch mode.
```bash
npm run build
```
Builds the app for production into the `build/` folder.
```bash
npm run eject
```
**Warning: This is a one-way operation. Once you `eject`, you can’t go back!**

---

## 📚 Learn More

- [React documentation](https://reactjs.org/).
- [Bootstrap Docs](https://getbootstrap.com/)
- [Create React App Guide](https://facebook.github.io/create-react-app/docs/getting-started).

---

## Related Docs

- [System Overview](../docs/architecture/overview.md)
- [API Design](./architecture/api_design.md)

---