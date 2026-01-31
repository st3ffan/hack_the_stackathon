from flask import Flask, render_template

app = Flask(__name__)

# Static sample data mimicking the MongoDB structure
SAMPLE_CORPORATIONS = [
    {
        "_id": "sample_1",
        "company": "TechCorp Industries",
        "rank": 1,
        "ticker": "TECH",
        "ir_page": "https://investors.techcorp.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 15, 2025",
            "document_url": "https://techcorp.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_2",
        "company": "Global Finance Ltd",
        "rank": 3,
        "ticker": "GFL",
        "ir_page": "https://investors.globalfinance.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "January 28, 2025",
            "document_url": "https://globalfinance.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_3",
        "company": "Healthcare Solutions Inc",
        "rank": 5,
        "ticker": "HSI",
        "ir_page": "https://investors.healthcaresolutions.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 5, 2025",
            "document_url": "https://healthcaresolutions.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_4",
        "company": "Energy Systems Corp",
        "rank": 2,
        "ticker": "ENR",
        "ir_page": "https://investors.energysystems.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 20, 2025",
            "document_url": "https://energysystems.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_5",
        "company": "Retail Dynamics LLC",
        "rank": 8,
        "ticker": "RTL",
        "ir_page": "https://investors.retaildynamics.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "March 1, 2025",
            "document_url": "https://retaildynamics.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_6",
        "company": "Cloud Services Group",
        "rank": 4,
        "ticker": "CLD",
        "ir_page": "https://investors.cloudservices.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 10, 2025",
            "document_url": "https://cloudservices.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_7",
        "company": "Manufacturing Pro Inc",
        "rank": 7,
        "ticker": "MFG",
        "ir_page": "https://investors.manufacturingpro.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "January 22, 2025",
            "document_url": "https://manufacturingpro.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_8",
        "company": "Transportation Network Co",
        "rank": 9,
        "ticker": "TRN",
        "ir_page": "https://investors.transportation.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 25, 2025",
            "document_url": "https://transportation.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_9",
        "company": "Biotechnology Ventures",
        "rank": 6,
        "ticker": "BIO",
        "ir_page": "https://investors.biotechnology.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "February 18, 2025",
            "document_url": "https://biotechnology.com/earnings/Q4_2024.pdf",
        },
    },
    {
        "_id": "sample_10",
        "company": "Real Estate Holdings",
        "rank": 10,
        "ticker": "REH",
        "ir_page": "https://investors.realestate.com",
        "latest_earnings": {
            "period": "Q4 2024 (Full Year 2024)",
            "date": "March 5, 2025",
            "document_url": "https://realestate.com/earnings/Q4_2024.pdf",
        },
    },
]


def get_sample_corporations():
    """Return static sample corporation data"""
    return SAMPLE_CORPORATIONS


@app.route("/")
def index():
    corporations = get_sample_corporations()
    return render_template("index.html", corporations=corporations)


if __name__ == "__main__":
    print("Starting sample Flask app with static data...")
    print("This demonstrates the UI without requiring MongoDB connection")
    app.run(host="0.0.0.0", port=8080, debug=True)
