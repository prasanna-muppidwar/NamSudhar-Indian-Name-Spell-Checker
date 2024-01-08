from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Function to calculate Levenshtein distance
def levenshtein_distance(str1, str2):
    if len(str1) < len(str2):
        return levenshtein_distance(str2, str1)

    if len(str2) == 0:
        return len(str1)

    previous_row = range(len(str2) + 1)
    for i, char1 in enumerate(str1):
        current_row = [i + 1]
        for j, char2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (char1 != char2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Function to suggest corrections
def suggest_corrections(incorrect_name, correct_names_column):
    suggestions = sorted(correct_names_column, key=lambda x: levenshtein_distance(incorrect_name, str(x)))
    return suggestions[:3]

# Load the CSV data
csv_path = 'All-Indian-Names.csv'
all_names_df = pd.read_csv(csv_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_input():
    input_name = request.form.get('input_name')
    suggestions = suggest_corrections(input_name, all_names_df['name'])
    return render_template('index.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
