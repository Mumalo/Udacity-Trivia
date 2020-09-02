import os
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, abort, jsonify, request, json
from flask_cors import CORS
import random
from models import setup_db, Question, Category
import sys
QUESTIONS_PER_PAGE = 10


def paginate(questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS,POST,PATCH,DELETE')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route("/categories", methods=["GET"])
    def list_categories():
        categories = list(map(Category.format, Category.query.all()))
        return jsonify({"success": True, "categories": categories})

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route("/questions", methods=["GET"])
    def list_questions():
        questions = Question.query.order_by(Question.id).all()
        paginated_result = paginate(questions)

        """when client requests above valid page"""
        if len(paginated_result) == 0:
            abort(404)
        categories = list(map(Category.format, Category.query.all()))
        return jsonify({
            "success": True,
            "questions": paginated_result,
            "total_questions": len(Question.query.all()),
            "categories": categories,
            "current_category":  None
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID.     
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if not question:
            abort(404)
            return

        question.delete()
        remaining = Question.query.order_by(Question.id).all()
        paginated = paginate(remaining)
        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': paginated,
            'total_questions': len(Question.query.all())
        })


    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()
        try:
            question_text = body["question"]
            answer = body["answer"]
            category = body["category"]
            difficulty = body["difficulty"]
            new_question = Question(question=question_text, answer=answer, category=str(category), difficulty=difficulty)
            new_question.insert()
            updated_questions = Question.query.order_by(Question.id).all()
            paginated_list = paginate(updated_questions)
            return jsonify({
                "success": True,
                "created": new_question.id,
                "questions": paginated_list,
                "total_questions": len(updated_questions)
            })
        except:
            abort(400)

    '''
    @T    ODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question.     
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        try:
            search_data = request.get_json()
            if search_data is not None:
                continue_search = True if 'searchTerm' in search_data else False
                if continue_search:
                    search_term = search_data["searchTerm"]
                    questions_found = Question.query.filter(
                        Question.question.ilike("%{}%".format(search_term))
                    ).all()
                    paginated_list = paginate(questions_found)
                    if len(paginated_list) > 0:
                        return jsonify({
                            "success": True,
                            "questions": paginated_list,
                            "total_questions": len(questions_found),
                        })
                    else:
                        return jsonify({
                            "success": True,
                            "questions": None,
                            "total_questions": 0
                        })
                else:
                    abort(422)
                    return
            abort(422)
        except SQLAlchemyError:
            print(sys.exc_info())
            abort(400)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category.     
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route("/categories/<int:category_id>/questions")
    def get_question_by_category(category_id):
        try:
            categories = list(map(Category.format, Category.query.all()))
            category = Category.query.get(category_id)
            questions = Question.query.filter_by(
                category=str(category_id)).all()
            paginated = paginate(questions)
            if len(paginated) > 0:
                result = {
                    "success": True,
                    "questions": paginated,
                    "total_questions": len(questions),
                    "categories": categories,
                    "current_category": category.format(),
                }
                return jsonify(result)
            abort(404)
        except SQLAlchemyError:
            print(sys.exc_info())
            abort(400)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions.     
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route("/quizzes", methods=["POST"])
    def questions_for_quiz():
        search_data = request.get_json()
        if search_data:
            if (('quiz_category' in search_data
                 and 'id' in search_data['quiz_category'])
                    and 'previous_questions' in search_data):
                questions_query = Question.query.filter_by(
                    category=str(search_data['quiz_category']['id'])
                ).filter(
                    Question.id.notin_(search_data["previous_questions"])
                ).all()
                length_of_available_question = len(questions_query)
                if length_of_available_question > 0:
                    result = {
                        "success": True,
                        "question": Question.format(
                            questions_query[random.randrange(
                                0,
                                length_of_available_question
                            )]
                        )
                    }
                    return jsonify(result)
                else:
                    result = {
                        "success": True,
                        "question": None
                    }
                    return jsonify(result)
            abort(400)
        abort(400)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def interbal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "bad request"
        }), 500

    return app
