import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_pharma_data(num_rows=2500):
    regions = ['North', 'South', 'East', 'West', 'Midwest']
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    
    # Real-world drug data
    drugs = {
        'Cardiovascular': ['Eliquis', 'Entresto', 'Xarelto', 'Lipitor'],
        'Oncology': ['Keytruda', 'Opdivo', 'Revlimid', 'Imbruvica'],
        'Immunology': ['Humira', 'Stelara', 'Cosentyx', 'Enbrel'],
        'Neurology': ['Ocrevus', 'Biktarvy', 'Tysabri', 'Spinraza'],
        'Respiratory': ['Symbicort', 'Spiriva', 'Fasenra', 'Advair']
    }
    drug_categories = list(drugs.keys())
    
    # Real-world manufacturers
    manufacturers = ['Pfizer', 'Johnson & Johnson', 'Novartis', 'Merck', 'AbbVie', 'AstraZeneca', 'Roche']
    
    # Real-world hospital networks
    hospitals = [
        'Mayo Clinic', 'Cleveland Clinic', 'Tenet Healthcare', 
        'Kaiser Permanente', 'HCA Healthcare', 'Mount Sinai', 
        'Mass General Brigham', 'Johns Hopkins Hospital',
        'UCLA Medical Center', 'Stanford Health Care'
    ]
    reps = ['Michael S.', 'Sarah M.', 'David L.', 'Emma B.', 'James T.', 'Olivia K.', 'William R.']
    
    data = []
    start_date = datetime(2022, 1, 1) # 3 years of data
    
    for _ in range(num_rows):
        days_offset = random.randint(0, 365 * 3) 
        date = start_date + timedelta(days=days_offset)
        
        region = random.choice(regions)
        
        # Season based on month
        month = date.month
        if month in [3, 4, 5]: season = 'Spring'
        elif month in [6, 7, 8]: season = 'Summer'
        elif month in [9, 10, 11]: season = 'Autumn'
        else: season = 'Winter'
            
        category = random.choice(drug_categories)
        drug_name = random.choice(drugs[category])
        manufacturer = random.choice(manufacturers)
        
        hospital = random.choice(hospitals)
        rep = random.choice(reps)
        
        # Base stats logic
        base_price = random.uniform(500, 5000)
        units_sold = random.randint(10, 500)
        
        # Inject some seasonal/category logic for interesting queries
        if season == 'Winter' and category == 'Respiratory':
            units_sold = int(units_sold * 1.8) # High respiratory sales in winter
        if region == 'South' and category == 'Cardiovascular':
            units_sold = int(units_sold * 1.3)
            
        gross_revenue = base_price * units_sold
        discount_perc = random.uniform(0.05, 0.25)
        net_revenue = gross_revenue * (1 - discount_perc)
        
        # NEW STRATEGIC COLUMNS
        operating_cost = net_revenue * random.uniform(0.4, 0.7)
        net_profit = net_revenue - operating_cost
        profit_margin = (net_profit / net_revenue) if net_revenue > 0 else 0
        
        data.append({
            'Transaction_ID': f"TXN_{random.randint(100000, 999999)}",
            'Date': date.strftime('%Y-%m-%d'),
            'Season': season,
            'Region': region,
            'Hospital_Network': hospital,
            'Sales_Rep': rep,
            'Manufacturer': manufacturer,
            'Drug_Category': category,
            'Drug_Name': drug_name,
            'Units_Sold': units_sold,
            'Unit_Price_USD': round(base_price, 2),
            'Discount_Applied_Perc': round(discount_perc * 100, 1),
            'Gross_Revenue_USD': round(gross_revenue, 2),
            'Net_Revenue_USD': round(net_revenue, 2),
            'Net_Profit_USD': round(net_profit, 2),
            'Profit_Margin_Perc': round(profit_margin * 100, 1),
            'Order_Priority': random.choice(['Critical', 'High', 'Medium', 'Low']),
            'Insurance_Coverage_Perc': random.choice([50, 80, 100]),
            'Approval_Status': random.choice(['Approved', 'Pending Review', 'Internal Audit']),
            'Patient_Feedback_Score': round(random.uniform(3.5, 5.0), 1)
        })
        
    df = pd.DataFrame(data)
    df = df.sort_values(by='Date')
    df.to_csv('/Users/varunsaini/Desktop/RabbittAI_Varun/talking-rabbitt-mvp/sample_data/pharma_sales_data.csv', index=False)
    print(f"Generated pharma_sales_data.csv with {len(df.columns)} columns and {len(df)} rows!")

if __name__ == "__main__":
    generate_pharma_data()
