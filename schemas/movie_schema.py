from main import ma

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "genre", "length", "year")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)