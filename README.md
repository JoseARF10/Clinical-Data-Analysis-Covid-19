# COVID-19 Mexico Data Analysis Tool

A command-line tool to analyze COVID-19 patient data from Mexico. It generates charts comparing medical conditions against patient mortality, and can export cleaned data to a SQLite database.

---

## Requirements

- Python 3.8 or higher
- pip

Install the required libraries by running:

```
pip install pandas matplotlib
```

---

## Setup

1. Place the script file and your `Covid_Data.csv` file in the same folder.
2. Open a terminal and navigate to that folder.

---

## Running the Program

```
python script.py
```

The program will first ask you for the name of the CSV file:

```
Type the name of the file (with .csv extension): Covid_Data.csv
```

If the file is not found, it will ask again until a valid file is provided.

---

## Menu Options

Once the file is loaded, a menu will appear. Type one of the following commands and press Enter:

**diabetes**
Shows a bar chart comparing death rates between patients with and without diabetes.

**obesity**
Shows a bar chart comparing death rates between patients with and without obesity.

**obesity diabetes**
Shows a bar chart comparing death rates between patients who have both obesity and diabetes versus those who do not.

**data-cleaning**
Cleans the dataset and saves it to a SQLite database file called `patients.db`. Numeric codes are replaced with readable labels and dates are formatted to YYYY-MM-DD.

**exit**
Closes the program.

---

## Output Files

| File | Description |
|---|---|
| `patients.db` | SQLite database created by the data-cleaning command |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| File not found error | Make sure the CSV file is in the same folder as the script |
| ModuleNotFoundError | Run `pip install pandas matplotlib` in your terminal |
| Chart does not appear | Make sure your environment supports graphical output |
| Command not recognized | Type the command exactly as shown in the menu, in lowercase |