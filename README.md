# Kynthera Funds MVP

Kynthera Funds is a prototype cash-flow intelligence tool for SME lending.

The MVP allows a lender to upload bank transaction data, calculate cash-flow indicators, generate an explainable credit confidence score, and view a lending recommendation.

## Features

- CSV upload for SME transaction data
- Data validation and cleaning
- Cash-flow metrics
- Rule-based explainable credit score
- Lending recommendation: approve, manual review, or reject
- Driver breakdown explaining the score
- Simple Streamlit dashboard

## Required CSV Format

The uploaded CSV should contain:

```text
date, description, amount, balance, category
```

A sample file is included in `data/sample_transactions.csv`.

How to Run the App

Follow the steps below to run the Kynthera Funds MVP locally.

1. Clone or download the repository

First, download the GitHub repository to your computer or clone it using Git:

git clone https://github.com/your-username/Kynthera_Funds.git

Then move into the project folder:

cd Kynthera_Funds

2. Check the project structure

Make sure the project folder contains the following files and folders:

Kynthera_Funds/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_transactions.csv
└── src/
├── init.py
├── data_processing.py
└── scoring.py

3. Install the required packages in your terminal

Install the required Python packages using:

pip install -r requirements.txt

This installs the packages needed to run the app, including Streamlit, Pandas, and NumPy.

4. Run the Streamlit app

Start the app with the following command:

streamlit run app.py

After running this command, Streamlit will open the app in your browser. If it does not open automatically, copy the local URL shown in the terminal, usually:

http://localhost:8501

and paste it into your browser.

5. Upload the sample transaction file

Once the app is open, upload the sample transaction file located in:

data/sample_transactions.csv

The app will then process the transaction data and generate:

* a credit confidence score;
* an approval recommendation;
* a suggested maximum loan amount;
* key cash-flow signals;
* explainable score drivers;
* a monthly cash-flow overview;
* a transparent explanation of how the score is calculated.

6. Stop the app

To stop the app, go back to the terminal and press:

Control + C

Notes

This MVP uses a CSV upload to simulate transaction data access. In a production version, this input would be replaced by PSD2/open banking API connections.

The current credit score is rule-based and explainable by design. In a later version, the model could be validated and improved using real repayment and default outcome data.

## MVP Scope

The current MVP uses CSV uploads to simulate transaction data access. In production, this input would be replaced with PSD2/open banking API connections.

The scoring model is intentionally rule-based for transparency. In later versions, it could be validated and improved using real repayment and default outcome data.

## Limitations

- No live PSD2 API integration yet
- No real customer authentication
- No production-grade encryption or access control
- Rule-based scoring is not yet validated on real loan outcomes
- Not intended for real lending decisions
