# djanX base static

This folder contains static assets for the project. Below are the sources for each asset:

| Asset             | NPM Source            | Node Modules Path                            | CDN Source                                                         |
| ----------------- | --------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| `alpinejs.min.js` | `npm i @alpinejs/csp` | `node_modules/@alpinejs/csp/dist/cdn.min.js` | `https://cdn.jsdelivr.net/npm/@alpinejs/csp@3.x.x/dist/cdn.min.js` |

---

**Note**: `tailwind.min.css` is built using the Django management command:

```bash
uv run python manage.py tailwind build
```
