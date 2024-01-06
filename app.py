# app.py
import streamlit as st
import pandas as pd

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
csv_path = 'data/All-Indian-Names.csv'
all_names_df = pd.read_csv(csv_path)

# Streamlit app
def main():
    st.title("IndianSpell Checker")
    st.text("With Love by @prasanna_muppidwar")
    # Form for user input
    input_name = st.text_input("Enter Name:")
    add_button = st.button("Add Name")

    if add_button:
        # Spell check the input name and get suggestions
        suggestions = suggest_corrections(input_name, all_names_df['name'])

        # Display suggestions
        st.write("Suggestions:", ", ".join(suggestions))

if __name__ == '__main__':
    main()
