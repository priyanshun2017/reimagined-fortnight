from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, MovieRating
from utils import search_movie, get_movie_details

auth = Blueprint('auth', __name__)
movie = Blueprint('movie', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401


@movie.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search_movie(query)
    return jsonify(results)


@movie.route('/rate', methods=['POST'])
@jwt_required()
def rate_movie():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()
    new_rating = MovieRating(user_id=user.id, movie_id=data['movie_id'], rating=data['rating'])
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Rating submitted'})


@movie.route('/ratings', methods=['GET'])
@jwt_required()
def get_ratings():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()
    ratings = MovieRating.query.filter_by(user_id=user.id).all()
    output = []
    for rating in ratings:
        movie_details = get_movie_details(rating.movie_id)
        output.append({
            'movie': movie_details['title'],
            'rating': rating.rating
        })
    return jsonify(output)
