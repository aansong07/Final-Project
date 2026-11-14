let recipes = [];
const selectedFilters = new Set();
const filterButtons = document.querySelectorAll(".filter-button");
const clearButton = document.querySelector(".clear-button");
const recipeGrid = document.querySelector(".recipe-grid");
const recipeCount = document.querySelector(".recipe-count");
const emptyState = document.querySelector(".empty-state");
const pageMessage = document.querySelector(".page-message");
const recipeForm = document.querySelector(".recipe-form");
const formMessage = document.querySelector(".form-message");

const showMessage = (element, message) => {
  element.textContent = message;
  element.hidden = false;
};

const clearMessage = (element) => {
  element.textContent = "";
  element.hidden = true;
};

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

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-button";
  deleteButton.type = "button";
  deleteButton.textContent = "Delete recipe";
  deleteButton.setAttribute("aria-label", `Delete ${recipe.name}`);
  deleteButton.addEventListener("click", () => deleteRecipe(recipe.id));
  article.append(deleteButton);

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

const loadRecipes = async () => {
  let response;
  try {
    response = await fetch("/api/recipes");
  } catch (error) {
    if (!(error instanceof TypeError)) {
      throw error;
    }
    showMessage(pageMessage, "We couldn't load recipes. Please check your connection and try again.");
    return;
  }

  if (response.status === 404 || response.status === 500) {
    showMessage(pageMessage, "We couldn't load recipes right now. Please try again later.");
    return;
  }
  if (!response.ok) {
    throw new Error(`Unexpected recipe response: ${response.status}`);
  }

  const loadedRecipes = await response.json();
  if (!Array.isArray(loadedRecipes)) {
    throw new Error("The recipe response was not a list.");
  }
  recipes = loadedRecipes;
  clearMessage(pageMessage);
  renderRecipes();
};

const deleteRecipe = async (recipeId) => {
  clearMessage(pageMessage);
  let response;
  try {
    response = await fetch(`/api/recipes/${encodeURIComponent(recipeId)}`, {
      method: "DELETE"
    });
  } catch (error) {
    if (!(error instanceof TypeError)) {
      throw error;
    }
    showMessage(pageMessage, "We couldn't delete that recipe. Please check your connection and try again.");
    return;
  }

  if (response.status === 204) {
    recipes = recipes.filter((recipe) => recipe.id !== recipeId);
    renderRecipes();
    return;
  }
  if (response.status === 404 || response.status === 500) {
    showMessage(pageMessage, "We couldn't delete that recipe. Please refresh and try again.");
    return;
  }
  showMessage(pageMessage, "We couldn't delete that recipe. Please try again.");
};

const listFromText = (value) =>
  value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);

recipeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessage(formMessage);

  const formData = new FormData(recipeForm);
  const payload = {
    name: formData.get("name"),
    prepMinutes: formData.get("prepMinutes"),
    tags: formData.getAll("tags"),
    ingredients: listFromText(formData.get("ingredients")),
    steps: listFromText(formData.get("steps"))
  };

  let response;
  try {
    response = await fetch("/api/recipes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  } catch (error) {
    if (!(error instanceof TypeError)) {
      throw error;
    }
    showMessage(formMessage, "We couldn't save that recipe. Please check your connection and try again.");
    return;
  }

  if (response.status === 201) {
    const newRecipe = await response.json();
    recipes.push(newRecipe);
    renderRecipes();
    recipeForm.reset();
    clearMessage(formMessage);
    return;
  }
  if (response.status === 400) {
    const result = await response.json();
    showMessage(formMessage, result.error || "Please check the recipe details and try again.");
    return;
  }
  if (response.status === 404 || response.status === 500) {
    showMessage(formMessage, "We couldn't save that recipe right now. Please try again later.");
    return;
  }
  showMessage(formMessage, "We couldn't save that recipe. Please try again.");
});

loadRecipes();
