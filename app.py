
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from database import (
    init_db,
    save_prediction,
    get_prediction_history,
    get_dashboard_stats
)
from model.predict import predict_crop

app = Flask(__name__)
app.secret_key = "opticrop-premium-secret-key"

# Initialize database
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    stats = get_dashboard_stats()
    history = get_prediction_history(10)

    return render_template(
        "dashboard.html",
        stats=stats,
        history=history
    )


@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    result = None

    if request.method == "POST":
        try:
            data = {
                "nitrogen": request.form.get("nitrogen"),
                "phosphorus": request.form.get("phosphorus"),
                "potassium": request.form.get("potassium"),
                "temperature": request.form.get("temperature"),
                "humidity": request.form.get("humidity"),
                "ph": request.form.get("ph"),
                "rainfall": request.form.get("rainfall")
            }

            result = predict_crop(data)

            save_prediction(
                data,
                result["crop"],
                result["confidence"]
            )

            flash("Crop recommendation generated successfully!", "success")

        except (ValueError, FileNotFoundError) as error:
            flash(str(error), "error")

        except Exception as error:
            print("Prediction error:", error)
            flash("Something went wrong. Please check your inputs and model.", "error")

    return render_template(
        "recommend.html",
        result=result
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("base.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
