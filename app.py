from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load and prepare the dataset
data = pd.read_csv("blood_donation_data.csv")
feature_columns = ['Recency (months)', 'Frequency (times)', 'Monetary (c.c. blood)', 'Time (months)']
target_column = 'whether he/she donated blood in March 2007'
X = data[feature_columns]
y = data[target_column]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/donate')
def donate():
    return render_template('donate.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/seek')
def seek():
    return render_template('seek.html')

@app.route('/predict', methods=['POST'])
def predict():
    recency = int(request.form['recency'])
    frequency = int(request.form['frequency'])
    monetary = int(request.form['monetary'])
    time = int(request.form['time'])
    
    input_data = pd.DataFrame([[recency, frequency, monetary, time]], columns=feature_columns)
    prediction = model.predict(input_data)[0]
    
    if prediction == 1:
        average_interval = time / frequency if frequency > 0 else 0
        next_donation = recency + average_interval
        return jsonify({
            'prediction': 'Will donate',
            'next_donation': round(next_donation, 2)
        })
    else:
        return jsonify({
            'prediction': 'Will not donate'
        })

if __name__ == '__main__':
    app.run(debug=True)
