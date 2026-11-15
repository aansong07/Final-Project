1. My website Yummy Eats is a single-page recipe finder. Intially when the webpage loads the script.js finds all the recipes from the Flask and filters them by category. The user then picks which recipes they would like to see and then can also add a recipe with the the form option.
                     API Contract Table 
_Method_ | _Source Field_  |   _Request_  | _Success_ | _Errors_
GET    | /api/recipes      | none         | 200       | 500
GET    | /api/recipes/<id> | none         | 200       | 404
POST   | /api/recipes      | name,        | 201       | 400
       |                     prepMinutes, |
       |                     tags,        | 
       |                     ingredients, |
       |                     steps        |
PUT    | /api/recipes/<id> | same as POST | 200       | 400
DELETE | /api/recipes/<id> | none         | 204       | 404


2.  Column       | Type    | Contraints  
    id             integer   primary key   
    name           text      not null
    prep_minutes   text      not null
    tags           text      not null
    ingredients    text      not null
    steps          text      not null

3.  Step 1: install python and make sure the verion is correct
    Step 2: install the flask 
    Step 3: start the server (python app.py )
    Step 4: using http://localhost:5000 open your browser and test the filters and look at the recipe result count to ensure that the filters work. Then use the clear filters and check the the recipe result count go back to its orginal number. Then use the recipe from to create your own.

4.  I used Claude to help me with the Section 5 and 6 of the SPEC.md along with some parts of the checklist. I used copilot to implement the chnages in my SPEC.md      along with debugging. I also uses claude to help me write some of the commits as I was unsure what excactly to write in a clear a concice way. 
