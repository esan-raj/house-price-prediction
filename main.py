from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('final_dataset.csv')
pipe = pickle.load(open("Random_forest.pkl", 'rb'))

@app.route('/')
def index():
    bedrooms = sorted(data['beds'].unique())
    bathrooms = sorted(data['baths'].unique())
    sizes = sorted(data['size'].unique())
    city_codes = sorted(data['city_codes'].unique())

    return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, city_codes=city_codes)


@app.route('/predict', methods=['POST'])
def predict():
    bedrooms = request.form.get('beds')
    bathrooms = request.form.get('baths')
    size = request.form.get('size')
    city_codes = request.form.get('city_code')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[bedrooms, bathrooms, size, city_codes]],
                               columns=['beds', 'baths', 'size', 'city_codes'])

    print("Input Data:")
    print(input_data)

    # **Choose a strategy for handling unknown categories:**
    # Option 1: Impute with Most Frequent Category (modify as needed)
    for column in input_data.columns:
        unknown_categories = set(input_data[column]) - set(data[column].unique())
        if unknown_categories:
            most_frequent = data[column].mode()[0]
            input_data[column] = input_data[column].replace(unknown_categories, most_frequent)

    # Option 2: Impute with Mean/Median (modify as needed)
    # for column in input_data.columns:
    #     if column in data.select_dtypes(include=['int64', 'float64']):  # Check for numerical columns
    #         unknown_categories = set(input_data[column]) - set(data[column].unique())
    #         if unknown_categories:
    #             mean_value = data[column].mean()  # Replace with median if desired
    #             input_data[column] = input_data[column].replace(unknown_categories, mean_value)

    # Option 3: Separate Category for "Unknown" (modify as needed)
    #  - Add "unknown" category to all categorical features before training
    #  - Modify model training to handle the new category

    # Option 4: Error Message (uncomment if preferred)
    # unknown_categories = False
    # for column in input_data.columns:
    #     unknown_categories |= any(cat in set(input_data[column]) for cat in set(input_data[column]) - set(data[column].unique()))
    #
    # if unknown_categories:
    #     return "Error: Encountered unknown categories in input data. Please select valid options."

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction = pipe.predict(input_data)[0]
    print(prediction)

    return str(prediction)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
