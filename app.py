from flask import Flask, render_template, request
import joblib
import numpy as np

# Create Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load("flood_prediction_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get values from HTML form
        temp = float(request.form["Temp"])
        humidity = float(request.form["Humidity"])
        cloud_cover = float(request.form["CloudCover"])
        annual = float(request.form["Annual"])
        jan_feb = float(request.form["JanFeb"])
        mar_may = float(request.form["MarMay"])
        jun_sep = float(request.form["JunSep"])
        oct_dec = float(request.form["OctDec"])
        avgjune = float(request.form["AvgJune"])
        sub = float(request.form["Sub"])

        # Arrange input in the same order as training
        input_data = np.array([[
            temp,
            humidity,
            cloud_cover,
            annual,
            jan_feb,
            mar_may,
            jun_sep,
            oct_dec,
            avgjune,
            sub
        ]])

        # Prediction
        prediction = model.predict(input_data)

        if prediction[0] == 1:
            result = "⚠️ Flood Likely"
        else:
            result = "✅ No Flood"

        return render_template("index.html", prediction_text=result)

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run(debug=True)