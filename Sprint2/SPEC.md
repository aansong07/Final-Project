# SPEC: Recipe Finder
## 1. Purpose & Scope
- A single-page recipe finder for one user. the user picks dietary/nutrition
  filters and the page shows recipes that match.
- Filters: Protein, Carbs, Fiber, Vegetarian, Vegan.
- Non-Goals: no multi-page routing; no accounts or login;
  no saving favorites; no user-submitted recipes; no external recipe APIs.

## 2. Invariants & Negative Constraints
- All styling MUST reside in `./style.css` (no inline style="..." attributes).
- All behavior MUST reside in `./script.js` (no inline onclick="..." attributes).
- Recipe data MUST live in one place: a `recipes` array in `./recipes.js`
  Recipes MUST NOT be hardcoded in index.html or script.js. recipes.js is deleted once the frontend uses fetch().
- The page MUST NOT load external CSS frameworks, JS frameworks, or CDNs
  (no Bootstrap, no Tailwind, no React, no jQuery).
- style.css MUST begin with the universal reset: `*, *::before, *::after {
  box-sizing: border-box; }`.
- Spacing and font sizes MUST use rem. px MAY be used only for borders.
- Styling MUST use class selectors. ID selectors MUST NOT be used for styling.
- The layout MUST collapse into a single vertical column on screens narrower
  than 768px.
- Filter state MUST NOT be stored in the DOM only; it MUST live in a JS
  variable and the UI MUST be re-rendered from it.

## 3. UI Content & Interface Contract
### 3.1 Page structure
- Semantic landmarks: one <header>, one <nav>, one <main>, one <footer>,
  and each content group inside its own <section> with a heading.
- Exactly one <h1> ("<Recipe Finder>"); heading levels MUST NOT skip.
- Header: site title and a one-line subtitle: "<Pick a goal, get a recipe.>".
- <nav> MUST contain links to the filters section and the recipes section.

### 3.2 Filters section (id="filters")
- Five clickable filter buttons: Protein, Carbs, Fiber, Vegetarian, Vegan.
- Each MUST be a real <button type="button">, not a <div> or <span>.
- Each MUST expose its state with `aria-pressed="true|false"`.
- Selected buttons MUST look visibly different from unselected ones.
- A "Clear filters" button MUST reset all filters and show all recipes.
- Filter logic: <decide: multiple filters combine with AND (recipe must match
  all selected) or OR (match any)>.
- Vegan recipes MUST also count as vegetarian. <confirm or change>.
- Add-recipe form: name, prep minutes, tags, ingredients, steps, and a submit button, each with a <label>.

### 3.3 Recipes section (id="recipes")
- Each recipe MUST be an <article class="card"> inside a container that uses
  display: flex, flex-wrap: wrap and gap.
- Each card MUST show: recipe name, tag list (e.g., "High protein", "Vegan"),
  prep time, ingredients list, and short steps.
- When no recipe matches, the section MUST show a message:
  "<No recipes match those filters yet.>".
- The recipe count MUST be displayed ("Showing X of Y recipes") and
  announced via `aria-live="polite"`.

### 3.4 Recipe data contract
- Each recipe object MUST have this shape:
  `{ id, name, tags: [...], prepMinutes, ingredients: [...], steps: [...] }`
- Allowed tags: "protein", "carbs", "fiber", "vegetarian", "vegan".
- Minimum starter content: <at least 8 recipes, with at least 1 per tag>.

### 3.5 Visual design
- Page background: <#hex>; text color: <#hex>; accent color: <#hex>.
- Headings SHOULD use a serif font such as Georgia; body uses <system sans-serif>.
- Cards MUST have rounded corners and a visible hover state.

### 3.6 Button states (filters)
- Filter buttons MUST have four visually distinct states: :hover,
  :focus-visible, :active, and a selected state ([aria-pressed="true"]).
- All state rules MUST live in style.css.

## 4. Backend
- app.py runs on localhost:5000 and serves the page and the API
- Phase 1 stores recipes in a Python list.
- Read request data with .get() and clean it: strip whitespace from strings, make prepMinutes an integer, and only accept the allowed tags.
- if a ewquired field is missing or invalid return 400 and a JSON error message that syays what is wrong.
- Return a JSON error for 404 and 500.
- | Method | Path | Success | Errors |
| GET | /api/recipes | 200 | 500 |
| GET | /api/recipes/<id> | 200 | 404 |
| POST | /api/recipes | 201 | 400 |
| PUT | /api/recipes/<id> | 200 | 400, 404 |
| DELETE | /api/recipes/<id> | 204 | 404 |

## 5. Database 
- A recipes table with id INTEGER PRIMARY KEY AUTOINCREMENT, name, prep_minutes, tags, ingredients, and steps. Lists are stored as JSON text and converted back to lists in the API.
- Routes use SELECT, INSERT, UPDATE, and DELETE with ? placeholders.
- Create the table and add the starter recipes on startup if the table is empty.
- Routes, JSON shapes, and status codes stay the same as Phase 1.
- Data MUST survive stopping (Ctrl+C) and restarting the server.
Add recipes.db to .gitignore.

## 6. Frontend Wiring
- script.js uses fetch() for all data. On page load it gets /api/recipes and saves the result in a JS variable used to render.
- Update the page based on the status code:
- 201: show the new recipe and clear the form.
- 204: remove the deleted recipe's card.
- 400: show the error messages next to the form and keep what was typed.
- 404 or 500: show a short, friendly error message.


## 8. Acceptance Checklist
- [ ] Exactly one <h1>, one <header>, one <nav>, one <main>, one <footer>.
- [ ] No inline style="..." or onclick="..." attributes in index.html.
- [ ] style.css begins with the box-sizing reset.
- [ ] No ID selectors (#something) in style.css.
- [ ] No external CSS/JS loaded (check the Network tab).
- [ ] Every recipe is an <article class="card"> inside a flex container with gap.
- [ ] Clicking a filter updates the visible recipes immediately.
- [ ] Clicking the same filter again turns it off.
- [ ] "Clear filters" shows all recipes again.
- [ ] Selecting a combination with no matches shows the empty-state message.
- [ ] Filters are usable with keyboard only (Tab, Enter/Space).
- [ ] Tabbing to a filter shows a clear focus ring.
- [ ] No horizontal scrollbar when the browser is narrowed to 375px.
- [ ] app runs on localhost:5000
- [ ] Each API route returns the right status code (200, 201, 204, 400, 404).
- [ ] Bad input (missing name, bad prep time) returns 400 with a message.
- [ ] No hardcoded recipes remain in the frontend.
- [ ] Add, edit, and delete a recipe, restart the server: changes are still there.
- [ ] Git history has many small commits with clear messages.

## 9. Audit Protocol
- Inspect the generated code line by line with `git diff --staged` before
  committing.
- Test each acceptance item manually in the browser before marking it [x].
- Verify every recipe's tags match its ingredients (e.g., no meat in a
  "vegan" recipe).