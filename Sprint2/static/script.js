import { recipes } from "./recipes.js";

const selectedFilters = new Set();
const filterButtons = document.querySelectorAll(".filter-button");
const clearButton = document.querySelector(".clear-button");
const recipeGrid = document.querySelector(".recipe-grid");
const recipeCount = document.querySelector(".recipe-count");
const emptyState = document.querySelector(".empty-state");

const filterMatches = (recipe, filter) => {
  if (filter === "vegetarian") {
    return recipe.tags.includes("vegetarian") || recipe.tags.includes("vegan");
  }

  return recipe.tags.includes(filter);
};

const formatTag = (tag) => ({
  protein: "High protein",
  carbs: "Carbs",
  fiber: "High fiber",
  vegetarian: "Vegetarian",
  vegan: "Vegan"
})[tag];

const createRecipeCard = (recipe) => {
  const article = document.createElement("article");
  article.className = "card";

  const heading = document.createElement("h3");
  heading.className = "card-title";
  heading.textContent = recipe.name;
  article.append(heading);

  const tags = document.createElement("ul");
  tags.className = "tag-list";
  tags.setAttribute("aria-label", "Recipe tags");
  for (const tag of recipe.tags) {
    const item = document.createElement("li");
    item.className = "tag";
    item.textContent = formatTag(tag);
    tags.append(item);
  }
  article.append(tags);

  const prep = document.createElement("p");
  prep.className = "prep-time";
  prep.textContent = `${recipe.prepMinutes} min prep`;
  article.append(prep);

  const ingredientsHeading = document.createElement("h4");
  ingredientsHeading.className = "card-subheading";
  ingredientsHeading.textContent = "Ingredients";
  article.append(ingredientsHeading);

  const ingredients = document.createElement("ul");
  ingredients.className = "ingredient-list";
  for (const ingredient of recipe.ingredients) {
    const item = document.createElement("li");
    item.className = "ingredient-item";
    item.textContent = ingredient;
    ingredients.append(item);
  }
  article.append(ingredients);

  const stepsHeading = document.createElement("h4");
  stepsHeading.className = "card-subheading";
  stepsHeading.textContent = "Steps";
  article.append(stepsHeading);

  const steps = document.createElement("ol");
  steps.className = "steps-list";
  for (const step of recipe.steps) {
    const item = document.createElement("li");
    item.className = "step-item";
    item.textContent = step;
    steps.append(item);
  }
  article.append(steps);

  return article;
};

const renderRecipes = () => {
  const visibleRecipes = recipes.filter((recipe) =>
    [...selectedFilters].every((filter) => filterMatches(recipe, filter))
  );

  recipeGrid.replaceChildren(...visibleRecipes.map(createRecipeCard));
  recipeCount.textContent = `Showing ${visibleRecipes.length} of ${recipes.length} recipes`;
  emptyState.hidden = visibleRecipes.length !== 0;
  recipeGrid.hidden = visibleRecipes.length === 0;

  for (const button of filterButtons) {
    button.setAttribute("aria-pressed", String(selectedFilters.has(button.dataset.filter)));
  }
};

for (const button of filterButtons) {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    if (selectedFilters.has(filter)) {
      selectedFilters.delete(filter);
    } else {
      selectedFilters.add(filter);
    }
    renderRecipes();
  });
}

clearButton.addEventListener("click", () => {
  selectedFilters.clear();
  renderRecipes();
});

renderRecipes();
