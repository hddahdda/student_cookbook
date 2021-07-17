# A Student's cookbook

# About

Student Cookbook is a collaborative cookbook for students by students. It's use is, however, not restricted to just students. The website can be used or viewed by anyone interested in a cheap meal. The main focus group for the project is students whereas this is one group that for some time in a lot of cases are affected by a restricted economy. It will serve as a source of inspiration when it comes to cheap and preferably easy cooking, something some students even barely do. 

### User Stories 
* Students 
* Anyone with a restricted economy
* People interested in cooking aka "foodies"
* A user who wishes to be able to filter their recipy search based on different diet categories.
* A user who wishes to able to filter their recipy search based on estimated ingredient cost. 

As previously elaborated in the "About" section the conecpt of this website is to cater to the estimated needs of a student with restricted economy and scheduale. In this day and age young a lot of young people also have restricted diets, whereas many are vegeterian or vegan or might have chosen to exclude for example gluten. 

### Reasons for the website
* A website for browsing recipes with few or cheap ingredients 
* A website where the user has the possibility to register, log in and thereby being able to add their own recipes
* Inspirational, for the user that has a lack of inspiration and wants to seek cooking inspiration 

# Scope

### What the user may expect
* For the concept of the website to be clear and easily understood
* For the website to be intutitive and easy to use aka functional design.
* To be able to view recipes
* As the concept of the website is to be a collaborative cookbook, the user might expect to be able to add recipes.

### What the user may want
* To be able to add and edit their own recipes.
* To be able to register to make sure that recipes added by them could not easily be edited or deleted by other users.
* A search bar which makes it possible to filter recipes by ingredients, recipy name, category etc. 

# Structure 
## Wireframes

## Design 
### Colors

### Fonts

# Features

## Features left to include
* For the user to be able to star a recipy and thereby get access to these on their profile page.
* For the user to be able to edit and/or deletetheir own recipes from their profile page.
* 404 Not Found, 500 internal error, 403 forbidden. 
https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
* For the user to be able to add a recipe image (using a link as a image source)
* Search recipes functionality 

### Bugs
* Bug 1: When adding a new recipe to the database this appears in the middle of the row below the other recipes, this doesn't affect functionality, however It looks odd and misplaced.

Update Bug 1: After making the changes described above, changing "pricing" and "cooking_time" to be separate objects instead of keys, the choices does no longer add one choice every time a recipe is added. However when browsing the "estimated pricing" dropdown menu the prices are not in the correct order. It probably needs to be sorted in a different way.


* Bug 2: When adding a new recipe to the database, the chosen pricing and cooking time also gets added to the database, so the same value reappears in the dropdown menu. This, I think, will have to be resolved by manually adding these as separate objects to the database instead of, as it is for the moment, only appearing in database as separate keys in different objects. 

### Credits 
* "Flask Mini-Project" which is one module from Code Institutes course was of big use when creating my project. This was of big help regarding how to structure the work, learning Materialize and naming conventions. Quite a lot of my websites design is partly based on this module.
* Code snippet from "Flask Mini Project" that is located in static/js/script.js file. This code snippet allows the Materialize dropdown menu to actually be "reqired" as it otherwise defaults to not required.

#### Images
These are the images uploaded manually by me to the website, however images uploaded or, more accurately, linked to by other users will not be able to be credited. 
https://unsplash.com/photos/12eHC6FxPyg




