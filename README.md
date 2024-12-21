# API Documentation
## Swagger API documentation 
<img width="1409" alt="Screenshot 2024-12-21 at 10 06 42 PM" src="https://github.com/user-attachments/assets/232583ee-e492-4442-9def-db54427a84a4" />


## Recipes API

### 1. Get All Recipes
- **Route**: `/recipes/`
- **Method**: GET
- **Description**: Fetch all available recipes.
- **Query Parameters**:
  - `cuisine_type` (optional): Filter recipes by cuisine type.
  - `difficulty_level` (optional): Filter recipes by difficulty level.
  - `is_vegetarian` (optional): Filter recipes by vegetarian status (true/false).
- **Sample Response**:
```json
[
  {
    "name": "Pasta Carbonara",
    "cuisine_type": "Italian",
    "preparation_time": 15,
    "cooking_time": 20,
    "difficulty_level": "Easy",
    "taste_profile": "Savory",
    "instructions": "Boil pasta. Cook bacon. Mix eggs, cheese, and pepper. Combine all ingredients.",
    "ingredients": [
      {
        "ingredient_name": "Pasta",
        "quantity": 200,
        "unit": "grams"
      },
      {
        "ingredient_name": "Bacon",
        "quantity": 100,
        "unit": "grams"
      },
      {
        "ingredient_name": "Egg",
        "quantity": 2,
        "unit": "pieces"
      }
    ],
    "id": 1,
    "user_id": "user123",
    "average_rating": 4.5,
    "number_of_reviews": 10,
    "vector_store_id": "vector_123",
    "created_at": "2024-12-21T15:17:13.579Z",
    "is_vegetarian": false
  }
]
```

### 2. Add a New Recipe
- **Route**: `/recipes/`
- **Method**: POST
- **Description**: Add a new recipe.
- **Request Body**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "is_vegetarian": false
}
```
- **Sample Response**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "id": 0,
  "user_id": "string",
  "average_rating": 0,
  "number_of_reviews": 0,
  "vector_store_id": "string",
  "created_at": "2024-12-21T15:17:13.582Z",
  "is_vegetarian": false
}
```

### 3. Get Recipe by ID
- **Route**: `/recipes/{recipe_id}`
- **Method**: GET
- **Description**: Fetch a single recipe by its ID.
- **Sample Response**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "id": 0,
  "user_id": "string",
  "average_rating": 0,
  "number_of_reviews": 0,
  "vector_store_id": "string",
  "created_at": "2024-12-21T15:17:13.582Z",
  "is_vegetarian": false
}
```

### 4. Update Recipe by ID
- **Route**: `/recipes/{recipe_id}`
- **Method**: PUT
- **Description**: Update an existing recipe by its ID.
- **Request Body**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "is_vegetarian": false
}
```
- **Sample Response**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "id": 0,
  "user_id": "string",
  "average_rating": 0,
  "number_of_reviews": 0,
  "vector_store_id": "string",
  "created_at": "2024-12-21T15:17:13.588Z",
  "is_vegetarian": false
}
```


### 4. Upload Recipe Image  
- **Route**: `/recipes/image`  
- **Method**: `POST`  
- **Description**: Upload an image for a recipe and get the recipe details.

- **Request Body**:
```json
{
  "file": "<binary_file>"
}
```

- **Sample Response**:
```json
{
  "name": "string",
  "cuisine_type": "string",
  "preparation_time": 0,
  "cooking_time": 0,
  "difficulty_level": "string",
  "taste_profile": "string",
  "instructions": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "quantity": 0,
      "unit": "string"
    }
  ],
  "id": 0,
  "user_id": "string",
  "average_rating": 0,
  "number_of_reviews": 0,
  "vector_store_id": "string",
  "created_at": "2024-12-21T15:25:27.134Z"
}
```

## Ingredients API

### 1. Get All Ingredients
- **Route**: `/ingredients/`
- **Method**: GET
- **Description**: Fetch all available ingredients.
- **Sample Response**:
```json
[
  {
    "name": "string",
    "quantity": 0,
    "unit": "string",
    "category": "string",
    "expiry_date": "2024-12-21T15:25:27.145Z",
    "id": 0,
    "user_id": "string",
    "last_updated": "2024-12-21T15:25:27.145Z"
  }
]
```

### 2. Add a New Ingredient
- **Route**: `/ingredients/`
- **Method**: POST
- **Description**: Add a new ingredient.
- **Request Body**:
```json
{
  "name": "string",
  "quantity": 0,
  "unit": "string",
  "category": "string",
  "expiry_date": "2024-12-21T15:25:27.145Z"
}
```
- **Sample Response**:
```json
{
  "name": "string",
  "quantity": 0,
  "unit": "string",
  "category": "string",
  "expiry_date": "2024-12-21T15:25:27.145Z",
  "id": 0,
  "user_id": "string",
  "last_updated": "2024-12-21T15:25:27.145Z"
}
```
## Chat API

### 1. Chat with Recipe Assistant  
- **Route**: `/chat/`  
- **Method**: `POST`  
- **Description**: Send a message to the recipe assistant and receive a response based on the query.

- **Request Body**:
```json
{
  "message": "How to Cook Poutine"
}
```

- **Sample Response**:
```json
"string"
```  

