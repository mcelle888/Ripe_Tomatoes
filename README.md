# ORM-challenge

The purpose of this challenge is to continue practicing with Flask, SQLAlchemy and Marshmallow. You are about to build the "Ripe Tomatoes" API that will provide information about the film industry (movies, actors, etc.).

The provided scaffold is very basic, to have it in your computer make sure you:

- Clone/fork the repo.
- Create the virtual environment.
- Install the requirements with ```pip install -r requirements.txt```
- Run the app with ```flask run```

If everything works fine let's go with the database creation:

- Open psql terminal.
- Create the ripe_tomatoes_db database and connect.
- Create the user "tomato" with a password of your choice and grant the privileges to access to the new database.
  
Back to the flask application these are tesks you need to to to complete the challenge:

- create the connection to the database you have just created. (Remember to install all the needed packages and then to store them in requirements.txt)
- Create the Movie and Actor models. From each movie we'd like to store the id, title, genre, length(in minutes) and release year. From each actor we'd like to store the id, first and last name, gender, country and date of birth. Feel free to add more attributes to each model, but don't add relationships between movies and actors, we'll work on this in further lessons.
- Create the cli commands that create and drop the tables.
- Create the cli command that seeds both tables. Seed them with at least two movies and 4 actors
- Create two routes ```/movies``` and ```/actors``` that print the information stored in the database in JSON format when there is a GET method request.

Challenge completed when these 3 routes show the following information (of course, movies and actors information don't match with your data.)

![postman screenshot with Welcome message](screenshots/root_get.png)
![postman screenshot with movies data](screenshots/movies_get.png)
![postman screenshot with actors data](screenshots/actors_get.png)
