from app import app   # import the actual app object
from flask import jsonify, request

from application.models import Student, Company, Drive

@app.route("/")
def index():
    return "<h1>Welcome to the Placement Portal API</h1>" \
            "The Server is Running!" \
            "<p>Use /api/ for API endpoints.</p>" \
            "<p>Example: <a href='/api/health'>/api/health</a></p>" \
            "<p>Documentation: <a href='/api/docs'>/api/docs</a></p>" \

@app.route("/api/")
def home():
    return jsonify({
        "message": "Placement Portal API running"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "status": "OK"
    })


@app.route("/viva", methods=["GET"])
def viva():
    companies = Company.query.all()

    result = [
        {
            "id": c.id,
            "name": c.name,
            "username": c.username,
            "email": c.email,
            "industry": c.industry
        } for c in companies
    ] 

    return jsonify(result)

@app.route("/viva/<int:company_id>", methods=['GET'])
def viva_id(company_id):

    c = Company.query.get(company_id)

    if not c:
        return jsonify({'error':'No company found'}), 404


    result = [{
        "id": c.id,
        "username": c.username,
        "name": c.name,
        "email": c.email,
        "description": c.description,
        "industry": c.industry,
        "logo": c.logo
    }]

    return jsonify(result)

from datetime import datetime
@app.route("/api/viva/drives", methods=['GET'])
def get_drives():

    date_str = request.args.get('date')
    today = datetime.now()

    if not date_str:
        return jsonify ({"error": "Date is Required"}), 400
    
    try:
        
        input_date = datetime.fromisoformat(date_str)

    except:
        return jsonify ({"error":"Invalid date format"}), 400
    
    drives = Drive.query.filter(Drive.deadline > input_date).all()

    result = [{
        "Title": d.title,
        "Company": d.company.name,
        "Deadline": d.deadline,
        "Description": d.description
    } for d in drives
    ]

    return jsonify (result)


from datetime import date, timedelta
@app.route('/viva/msg', methods=['GET'])
def msg():

    today = date.today()

    msgDate = today + timedelta(days=5)

    msg = ("Hey This is a message from Flask")

    return jsonify ({
                        "date": msgDate,
                        "message": msg
                     })

@app.route('/api/sum', methods=['GET'])
def sum():

    a = int(request.args.get('a'))
    b = int(request.args.get('b'))

    sum = a + b

    return jsonify ({
                        'a': a,
                        'b': b,
                        'sum': sum
                    })

from application.tasks import get_recent_appointments
@app.route('/applications/recent', methods=['GET'])
def recent_appointments():
    task = get_recent_appointments.delay()

    return jsonify ({"task_id": task.id })


from application.tasks import new_task
@app.route('/task/trigger/1', methods=['GET'])
def task_trigger():
    task = new_task.delay()

    return jsonify({
        "task_id": task.id
    })


from application.tasks import sum
@app.route('/sum', methods=['GET'])

def get_sum():

    a = int(request.args.get('a'))
    b = int(request.args.get('b'))

    task = sum.delay(a,b)

    return jsonify({
        'task_id':task.id,
        'status':'processing'
    })