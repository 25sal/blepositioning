from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import text
from database import db
from models import get_position
 
# Creating Flask App
app = Flask(__name__)
# Database Name
db_name = 'info.db'
 
# Configuring SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
 
# Suppresses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialising SQLAlchemy with Flask App
db.init_app(app)




@app.route('/')
def index():
   return render_template('index.html')


#this method will return the last updated positions of the one individual or object
@app.route('/api-service/position')
def position():
    #get the id from the request
    id = request.args.get('id')
    result = get_position(id)
    
    if result is None:
        return jsonify({'error': 'Data not found'})
    else:
        # return the result as a json
        return jsonify({'id': result.id, 'x': result.x, 'y': result.y, 'z': result.z, 'sqltime': result.sqltime})

#this method will get the updated positions of all the objects and individuals after a certain time
@app.route('/api-service/updates', methods=['GET'])
def updates():
    pass

#this method will update the position of an individual or object
@app.route('/api-service/update', methods=['POST'])
def updates():
    pass

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from models import Positions
    create_db()
    app.run(host="0.0.0.0", debug=True)
        