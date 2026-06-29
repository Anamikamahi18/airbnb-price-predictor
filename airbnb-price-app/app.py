from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    host_id = int(request.form["Host Id"])
    host_since = pd.to_datetime(request.form["Host Since"]).toordinal()
    neighbourhood = request.form["Neighbourhood"]
    property_type = request.form["Property Type"]
    review_scores_rating_bin = float(request.form["Review Scores Rating (bin)"])
    room_type = request.form["Room Type"]
    zipcode = float(request.form["Zipcode"])
    beds = float(request.form["Beds"])
    number_of_records = int(request.form["Number of Records"])
    number_of_reviews = int(request.form["Number Of Reviews"])
    review_scores_rating = float(request.form["Review Scores Rating"])

    input_data = pd.DataFrame([{
        "Host Id": host_id,
        "Host Since": host_since,
        "Neighbourhood": neighbourhood,
        "Property Type": property_type,
        "Review Scores Rating (bin)": review_scores_rating_bin,
        "Room Type": room_type,
        "Zipcode": zipcode,
        "Beds": beds,
        "Number of Records": number_of_records,
        "Number Of Reviews": number_of_reviews,
        "Review Scores Rating": review_scores_rating
    }])

    prediction = model.predict(input_data)[0]

    # Step 7: price range
    lower_price = round(prediction - 79, 2)
    upper_price = round(prediction + 79, 2)

    return render_template(
        "index.html",
        prediction_text=f"Estimated price range: ${lower_price} to ${upper_price}"
    )

if __name__ == "__main__":
    app.run(debug=True)