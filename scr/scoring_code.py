
import pandas as pd
import pymysql

def scoring_metric():
    # Database connection 
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'esg_database',
        'charset': 'utf8mb4'
    }

    # Connect to the MySQL database
    conn = pymysql.connect(**db_config)

    # Query to fetch the most recent timestamp from Structured_data
    query_latest_time = "SELECT MAX(time) AS latest_time FROM Structured_data;"
    latest_time = pd.read_sql(query_latest_time, conn).iloc[0, 0]

    # Query to fetch data with the latest timestamp and include report_id and report_year from esg_report
    query = """
   SELECT sd.*, er.report_id, er.report_year
FROM Structured_data AS sd
JOIN (
    SELECT firm_name, MAX(report_id) AS report_id
    FROM esg_report
    GROUP BY firm_name
) AS max_report
ON sd.company_name = max_report.firm_name
JOIN esg_report AS er
ON max_report.report_id = er.report_id
WHERE sd.time = %s;

    """
    company_data = pd.read_sql(query, conn, params=(latest_time,))


    # Close the connection
    conn.close()

    industry_avg_data = pd.DataFrame({
        'categories': ['Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Environment', 'Governance', 'Governance', 'Governance', 'Governance', 'Governance', 'Governance', 'Governance', 'Governance', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social'],
        'metric': ['Protected_or_restored_habitats', 'Absolute_emissions', 'Emission_intensities', 'Total_energy_consumption', 'Energy_consumption_intensity', 
                'Green_financing_projects', 'Green_certified_buildings', 'Waste_generated', 'Water_consumption', 'Water_intensity', 
                'External_audit_conducted', 'Board_independence', 'Women_in_the_management_team', 'Women_on_the_board', 'Anti_corruption_disclosures', 
                'Anti_corruption_training', 'Assurance_of_sustainability_report', 'List_of_relevant_certifications', 'Availability_of_Healthcare_Resources', 
                'Community_Health_Program', 'Percentage_of_employees_covered_by_health_insurance', 'Company_donated', 'Philanthropic_initiatives', 'Controversial_Sourcing', 
                'Consumer_rights_protection', 'Average_training_hours_per_employee', 'Current_employees_by_age_groups', 'Current_employees_by_gender', 'Employee_satisfaction_rate', 
                'New_hires_by_gender', 'New_hires_by_age', 'Total_number_of_employees', 'Total_turnover', 'Turnover_by_gender', 
                'Turnover_by_age', 'Fatalities', 'High_consequence_injuries', 'Work_related_injuries', 'Community_nutrition_programs'],
        'weight': [1.34128, 4.61997, 3.20417, 4.47094, 2.98063, 3.20417, 5.81222, 3.27869, 3.12966, 1.49031, 0.74516, 0.74516, 3.8003, 0.07452, 2.30999, 0.81967, 6.03577, 6.03577, 1.93741, 1.93741, 1.63934, 0.29806, 0.52161, 0.52161, 1.63934, 3.42772, 4.39642, 5.14158, 1.86289, 1.80759, 1.54561, 0.74516, 4.24739, 2.28961, 1.95778, 3.42772, 2.23547, 4.09836, 0.22355],
        'avg_value': [None, None, 0.119476363636364, None ,1.95727727272727, None, None, 338.99875, None, 1.83794285714286, None,60 ,42.34 ,28.68, None, None, None, None, None, None, 100, 466528.25, None, None, None, 26.808, 17.85, 57.41, 80, 53.53, 12.85, None, 28.76, 65.42, 16.28, 0, 0, 4.7, None]
    })

    def calculate_score(company_value, industry_avg_value, weight, score_type):
        if pd.isna(company_value):
            return 0

        if score_type == 'disclosure':
            return 100
        if score_type == 'lower_is_better':
            diff = company_value - industry_avg_value
            if diff < -0.5 * industry_avg_value:
                return 100
            elif diff < -0.2 * industry_avg_value:
                return 75
            elif abs(diff) <= 0.2 * industry_avg_value:
                return 50
            elif diff < 0.5 * industry_avg_value:
                return 25
            else:
                return 0

        if score_type == 'higher_is_better':
            diff = company_value - industry_avg_value
            if diff < -0.5 * industry_avg_value:
                return 0
            elif diff < -0.2 * industry_avg_value:
                return 25
            elif abs(diff) <= 0.2 * industry_avg_value:
                return 50
            elif diff < 0.5 * industry_avg_value:
                return 75
            else:
                return 100

        if score_type == 'closest_to_average':
            diff = company_value - industry_avg_value
            if abs(diff) <= 0.2 * industry_avg_value:
                return 100
            elif diff < -0.5 * industry_avg_value or diff > 0.5 * industry_avg_value:
                return 0
            else:
                return 50

        if score_type == 'turnover_level':
            if 10 <= company_value <= 20:
                return 100
            elif 0 <= company_value < 10 or 20 < company_value <= 30:
                return 50
            else:
                return 0
        elif score_type == 'adverse_events':
            return 100 if company_value == 0 else 0
        elif score_type == 'Work_related_injuries':
            if company_value == 0:
                return 100
            elif 1 <= company_value <= 2:
                return 50
            else:
                return 0

    # Function to calculate the rating based on the total score
    def calculate_rating(score):
        if 85.72 <= score <= 100:
            return 'AAA'
        elif 71.44 <= score < 85.72:
            return 'AA'
        elif 57.15 <= score < 71.44:
            return 'A'
        elif 42.87 <= score < 57.15:
            return 'BBB'
        elif 28.58 <= score < 42.86:
            return 'BB'
        elif 14.30 <= score < 28.57:
            return 'B'
        elif 0.0 <= score < 14.29:
            return 'CCC'
        else:
            return 'Unknown'

    def calculate_esg_score(company_data, industry_avg_data):
        total_score = 0
        e_score = 0
        s_score = 0
        g_score = 0
        total_weight = 0

        # Initialize 26 default metrics to 0
        metrics_values = {
            "Emission_intensities": 0,
            "Energy_consumption_intensity": 0,
            "Waste_generated": 0,
            "Water_intensity": 0,
            "Board_independence": 0,
            "Women_in_the_management_team": 0,
            "Women_on_the_board": 0,
            "Percentage_of_employees_covered_by_health_insurance": 0,
            "Company_donated": 0,
            "Average_training_hours_per_employee": 0,
            "Current_employees_by_age_groups": 0,
            "Current_employees_by_gender": 0,
            "Employee_satisfaction_rate": 0,
            "New_hires_by_gender": 0,
            "New_hires_by_age": 0,
            "Total_turnover": 0,
            "Turnover_by_gender": 0,
            "Turnover_by_age": 0,
            "Fatalities": 0,
            "High_consequence_injuries": 0,
            "Work_related_injuries": 0,
        }

        # Get unique company names from the data
        report_id = company_data['report_id'].iloc[0]
        report_year = company_data['report_year'].iloc[0]
        company_name = company_data['company_name'].iloc[0]
        results = []

        for idx, row in company_data.iterrows():
            metric = row['metric']
            company_value = row['value']

            industry_avg_row = industry_avg_data[industry_avg_data['metric'] == metric]
            if industry_avg_row.empty:
                continue

            category = industry_avg_row['categories'].values[0]
            weight = industry_avg_row['weight'].values[0]
            # print(category, weight)
            industry_avg_value = industry_avg_row['avg_value'].values[0]

            # Determine score type based on metric
            score_type = ""
            if metric in ['Protected_or_restored_habitats','Absolute_emissions','Total_energy_consumption','Green_financing_projects','Green_certified_buildings',
                            'Water_consumption','External_audit_conducted','Anti_corruption_disclosures','Anti_corruption_training','Assurance_of_sustainability_report',
                            'List_of_relevant_certifications','Availability_of_Healthcare_Resources','Community_Health_Program','Philanthropic_initiatives','Controversial_Sourcing',
                            'Consumer_rights_protection','Total_number_of_employees','Community_nutrition_programs']:
                score_type = "disclosure"
            elif metric in ["Emission_intensities", "Energy_consumption_intensity", "Waste_generated", "Water_intensity"]:
                score_type = "lower_is_better"
            elif metric in ['Board_independence','Women_in_the_management_team','Women_on_the_board','Percentage_of_employees_covered_by_health_insurance','Company_donated',
                            'Average_training_hours_per_employee','Employee_satisfaction_rate']:
                score_type = "higher_is_better"
            elif metric in ["Total_turnover"]:
                score_type = "turnover_level"
            elif metric in ["Fatalities", "High_consequence_injuries"]:
                score_type = "adverse_events"
            elif metric in ["Work_related_injuries"]:
                score_type = "Work_related_injuries"
            else:
                score_type = "closest_to_average"

            # Calculate score for the metric
            score = calculate_score(company_value, industry_avg_value, weight, score_type)
            total_score += score * weight
            total_weight += weight
            if category == 'Environment':
                e_score += score * weight
            elif category == 'Social':
                s_score += score * weight
            elif category == 'Governance':
                g_score += score * weight

            # Update metrics scores
            if metric in metrics_values:
                metrics_values[metric] = score

        # Calculate final scores
        total_score = total_score / 100
        e_score = e_score / 100
        s_score = s_score / 100
        g_score = g_score / 100

        # Calculate rating
        rating = calculate_rating(total_score)

        # Create a result dictionary for each company
        result = {
            'report_id': report_id,
            'report_year': report_year,
            'company_name': company_name,
            'Total_Score': total_score,
            'Rating': rating,
            'E_Score': e_score,
            'S_Score': s_score,
            'G_Score': g_score
        }
        result.update(metrics_values)

        # Append the result to the list
        results.append(result)

        # Convert to DataFrame and save as Excel
        result_df = pd.DataFrame(results)
        # print(result_df)
        return result_df

    # Load company ESG data

    # Calculate ESG scores for all companies
    company_score_data = calculate_esg_score(company_data, industry_avg_data)

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'esg_database',
        'charset': 'utf8mb4'
    }

    # 连接到 MySQL 数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 将数据插入到 MySQL 中
    for index, row in company_score_data.iterrows():
        insert_query = """
        INSERT INTO ESG_Scores (
            report_id, company_name, Total_Score, Rating, E_Score, S_Score, G_Score, 
            Emission_intensities, Energy_consumption_intensity, Waste_generated, Water_intensity, Board_independence, 
            Women_in_management_team, Women_on_board, 
            Employees_covered_by_health_insurance, 
            Company_donated, 
            Avg_training_hours_per_employee, Employees_above_50, Female_employees, Employee_satisfaction_rate, New_hires_female, New_hires_above_50, 
            Total_turnover, Turnover_female, Turnover_above_50, 
            Fatalities, 
            High_consequence_injuries, 
            Work_related_injuries
        ) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['report_id'],  row['company_name'], row['Total_Score'], row['Rating'], row['E_Score'], row['S_Score'], row['G_Score'],
            row['Emission_intensities'], row['Energy_consumption_intensity'], row['Waste_generated'], row['Water_intensity'], row['Board_independence'], 
            row['Women_in_the_management_team'], row['Women_on_the_board'], 
            row['Percentage_of_employees_covered_by_health_insurance'], 
            row['Company_donated'], 
            row['Average_training_hours_per_employee'], row['Current_employees_by_age_groups'], 
            row['Current_employees_by_gender'], row['Employee_satisfaction_rate'], row['New_hires_by_gender'], row['New_hires_by_age'], 
            row['Total_turnover'], row['Turnover_by_gender'], row['Turnover_by_age'], 
            row['Fatalities'], 
            row['High_consequence_injuries'], 
            row['Work_related_injuries']
        ))

    # 提交更改并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

    print("Data imported successfully!")
scoring_metric()


