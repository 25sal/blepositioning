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



'''
def create_db():
    if os.path.isfile(dbname):
        os.remove(dbname)
    
    conn = sqlite3.connect(dbname)
    query = 'CREATE TABLE positions ' \
            '(id	INTEGER NOT NULL, x NOT NULL, y	REAL NOT NULL, ' \
            'z	REAL NOT NULL, ' \
            'postime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, '   \
            'PRIMARY KEY(id AUTOINCREMENT))'
    
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
'''



@app.route('/')
def index():
   return render_template('index.html')

@app.route('/api-service/position')
def position():
    #get the id from the request
    id = request.args.get('id')
    result = get_position(id)
    
    #t = text('SELECT id, x,y,z,sqltime FROM positions where id = :val1 ORDER BY sqltime DESC LIMIT 1')
    #result = db.session.execute(t, {'val1': id}).fetchall()
    if result is None:
        return jsonify({'error': 'Data not found'})
    else:
        # return the result as a json
        return jsonify({'id': result.id, 'x': result.x, 'y': result.y, 'z': result.z, 'sqltime': result.sqltime})



""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from models import Positions
    create_db()
    app.run(debug=True)
        