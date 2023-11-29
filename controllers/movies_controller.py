from flask import Blueprint, jsonify, request, abort
from main import db
from models.movies import Movie
from schemas.movie_schema import movie_schema, movies_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User

movies = Blueprint('movies', __name__, url_prefix="/movies")

# GET
@movies.route("/", methods=["GET"])
def get_movies():
    stmt = db.select(Movie)
    movies = db.session.scalars(stmt)
    return movies_schema.dump(movies)

@movies.route("/<int:id>/", methods=["GET"])
def get_movie(id):
    stmt = db.select(Movie).filter_by(id=id)
    movie = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not movie:
        return abort(400, description= "Movie does not exist")
    # Convert the movies from the database into a JSON format and store them in result
    result = movie_schema.dump(movie)
    # return the data in JSON format
    return jsonify(result)

# UPDATE

@movies.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_movie(id):
    # #Create a new movie
    movie_fields = movie_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the movie
    stmt = db.select(Movie).filter_by(id=id)
    movie = db.session.scalar(stmt)
    #return an error if the movie doesn't exist
    if not movie:
        return abort(400, description= "movie does not exist")
    #update the movie details with the given values
    movie.title = movie_fields["title"]
    movie.genre = movie_fields["genre"]
    movie.length = movie_fields["length"]
    movie.year = movie_fields["year"]
    # add to the database and commit
    db.session.commit()
    #return the movie in the response
    return jsonify(movie_schema.dump(movie))

# POST
@movies.route("/", methods=["POST"])
#Decorator to make sure the jwt is included in the request
@jwt_required()
def card_create():
    #Create a new card
    movie_fields = movie_schema.load(request.json)

    new_movie = Movie()
    new_movie.title = movie_fields["title"]
    new_movie.genre  = movie_fields["genre"]
    new_movie.length = movie_fields["length"]
    new_movie.year = movie_fields["year"]
    
    # add to the database and commit
    db.session.add(new_movie)
    db.session.commit()
    #return the card in the response
    return jsonify(movie_schema.dump(new_movie))

# DELETE
@movies.route("/<int:id>", methods=["DELETE"])
@jwt_required()
#Includes the id parameter
def movies_delete(id):
    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the card
    stmt = db.select(Movie).filter_by(id=id)
    movie = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not movie:
        return abort(400, description= "Movie entry doesn't exist")
    #Delete the card from the database and commit
    db.session.delete(movie)
    db.session.commit()
    #return the movie in the response
    return jsonify(movie_schema.dump(movie))


# SEARCH
@movies.route("/search", methods=["GET"])
def search_movies():
    # create an empty list in case the query string is not valid
    movies_list = []

    if request.args.get('genre'):
        stmt = db.select(Movie).filter_by(genre= request.args.get('genre'))
        movies_list = db.session.scalars(stmt)
    elif request.args.get('year'):
        stmt = db.select(Movie).filter_by(year= request.args.get('year'))
        movies_list = db.session.scalars(stmt)

    result = movies_schema.dump(movies_list)
    # return the data in JSON format
    return jsonify(result)