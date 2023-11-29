from flask import Blueprint, jsonify, request, abort
from main import db
from models.actors import Actor
from schemas.actor_schema import actor_schema, actors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User

actors = Blueprint('actors', __name__, url_prefix="/actors")

@actors.route("/", methods=["GET"])
def get_actors():
    stmt = db.select(Actor)
    actors = db.session.scalars(stmt)
    return actors_schema.dump(actors)

@actors.route("/<int:id>/", methods=["GET"])
def get_actor(id):
    stmt = db.select(Actor).filter_by(id=id)
    actor = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not actor:
        return abort(400, description= "actor does not exist")
    # Convert the actors from the database into a JSON format and store them in result
    result = actor_schema.dump(actor)
    # return the data in JSON format
    return jsonify(result)

# CREATE
@actors.route("/", methods=["POST"])
#Decorator to make sure the jwt is included in the request
@jwt_required()
def actor_create():
    #Create a new card
    actor_fields = actor_schema.load(request.json)

    new_actor = Actor()
    new_actor.first_name = actor_fields["first_name"]
    new_actor.last_name  = actor_fields["last_name"]
    new_actor.gender = actor_fields["gender"]
    new_actor.country = actor_fields["country"]
    
    # add to the database and commit
    db.session.add(new_actor)
    db.session.commit()
    #return the card in the response
    return jsonify(actor_schema.dump(new_actor))


# UPDATE

@actors.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_actor(id):
    # #Create a new actor
    actor_fields = actor_schema.load(request.json)

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
    # find the actor
    stmt = db.select(Actor).filter_by(id=id)
    actor = db.session.scalar(stmt)
    #return an error if the actor doesn't exist
    if not actor:
        return abort(400, description= "actor does not exist")
    #update the actor details with the given values
    actor.first_name = actor_fields["first_name"]
    actor.last_name = actor_fields["last_name"]
    actor.gender = actor_fields["gender"]
    actor.country = actor_fields["country"]
    # add to the database and commit
    db.session.commit()
    #return the actor in the response
    return jsonify(actor_schema.dump(actor))

@actors.route("/actors/<int:id>", methods=["DELETE"])
@jwt_required()
#Includes the id parameter
def actors_delete(id):
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
    stmt = db.select(Actor).filter_by(id=id)
    actor = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not actor:
        return abort(400, description= "actor entry doesn't exist")
    #Delete the card from the database and commit
    db.session.delete(actor)
    db.session.commit()
    #return the actor in the response
    return jsonify(actor_schema.dump(actor))

@actors.route("/search", methods=["GET"])
def search_actors():
    # create an empty list in case the query string is not valid
    actors_list = []

    if request.args.get('country'):
        stmt = db.select(Actor).filter_by(country= request.args.get('country'))
        actors_list = db.session.scalars(stmt)
    elif request.args.get('gender'):
        stmt = db.select(Actor).filter_by(gender= request.args.get('gender'))
        actors_list = db.session.scalars(stmt)

    result = actors_schema.dump(actors_list)
    # return the data in JSON format
    return jsonify(result)