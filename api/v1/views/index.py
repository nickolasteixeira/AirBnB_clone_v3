from api.v1.views import app_views


@app_views.route('/status')
def return_status():
    return jsonify({"status": "OK"})
