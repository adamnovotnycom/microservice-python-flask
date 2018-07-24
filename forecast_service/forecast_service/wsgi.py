from forecast_service.app import app as application
from forecast_service.home.views import home_view
application.register_blueprint(home_view)
from forecast_service.forecast.views import forecast_view
application.register_blueprint(forecast_view)



def flask_default():
    # local Flask server. Development only
    application.run(debug=True, host="0.0.0.0", port=5002)

if __name__ == "__main__":
    flask_default()