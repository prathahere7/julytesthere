from flask import Flask, request, jsonify
from api.helpers import unsafe_query

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q')
    results = unsafe_query(query)  # SQL injection risk
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
