# Mini Shop (Session 2)

Small shop demo. Back-end holds products. Front-end shows them.

## Folders

- `backend/main.py` — FastAPI server. Holds products and cart in `products.db`.
- `frontend/index.html` — Page shell. Holds `#tagline` and `#product-grid`.
- `frontend/style.css` — Look of the page.
- `frontend/script.js` — Live code. No comments by choice.
- `frontend/script.cleaned.js` — Same logic, cleaned up, with comments.

## How to run

1. Start back-end on port 8003:

   ```bash
   cd backend
   uv run uvicorn main:app --port 8003
   ```

2. Open front-end:
   - Open `frontend/index.html` in a browser, or
   - Serve it, e.g. `cd frontend && python3 -m http.server 5500`.

Front-end calls `http://localhost:8003`, so back-end must be up first.

## API

- `GET /products` — List all products.
- `PUT /products/add-to-cart/{id}` — Add one item to cart.
  - Good: `{ success: true, message, products }`
  - Bad: `{ detail }` with code 400 or 404:
    - `Item is already in cart`
    - `Product not found`
    - `This item is out of stock`

## Front-end notes

- `queryProducts` uses promise chains. It fits a straight line: fetch, parse, draw.
- `addToCart` uses async/await. It fits a branch: wait, then check good vs bad.
- Key fix: `fetch` does not throw on 400/404. You must check `response.ok` by hand. Then read `data.detail` for errors and `data.message` for success.
