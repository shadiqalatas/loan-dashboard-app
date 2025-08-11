# **Luxury Loan Portfolio Dashboard**

A **Plotly Dash** web app that visualizes key metrics for luxury loans, based on LuxuryLoanPortfolio.csv data

---

## **Features**
1. **Loan Purpose Analysis**  
   - Compares interest rates and loan durations across different purposes (boats, planes, commercial property, home, and investment property).  
   - Identifies high risk loan purpose

2. **Loan-to-Value (LTV) Distribution**  
   - Histogram of LTV ratios stacked by purpose.  
   - Highlights risk thresholds (80% and 90% LTV).

3. **Loan Performance Trends**  
   - Time-series analysis of Total Funded Amount and Total Borrowers.  
   - Tracks performance of the company.

---

## **Prerequisites**
- Docker ([Install Guide](https://docs.docker.com/get-docker/))
- Python 3.9+ 

---

## **Quick Start**
### **1. Run with Docker**
```bash
# Pull the image from Docker Hub
docker pull alatasshadiq/luxury-loan-dashboard-app:latest

# Run the container
docker run -p 8050:8050 alatasshadiq/luxury-loan-dashboard-app
```
Access the app at: http://localhost:8050

---

## **Chart Details**
### **1. Loan Purpose Analysis**
- **X-axis**: Average Interest Rate (%).  
- **Y-axis**: Average Loan Duration (Years).
- **Bubble Size**: Total Funded Amount.
- **Bubble Color** : Purpose.  
- **Insight**: Compare risk-return profiles across purpose of the loan.

### **2. LTV Ratio Distribution**
- **Bar Color**: Purpose.
- **Thresholds**:  
  - 🟠 Orange line: 80% LTV (caution zone).  
  - 🔴 Red line: 90% LTV (high risk).  
- **Insight**: Identify risky loans that have high LTV Ratio.

### **3. Loan Performance Trends**
- **X-axis**: Time (months/quarters).  
- **Y-axis**: Total Funded Amount (left) and Total Borrowers (right).  
- **Insight**: Monitor performance of the company.

---

## **Technical Stack**
- **Backend**: Python (Pandas, Plotly, Dash).  
- **Frontend**: Plotly Dash.  
- **Deployment**: Docker.
