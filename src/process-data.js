// Load .env file
require('dotenv').config()

// fs module
const fs = require('fs');

// Load anylist API
const AnyList = require('anylist');
const any = new AnyList({
  email: process.env.ANYLIST_USERNAME,
  password: process.env.ANYLIST_PASSWORD
});

any.login().then(async () => {

  // Get all the user data from AnyList
  const result = await any.client.post('data/user-data/get');
  const decoded = any.protobuf.PBUserDataResponse.decode(result.body);

  // Get the recipe data
  const recipeData = decoded.recipeDataResponse.recipes;

  // Get the meal plan data
  const mealPlanResponse = decoded.mealPlanningCalendarResponse;
  const mealPlanEvents = mealPlanResponse.events;
  const mealPlanLabels = mealPlanResponse.labels;

  // Save recipes
  fs.writeFile("data/recipes.json", JSON.stringify(recipeData), function (err) {
    if (err) {
      return console.log(err);
    }
  });

  // Save meal plan data
  fs.writeFile("data/meal-plan.json", JSON.stringify(mealPlanEvents), function (err) {
    if (err) {
      return console.log(err);
    }
  });
  fs.writeFile("data/meal-plan-labels.json", JSON.stringify(mealPlanLabels), function (err) {
    if (err) {
      return console.log(err);
    }
  });


  any.teardown();
});