from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import pyodbc
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Connection string for SQL Server using Windows Authentication
conn_str = (
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=tcp:tccsqlserverdemo.database.windows.net,1433;'
    'Database=tccsqldbdemo;'
    'UID=jaygokul;'
    'PWD=S3@ttleAzure$Float;'
    'Encrypt=Yes;'
    'TrustServerCertificate=No;'
    'Connection Timeout=30;'
)

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str)
        print("Connection successful")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            print("Network-related or instance-specific error occurred")
        elif sqlstate == '28000':
            print("Invalid authorization specification")
        else:
            print("Error: {ex}")
        raise

def insert_site_visit_notice(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Site_Visit_Notice (
                Regional_Office_Id,
                Facility_Number,
                Site_Visit_Date,
                Regulatory_Violation_Citation_Ind,
                Regulatory_Violation_TypeA_Citation_Ind,
                Regulatory_Violation_TypeB_Citation_Ind,
                LPA_Name,
                LPA_Phone_Number,
                Inserted_DateTime,
                Created_By,
                Create_DateTime,
                Updated_By,
                Update_DateTime,
                Program_Code,
                Code_FT
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CODE1', 'FT1')
        """, data['Regional_Office_Id'], data['Facility_Number'], data['Site_Visit_Date'], 
           data['Regulatory_Violation_Citation_Ind'], data['Regulatory_Violation_TypeA_Citation_Ind'], 
           data['Regulatory_Violation_TypeB_Citation_Ind'], data['LPA_Name'], data['LPA_Phone_Number'],
           datetime.now(), 'Admin', datetime.now(), 'Admin', datetime.now())
        conn.commit()
    except Exception as e:
        print("Error inserting site visit notice: {e}")
        flash("An error occurred while submitting the form. Please try again.", "danger")
    finally:
        conn.close()

def read_site_visit_notice(facility_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Site_Visit_Notice WHERE Facility_Number = ?", facility_number)
        result = cursor.fetchall()
    except Exception as e:
        print("Error reading site visit notice: {e}")
        flash("An error occurred while retrieving notices. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def read_single_site_visit_notice(site_visit_notice_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Site_Visit_Notice WHERE Site_Visit_Notice_Id = ?", site_visit_notice_id)
        result = cursor.fetchone()
    except Exception as e:
        print("Error reading single site visit notice: {e}")
        flash("An error occurred while retrieving the notice. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def update_site_visit_notice(site_visit_notice_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Site_Visit_Notice
            SET
                Regional_Office_Id = ?,
                Facility_Number = ?,
                Site_Visit_Date = ?,
                Regulatory_Violation_Citation_Ind = ?,
                Regulatory_Violation_TypeA_Citation_Ind = ?,
                Regulatory_Violation_TypeB_Citation_Ind = ?,
                LPA_Name = ?,
                LPA_Phone_Number = ?,
                Updated_By = 'Admin',
                Update_DateTime = ?
            WHERE Site_Visit_Notice_Id = ?
        """, data['Regional_Office_Id'], data['Facility_Number'], data['Site_Visit_Date'],
           data['Regulatory_Violation_Citation_Ind'], data['Regulatory_Violation_TypeA_Citation_Ind'],
           data['Regulatory_Violation_TypeB_Citation_Ind'], data['LPA_Name'], data['LPA_Phone_Number'],
           datetime.now(), site_visit_notice_id)
        conn.commit()
    except Exception as e:
        print("Error updating site visit notice: {e}")
        flash("An error occurred while updating the notice. Please try again.", "danger")
    finally:
        conn.close()

def delete_site_visit_notice(site_visit_notice_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Site_Visit_Notice WHERE Site_Visit_Notice_Id = ?", site_visit_notice_id)
        conn.commit()
    except Exception as e:
        print("Error deleting site visit notice: {e}")
        flash("An error occurred while deleting the notice. Please try again.", "danger")
    finally:
        conn.close()

def insert_supportive_detail(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Supportive_Details_Information (
                Facility_Number,
                Facility_Name,
                Public_Or_Confidential,
                Collateral_Visit,
                Visit_Date,
                Visit_Reason_Description,
                LPA_Signed_Ind,
                LPA_Name,
                Signed_DateTime,
                Inserted_DateTime,
                Created_By,
                Create_DateTime,
                Updated_By,
                Update_DateTime,
                LPA_Sign
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data['Facility_Number'], data['Facility_Name'], data['Public_Or_Confidential'], data['Collateral_Visit'], 
           data['Visit_Date'], data['Visit_Reason_Description'], data['LPA_Signed_Ind'], 
           data['LPA_Name'], data['Signed_DateTime'], datetime.now(), 'Admin', datetime.now(), 'Admin', 
           datetime.now(), data['LPA_Sign'])
        conn.commit()
    except Exception as e:
        print("Error inserting supportive detail: {e}")
        flash("An error occurred while submitting the form. Please try again.", "danger")
    finally:
        conn.close()

def read_supportive_details(facility_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Supportive_Details_Information WHERE Facility_Number = ?", facility_number)
        result = cursor.fetchall()
    except Exception as e:
        print("Error reading supportive details: {e}")
        flash("An error occurred while retrieving records. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def read_single_supportive_detail(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("RECORD ID>>>>>>>>>>>>>>",record_id)
        cursor.execute("SELECT * FROM Supportive_Details_Information WHERE Supportive_Details_Information_Id = ?", record_id)
        result = cursor.fetchone()
    except Exception as e:
        print("Error reading single supportive detail: {e}")
        flash("An error occurred while retrieving the record. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def update_supportive_detail(record_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Supportive_Details_Information
            SET
                Facility_Number = ?,
                Facility_Name = ?,
                Public_Or_Confidential = ?,
                Collateral_Visit = ?,
                Visit_Date = ?,
                Visit_Reason_Description = ?,
                LPA_Signed_Ind = ?,
                LPA_Name = ?,
                Signed_DateTime = ?,
                Updated_By = 'Admin',
                Update_DateTime = ?,
                LPA_Sign = ?
            WHERE Supportive_Details_Information_Id = ?
        """, data['Facility_Number'], data['Facility_Name'], data['Public_Or_Confidential'], data['Collateral_Visit'], 
           data['Visit_Date'], data['Visit_Reason_Description'], data['LPA_Signed_Ind'], 
           data['LPA_Name'], data['Signed_DateTime'], datetime.now(), data['LPA_Sign'], record_id)
        conn.commit()
    except Exception as e:
        print("Error updating supportive detail: {e}")
        flash("An error occurred while updating the record. Please try again.", "danger")
    finally:
        conn.close()

def delete_supportive_detail(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Supportive_Details_Information WHERE Supportive_Details_Information_Id = ?", record_id)
        conn.commit()
    except Exception as e:
        print("Error deleting supportive detail: {e}")
        flash("An error occurred while deleting the record. Please try again.", "danger")
    finally:
        conn.close()

def insert_notification(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Notification_Of_Incomplete_Application (
                Notice_Date,
                Applicant_Name,
                Facility_Number,
                Received_Date,
                Appl_For_Facility_License_LIC200_200A_Ind,
                Applicant_Information_LIC215_Ind,
                Designation_Of_Facility_Responsibility_LIC308_Ind,
                Administrative_Organization_LIC309_Ind,
                Monthly_Operating_Statement_LIC401_Ind,
                Financial_Info_Release_Verification_LIC404_Ind,
                Personnel_Report_LIC500_Ind,
                Personnel_Record_LIC501_Ind,
                Facility_Personnel_Health_Screening_Rpt_LIC503_Ind,
                Health_Screening_Rpt_Personnel_Names,
                Applicant_Criminal_Record_Statement_LIC508_Ind,
                Criminal_Record_Statement_Personnel_Names,
                Emergency_Disaster_Plan_LIC610_610A_Ind,
                Facility_Sketch_Floor_Plan_LIC999_Ind,
                Orientation_Certificate_Ind,
                Articles_Of_Incorporation_Ind,
                Verification_Of_Admin_Or_Dir_Qualification_Ind,
                TB_Clearance_For_Applicant_Ind,
                TB_Clearance_For_Applicant_Names,
                Personnel_Policies_Ind,
                In_Service_Staff_Training_Ind,
                Job_Desc_Of_Each_Pos_Ind,
                Facility_Program_Description_Ind,
                Rules_Of_Discipline_Policies_Ind,
                Admission_Policies_Procedures_Ind,
                Admission_Agreement_Ind,
                Sample_Menu_Ind,
                List_Of_In_And_Outdoor_Equipment_Inv_Ind,
                Control_Of_Property_Ind,
                Bacteriol_Analysis_Of_Private_Water_Supply_Ind,
                Other_Ind,
                Other_Description,
                LPA_Sign,
                LPA_Phone_Number,
                Inserted_DateTime,
                Created_By,
                Create_DateTime
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, 
        data['Notice_Date'], data['Applicant_Name'], data['Facility_Number'], data['Received_Date'],
        data['Appl_For_Facility_License_LIC200_200A_Ind'], data['Applicant_Information_LIC215_Ind'],
        data['Designation_Of_Facility_Responsibility_LIC308_Ind'], data['Administrative_Organization_LIC309_Ind'],
        data['Monthly_Operating_Statement_LIC401_Ind'], data['Financial_Info_Release_Verification_LIC404_Ind'],
        data['Personnel_Report_LIC500_Ind'], data['Personnel_Record_LIC501_Ind'],
        data['Facility_Personnel_Health_Screening_Rpt_LIC503_Ind'], data['Health_Screening_Rpt_Personnel_Names'],
        data['Applicant_Criminal_Record_Statement_LIC508_Ind'], data['Criminal_Record_Statement_Personnel_Names'],
        data['Emergency_Disaster_Plan_LIC610_610A_Ind'], data['Facility_Sketch_Floor_Plan_LIC999_Ind'],
        data['Orientation_Certificate_Ind'], data['Articles_Of_Incorporation_Ind'],
        data['Verification_Of_Admin_Or_Dir_Qualification_Ind'], data['TB_Clearance_For_Applicant_Ind'],
        data['TB_Clearance_For_Applicant_Names'], data['Personnel_Policies_Ind'], data['In_Service_Staff_Training_Ind'],
        data['Job_Desc_Of_Each_Pos_Ind'], data['Facility_Program_Description_Ind'],
        data['Rules_Of_Discipline_Policies_Ind'], data['Admission_Policies_Procedures_Ind'],
        data['Admission_Agreement_Ind'], data['Sample_Menu_Ind'], data['List_Of_In_And_Outdoor_Equipment_Inv_Ind'],
        data['Control_Of_Property_Ind'], data['Bacteriol_Analysis_Of_Private_Water_Supply_Ind'],
        data['Other_Ind'], data['Other_Description'], data['LPA_Sign'], data['LPA_Phone_Number'],
        datetime.now(), 'Admin', datetime.now())
        conn.commit()
    except Exception as e:
        print("Error inserting notification: {e}")
        flash("An error occurred while submitting the form. Please try again.", "danger")
    finally:
        conn.close()

def read_notifications(facility_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Notification_Of_Incomplete_Application WHERE Facility_Number = ?", facility_number)
        result = cursor.fetchall()
    except Exception as e:
        print("Error reading notifications: {e}")
        flash("An error occurred while retrieving notifications. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    print("NOTIFICATIONS>>>>>>>>>>>", result)
    return result

def read_single_notification(notification_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Notification_Of_Incomplete_Application WHERE Notification_Of_Incomplete_Application_Id = ?", notification_id)
        result = cursor.fetchone()
    except Exception as e:
        print("Error reading single notification: {e}")
        flash("An error occurred while retrieving the notification. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def update_notification(notification_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Notification_Of_Incomplete_Application
            SET
                Notice_Date = ?,
                Applicant_Name = ?,
                Facility_Number = ?,
                Received_Date = ?,
                Appl_For_Facility_License_LIC200_200A_Ind = ?,
                Applicant_Information_LIC215_Ind = ?,
                Designation_Of_Facility_Responsibility_LIC308_Ind = ?,
                Administrative_Organization_LIC309_Ind = ?,
                Monthly_Operating_Statement_LIC401_Ind = ?,
                Financial_Info_Release_Verification_LIC404_Ind = ?,
                Personnel_Report_LIC500_Ind = ?,
                Personnel_Record_LIC501_Ind = ?,
                Facility_Personnel_Health_Screening_Rpt_LIC503_Ind = ?,
                Health_Screening_Rpt_Personnel_Names = ?,
                Applicant_Criminal_Record_Statement_LIC508_Ind = ?,
                Criminal_Record_Statement_Personnel_Names = ?,
                Emergency_Disaster_Plan_LIC610_610A_Ind = ?,
                Facility_Sketch_Floor_Plan_LIC999_Ind = ?,
                Orientation_Certificate_Ind = ?,
                Articles_Of_Incorporation_Ind = ?,
                Verification_Of_Admin_Or_Dir_Qualification_Ind = ?,
                TB_Clearance_For_Applicant_Ind = ?,
                TB_Clearance_For_Applicant_Names = ?,
                Personnel_Policies_Ind = ?,
                In_Service_Staff_Training_Ind = ?,
                Job_Desc_Of_Each_Pos_Ind = ?,
                Facility_Program_Description_Ind = ?,
                Rules_Of_Discipline_Policies_Ind = ?,
                Admission_Policies_Procedures_Ind = ?,
                Admission_Agreement_Ind = ?,
                Sample_Menu_Ind = ?,
                List_Of_In_And_Outdoor_Equipment_Inv_Ind = ?,
                Control_Of_Property_Ind = ?,
                Bacteriol_Analysis_Of_Private_Water_Supply_Ind = ?,
                Other_Ind = ?,
                Other_Description = ?,
                LPA_Sign = ?,
                LPA_Phone_Number = ?,
                Updated_By = 'Admin',
                Update_DateTime = ?
            WHERE Notification_Of_Incomplete_Application_Id = ?
        """, 
        data['Notice_Date'], data['Applicant_Name'], data['Facility_Number'], data['Received_Date'],
        data['Appl_For_Facility_License_LIC200_200A_Ind'], data['Applicant_Information_LIC215_Ind'],
        data['Designation_Of_Facility_Responsibility_LIC308_Ind'], data['Administrative_Organization_LIC309_Ind'],
        data['Monthly_Operating_Statement_LIC401_Ind'], data['Financial_Info_Release_Verification_LIC404_Ind'],
        data['Personnel_Report_LIC500_Ind'], data['Personnel_Record_LIC501_Ind'],
        data['Facility_Personnel_Health_Screening_Rpt_LIC503_Ind'], data['Health_Screening_Rpt_Personnel_Names'],
        data['Applicant_Criminal_Record_Statement_LIC508_Ind'], data['Criminal_Record_Statement_Personnel_Names'],
        data['Emergency_Disaster_Plan_LIC610_610A_Ind'], data['Facility_Sketch_Floor_Plan_LIC999_Ind'],
        data['Orientation_Certificate_Ind'], data['Articles_Of_Incorporation_Ind'],
        data['Verification_Of_Admin_Or_Dir_Qualification_Ind'], data['TB_Clearance_For_Applicant_Ind'],
        data['TB_Clearance_For_Applicant_Names'], data['Personnel_Policies_Ind'], data['In_Service_Staff_Training_Ind'],
        data['Job_Desc_Of_Each_Pos_Ind'], data['Facility_Program_Description_Ind'],
        data['Rules_Of_Discipline_Policies_Ind'], data['Admission_Policies_Procedures_Ind'],
        data['Admission_Agreement_Ind'], data['Sample_Menu_Ind'], data['List_Of_In_And_Outdoor_Equipment_Inv_Ind'],
        data['Control_Of_Property_Ind'], data['Bacteriol_Analysis_Of_Private_Water_Supply_Ind'],
        data['Other_Ind'], data['Other_Description'], data['LPA_Sign'], data['LPA_Phone_Number'],
        datetime.now(), notification_id)
        conn.commit()
    except Exception as e:
        print("Error updating notification: {e}")
        flash("An error occurred while updating the notification. Please try again.", "danger")
    finally:
        conn.close()

def delete_notification(notification_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notification_Of_Incomplete_Application WHERE Notification_Of_Incomplete_Application_Id = ?", notification_id)
        conn.commit()
    except Exception as e:
        print("Error deleting notification: {e}")
        flash("An error occurred while deleting the notification. Please try again.", "danger")
    finally:
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sitevisitnotice', methods=['GET', 'POST'])
def site_visit_notice():
    if request.method == 'POST':
        data = {
            'Regional_Office_Id': request.form['Regional_Office_Id'],
            'Facility_Number': request.form['Facility_Number'],
            'Site_Visit_Date': request.form['Site_Visit_Date'],
            'Regulatory_Violation_Citation_Ind': request.form['Regulatory_Violation_Citation_Ind'],
            'Regulatory_Violation_TypeA_Citation_Ind': request.form['Regulatory_Violation_TypeA_Citation_Ind'],
            'Regulatory_Violation_TypeB_Citation_Ind': request.form['Regulatory_Violation_TypeB_Citation_Ind'],
            'LPA_Name': request.form['LPA_Name'],
            'LPA_Phone_Number': request.form['LPA_Phone_Number']
        }
        insert_site_visit_notice(data)
        return redirect(url_for('list_notices', Facility_Number=request.form['Facility_Number']))
    return render_template('siteVisitNotice/sitevisitnotice.html', notice=None, mode=None)

@app.route('/listnotices', methods=['GET', 'POST'])
def list_notices():
    facility_number = request.form.get('Facility_Number') if request.method == 'POST' else request.args.get('Facility_Number')
    notices = read_site_visit_notice(facility_number) if facility_number else None
    return render_template('siteVisitNotice/listnotices.html', notices=notices, facility_number=facility_number)

@app.route('/view/<int:site_visit_notice_id>')
def view_notice(site_visit_notice_id):
    notice = read_single_site_visit_notice(site_visit_notice_id)
    return render_template('siteVisitNotice/sitevisitnotice.html', notice=notice, mode='view')

@app.route('/edit/<int:site_visit_notice_id>', methods=['GET', 'POST'])
def edit_notice(site_visit_notice_id):
    if request.method == 'POST':
        data = {
            'Regional_Office_Id': request.form['Regional_Office_Id'],
            'Facility_Number': request.form['Facility_Number'],
            'Site_Visit_Date': request.form['Site_Visit_Date'],
            'Regulatory_Violation_Citation_Ind': request.form['Regulatory_Violation_Citation_Ind'],
            'Regulatory_Violation_TypeA_Citation_Ind': request.form['Regulatory_Violation_TypeA_Citation_Ind'],
            'Regulatory_Violation_TypeB_Citation_Ind': request.form['Regulatory_Violation_TypeB_Citation_Ind'],
            'LPA_Name': request.form['LPA_Name'],
            'LPA_Phone_Number': request.form['LPA_Phone_Number']
        }
        update_site_visit_notice(site_visit_notice_id, data)
        return redirect(url_for('list_notices', Facility_Number=request.form['Facility_Number']))
    notice = read_single_site_visit_notice(site_visit_notice_id)
    return render_template('siteVisitNotice/sitevisitnotice.html', notice=notice, mode='edit')

@app.route('/delete/<int:site_visit_notice_id>', methods=['POST'])
def delete_notice(site_visit_notice_id):
    facility_number = request.form['Facility_Number']
    delete_site_visit_notice(site_visit_notice_id)
    return redirect(url_for('list_notices', Facility_Number=facility_number))

@app.route('/supportivedetailinfo', methods=['GET', 'POST'])
def supportive_detail_information():
    if request.method == 'POST':
        try:
            data = {
                'Facility_Number': request.form.get('facility_number'),
                'Facility_Name': request.form.get('facility_name'),
                'Public_Or_Confidential': request.form.get('confidential'),
                'Collateral_Visit': request.form.get('collateral_visit'),
                'Visit_Date': request.form.get('date_of_contact'),
                'Visit_Reason_Description': request.form.get('description'),
                'LPA_Signed_Ind': 1 if request.form.get('evaluator_signature') else 0,
                'LPA_Name': request.form.get('evaluator_name'),
                'Signed_DateTime': request.form.get('evaluator_date'),
                'LPA_Sign': request.form.get('evaluator_signature')
            }
            insert_supportive_detail(data)
            flash("Form submitted successfully!", "success")
        except Exception as e:
            print("Error inserting supportive details information: {e}")
            flash("An error occurred while submitting the form. Please try again.", "danger")
        return redirect(url_for('list_supportive_details', Facility_Number=request.form['facility_number']))
    return render_template('supportiveDetailInfo/supportivedetailInfo.html', detail=None, mode=None)

@app.route('/listsupportivedetails', methods=['GET', 'POST'])
def list_supportive_details():
    facility_number = request.form.get('Facility_Number') if request.method == 'POST' else request.args.get('Facility_Number')
    details = read_supportive_details(facility_number) if facility_number else None
    print("FACILITY NUMBER>>>>>>",facility_number, details)
    return render_template('supportiveDetailInfo/listsupportivedetails.html', records=details, facility_number=facility_number)

@app.route('/viewdetail/<int:record_id>')
def view_supportive_detail(record_id):
    detail = read_single_supportive_detail(record_id)
    return render_template('supportiveDetailInfo/supportivedetailInfo.html', detail=detail, mode='view')

@app.route('/editdetail/<int:record_id>', methods=['GET', 'POST'])
def edit_supportive_detail(record_id):
    if request.method == 'POST':
        try:
            data = {
                'Facility_Number': request.form.get('facility_number'),
                'Facility_Name': request.form.get('facility_name'),
                'Public_Or_Confidential': request.form.get('confidential'),
                'Collateral_Visit': request.form.get('collateral_visit'),
                'Visit_Date': request.form.get('date_of_contact'),
                'Visit_Reason_Description': request.form.get('description'),
                'LPA_Signed_Ind': 1 if request.form.get('evaluator_signature') else 0,
                'LPA_Name': request.form.get('evaluator_name'),
                'Signed_DateTime': request.form.get('evaluator_date'),
                'LPA_Sign': request.form.get('evaluator_signature')
            }
            update_supportive_detail(record_id, data)
            flash("Record updated successfully!", "success")
        except Exception as e:
            print("Error updating supportive detail: {e}")
            flash("An error occurred while updating the record. Please try again.", "danger")
        return redirect(url_for('list_supportive_details', Facility_Number=request.form.get('facility_number')))
    detail = read_single_supportive_detail(record_id)
    return render_template('supportiveDetailInfo/supportivedetailInfo.html', detail=detail, mode='edit')

@app.route('/deletedetail/<int:record_id>', methods=['POST'])
def delete_detail(record_id):
    facility_number = request.form.get('Facility_Number')
    delete_supportive_detail(record_id)
    return redirect(url_for('list_supportive_details', Facility_Number=facility_number))

@app.route('/notificationOfIncompleteApplication', methods=['GET', 'POST'])
def notification_of_incomplete_application():
    if request.method == 'POST':
        data = {
            'Notice_Date': request.form.get('date'),
            'Applicant_Name': request.form.get('applicant_name'),
            'Facility_Number': request.form.get('facility_file_number'),
            'Received_Date': request.form.get('received_date'),
            'Appl_For_Facility_License_LIC200_200A_Ind': 1 if request.form.get('lic200a') else 0,
            'Applicant_Information_LIC215_Ind': 1 if request.form.get('lic215') else 0,
            'Designation_Of_Facility_Responsibility_LIC308_Ind': 1 if request.form.get('lic308') else 0,
            'Administrative_Organization_LIC309_Ind': 1 if request.form.get('lic309') else 0,
            'Monthly_Operating_Statement_LIC401_Ind': 1 if request.form.get('lic401') else 0,
            'Financial_Info_Release_Verification_LIC404_Ind': 1 if request.form.get('lic404') else 0,
            'Personnel_Report_LIC500_Ind': 1 if request.form.get('lic500') else 0,
            'Personnel_Record_LIC501_Ind': 1 if request.form.get('lic501') else 0,
            'Facility_Personnel_Health_Screening_Rpt_LIC503_Ind': 1 if request.form.get('lic503') else 0,
            'Health_Screening_Rpt_Personnel_Names': request.form.get('lic503_detail'),
            'Applicant_Criminal_Record_Statement_LIC508_Ind': 1 if request.form.get('lic508') else 0,
            'Criminal_Record_Statement_Personnel_Names': request.form.get('lic508_detail'),
            'Emergency_Disaster_Plan_LIC610_610A_Ind': 1 if request.form.get('lic610') else 0,
            'Facility_Sketch_Floor_Plan_LIC999_Ind': 1 if request.form.get('lic999') else 0,
            'Orientation_Certificate_Ind': 1 if request.form.get('orientation_certificate') else 0,
            'Articles_Of_Incorporation_Ind': 1 if request.form.get('partnership_agreement') else 0,
            'Verification_Of_Admin_Or_Dir_Qualification_Ind': 1 if request.form.get('verification_qualifications') else 0,
            'TB_Clearance_For_Applicant_Ind': 1 if request.form.get('tb_clearances') else 0,
            'TB_Clearance_For_Applicant_Names': request.form.get('tb_clearances_detail'),
            'Personnel_Policies_Ind': 1 if request.form.get('personnel_policies') else 0,
            'In_Service_Staff_Training_Ind': 1 if request.form.get('in_service_training') else 0,
            'Job_Desc_Of_Each_Pos_Ind': 1 if request.form.get('job_description') else 0,
            'Facility_Program_Description_Ind': 1 if request.form.get('program_description') else 0,
            'Rules_Of_Discipline_Policies_Ind': 1 if request.form.get('discipline_policies') else 0,
            'Admission_Policies_Procedures_Ind': 1 if request.form.get('admission_policies') else 0,
            'Admission_Agreement_Ind': 1 if request.form.get('admission_agreement') else 0,
            'Sample_Menu_Ind': 1 if request.form.get('sample_menu') else 0,
            'List_Of_In_And_Outdoor_Equipment_Inv_Ind': 1 if request.form.get('inventory_furniture') else 0,
            'Control_Of_Property_Ind': 1 if request.form.get('control_property') else 0,
            'Bacteriol_Analysis_Of_Private_Water_Supply_Ind': 1 if request.form.get('bacteriological_analysis') else 0,
            'Other_Ind': 1 if request.form.get('other_ind') else 0,
            'Other_Description': request.form.get('other'),
            'LPA_Sign': request.form.get('licensing_reviewer_signature'),
            'LPA_Phone_Number': request.form.get('phone_number')
        }
        print("NOTIFIFCATION DATA TO INSERT>>>>>>>>>>>",data)
        insert_notification(data)
        return redirect(url_for('list_notifications', Facility_Number=request.form.get('facility_file_number')))
    return render_template('NOIA/notification.html', notification=None, mode=None)

@app.route('/listnotifications', methods=['GET', 'POST'])
def list_notifications():
    facility_number = request.form.get('Facility_Number') if request.method == 'POST' else request.args.get('Facility_Number')
    notifications = read_notifications(facility_number) if facility_number else None
    return render_template('NOIA/listnotifications.html', notifications=notifications, facility_number=facility_number)

@app.route('/viewnotification/<int:notification_id>')
def view_notification(notification_id):
    notification = read_single_notification(notification_id)
    return render_template('NOIA/notification.html', notification=notification, mode='view')

@app.route('/editnotification/<int:notification_id>', methods=['GET', 'POST'])
def edit_notification(notification_id):
    if request.method == 'POST':
        data = {
            'Notice_Date': request.form.get('date'),
            'Applicant_Name': request.form.get('applicant_name'),
            'Facility_Number': request.form.get('facility_file_number'),
            'Received_Date': request.form.get('received_date'),
            'Appl_For_Facility_License_LIC200_200A_Ind': 1 if request.form.get('lic200a') else 0,
            'Applicant_Information_LIC215_Ind': 1 if request.form.get('lic215') else 0,
            'Designation_Of_Facility_Responsibility_LIC308_Ind': 1 if request.form.get('lic308') else 0,
            'Administrative_Organization_LIC309_Ind': 1 if request.form.get('lic309') else 0,
            'Monthly_Operating_Statement_LIC401_Ind': 1 if request.form.get('lic401') else 0,
            'Financial_Info_Release_Verification_LIC404_Ind': 1 if request.form.get('lic404') else 0,
            'Personnel_Report_LIC500_Ind': 1 if request.form.get('lic500') else 0,
            'Personnel_Record_LIC501_Ind': 1 if request.form.get('lic501') else 0,
            'Facility_Personnel_Health_Screening_Rpt_LIC503_Ind': 1 if request.form.get('lic503') else 0,
            'Health_Screening_Rpt_Personnel_Names': request.form.get('lic503_detail'),
            'Applicant_Criminal_Record_Statement_LIC508_Ind': 1 if request.form.get('lic508') else 0,
            'Criminal_Record_Statement_Personnel_Names': request.form.get('lic508_detail'),
            'Emergency_Disaster_Plan_LIC610_610A_Ind': 1 if request.form.get('lic610') else 0,
            'Facility_Sketch_Floor_Plan_LIC999_Ind': 1 if request.form.get('lic999') else 0,
            'Orientation_Certificate_Ind': 1 if request.form.get('orientation_certificate') else 0,
            'Articles_Of_Incorporation_Ind': 1 if request.form.get('partnership_agreement') else 0,
            'Verification_Of_Admin_Or_Dir_Qualification_Ind': 1 if request.form.get('verification_qualifications') else 0,
            'TB_Clearance_For_Applicant_Ind': 1 if request.form.get('tb_clearances') else 0,
            'TB_Clearance_For_Applicant_Names': request.form.get('tb_clearances_detail'),
            'Personnel_Policies_Ind': 1 if request.form.get('personnel_policies') else 0,
            'In_Service_Staff_Training_Ind': 1 if request.form.get('in_service_training') else 0,
            'Job_Desc_Of_Each_Pos_Ind': 1 if request.form.get('job_description') else 0,
            'Facility_Program_Description_Ind': 1 if request.form.get('program_description') else 0,
            'Rules_Of_Discipline_Policies_Ind': 1 if request.form.get('discipline_policies') else 0,
            'Admission_Policies_Procedures_Ind': 1 if request.form.get('admission_policies') else 0,
            'Admission_Agreement_Ind': 1 if request.form.get('admission_agreement') else 0,
            'Sample_Menu_Ind': 1 if request.form.get('sample_menu') else 0,
            'List_Of_In_And_Outdoor_Equipment_Inv_Ind': 1 if request.form.get('inventory_furniture') else 0,
            'Control_Of_Property_Ind': 1 if request.form.get('control_property') else 0,
            'Bacteriol_Analysis_Of_Private_Water_Supply_Ind': 1 if request.form.get('bacteriological_analysis') else 0,
            'Other_Ind': 1 if request.form.get('other_ind') else 0,
            'Other_Description': request.form.get('other'),
            'LPA_Sign': request.form.get('licensing_reviewer_signature'),
            'LPA_Phone_Number': request.form.get('phone_number')
        }
        update_notification(notification_id, data)
        return redirect(url_for('list_notifications', Facility_Number=request.form.get('facility_file_number')))
    notification = read_single_notification(notification_id)
    return render_template('NOIA/notification.html', notification=notification, mode='edit')

@app.route('/deletenotification/<int:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    facility_number = request.form.get('Facility_Number')
    delete_notification(notification_id)
    return redirect(url_for('list_notifications', Facility_Number=facility_number))

#---------------------- Operation_Violation_Notice LIC195-------------------------------------------
#Create
def insert_operation_violation_notice(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Operation_Violation_Law (
                Original_Regional_Office_Number,
                Facility_Name,
                Facility_Address,
                Facility_City,
                Form_Name,
                Form_Number,
                Location_Label,
                LPA_Manager_Signed_DateTime,
                Signed_Ind,     
                Code_FT,
                Inserted_DateTime,
                Created_By,
                Create_DateTime
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data['Regional_Office_Number'], data['Facility_Name'], data['Facility_Address'], data['Facility_City'],
            'NOTICE OF OPERATION IN VIOLATION OF LAW', 'LIC195',
            data['Location_Label'], datetime.now(), '1', 'CODEFT' ,datetime.now(), 'Admin', datetime.now())
        conn.commit()
    except Exception as e:
        print(f"Error inserting operation violation notice: {e}")
        flash("An error occurred while submitting the form. Please try again.", "danger")
    finally:
        conn.close()

#Read
def read_single_operation_violation(operation_violation_law_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Operation_Violation_Law WHERE Operation_Violation_Law_Id = ?", operation_violation_law_id)
        result = cursor.fetchone()
    except Exception as e:
        print(f"Error reading single operation violation notice: {e}")
        flash("An error occurred while retrieving the notice. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

def read_operation_violation(Facility_Name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Operation_Violation_Law WHERE Facility_Name = ?", Facility_Name)
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error reading operation violation notice: {e}")
        flash("An error occurred while retrieving notices. Please try again.", "danger")
        result = None
    finally:
        conn.close()
    return result

#Update

def edit_operation_violation_notice(operation_violation_law_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Operation_Violation_Law
            SET
                Original_Regional_Office_Number,
                Facility_Name
                Facility_Address,
                Facility_City,
                Location_Label,
                Updated_By = 'Admin',
                Update_DateTime = ?
            WHERE Operation_Violation_Law_Id = ?
        """, data['Regional_Office_Number'], data['Facility_Name'], data['Facility_Address'], data['Facility_City'],
           data['Location_Label'], 'Admin', datetime.now(), operation_violation_law_id)
        conn.commit()
    except Exception as e:
        print(f"Error updating operation violation notice: {e}")
        flash("An error occurred while updating the notice. Please try again.", "danger")
    finally:
        conn.close()

#Delete
def delete_operation_violation(operation_violation_notice_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Operation_Violation_Law WHERE operation_violation_notice_id = ?", operation_violation_notice_id)
        conn.commit()
    except Exception as e:
        print(f"Error deleting site visit notice: {e}")
        flash("An error occurred while deleting the notice. Please try again.", "danger")
    finally:
        conn.close()

#Lookup Functions

# for drop down menu in violation notices page
def lookup_Facility_Names():
    facility_names = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Facility_Name FROM Operation_Violation_Law")
        facility_names = [row[0] for row in cursor.fetchall()]  # Extract the first element of each tuple
    except Exception as e:
        print(f"Error looking up Facilities: {e}")
        flash("An error occurred while looking up Facilities", "danger")
    finally:
        if conn:
            conn.close()
    return facility_names

# fill out drop down menu fields
def read_operation_violation(facility_name):
    operation_violations = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Operation_Violation_Law_Id, Facility_Name, Create_DateTime FROM Operation_Violation_Law WHERE Facility_Name = ?", facility_name)
        rows = cursor.fetchall()
        for row in rows:
            operation_violations.append({
                'operation_violation_law_id': row[0],
                'facility_name': row[1],
                'create_datetime': row[2],
            })
    except Exception as e:
        print(f"Error reading Operation Violations: {e}")
        flash("An error occurred while reading Operation Violations", "danger")
    finally:
        if conn:
            conn.close()
    return operation_violations

def lookup_Regional_Office_Name():
    regional_offices = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Regional_Office_Name FROM Regional_Office")
        regional_offices = cursor.fetchall()  # Fetch all rows as tuples
    except Exception as e:
        print(f"Error looking up Regional Offices: {e}")
        flash("An error occurred while looking up Regional Offices", "danger")
    finally:
        if conn:
            conn.close()
    
    return regional_offices

def lookup_Regional_Office_Info(office_name=None):
    r_offices = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Regional_Office_Name, Office_City, Office_Street_Address, Office_State, Office_Zip_Code, Office_Phone_Number, Regional_Office_Number FROM Regional_Office")
        rows = cursor.fetchall()
        if office_name:
            # Filter rows based on the office_name
            rows = [row for row in rows if row[0] == office_name]  # Access by integer index
        for row in rows:
            r_offices.append({
                'name': row[0],  # Column 1: Regional_Office_Name
                'city': row[1],  # Column 2: Office_City
                'street_address': row[2],  # Column 3: Office_Street_Address
                'state': row[3],  # Column 4: Office_State
                'zip_code': row[4],  # Column 5: Office_Zip_Code
                'phone_number': row[5],  # Column 6: Office_Phone_Number
                'regional_office_number': row[6]
            })
    except Exception as e:
        print(f"Error looking up Regional Offices: {e}")
        flash("An error occurred while looking up Regional Offices", "danger")
    finally:
        if conn:
            conn.close()
    return r_offices

def lookup_Regional_Office_Info_By_Office_Number(office_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Regional_Office_Name, Office_City, Office_Street_Address, Office_State, Office_Zip_Code, Office_Phone_Number, Regional_Office_Number FROM Regional_Office WHERE Regional_Office_Number = ?", office_number )
        regional_office = cursor.fetchone()
    except Exception as e:
        print(f"Error looking up Regional Office by Regional_Office_Number: {e}")
        flash("An error occurred while looking up the Regional Office by Regional Office Number", "danger")
    finally:
        if conn:
            conn.close()
    return regional_office

#Routing

@app.route('/operationviolationnotice', methods=['GET', 'POST'])
def operation_violation_notice():
    regional_offices = lookup_Regional_Office_Name()  # Fetch regional offices

    if request.method == 'POST':
        data = {
            'Facility_Name': request.form['Facility_Name'],
            'Facility_Address': request.form['Facility_Address'],
            'Facility_City': request.form['Facility_City'],
            'Location_Label': request.form['Location_Label'],
            'LPA_Manager_Signed_DateTime': request.form['LPA_Manager_Signed_DateTime'],
            'Regional_Office_Number': request.form['Regional_Office_Number']  # Add Regional_Office_Id from form
        }
        insert_operation_violation_notice(data)
        return redirect(url_for('list_operation_violation', Facility_Name=request.form['Facility_Name']))

    return render_template('operationViolationNotice/operationviolationnotice.html', regional_offices=regional_offices, notice=None, mode=None)

@app.route('/delete_notice/<int:operation_violation_notice_id>', methods=['POST'])
def delete_operation_violation_notice(operation_violation_notice_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Operation_Violation_Law WHERE Operation_Violation_Law_Id = ?", operation_violation_notice_id)
        conn.commit()
        flash("Notice deleted successfully.", "success")
    except Exception as e:
        print(f"Error deleting operation violation notice: {e}")
        flash("An error occurred while deleting the notice. Please try again.", "danger")
    finally:
        conn.close()
    return redirect(url_for('list_operation_violation'))

@app.route('/list_operation_violation_notices', methods=['GET', 'POST'])
def list_operation_violation():
    facility_name = request.form.get('facilityName') if request.method == 'POST' else request.args.get('facilityName')
    notices = read_operation_violation(facility_name) if facility_name else []
    facility_names = lookup_Facility_Names()
    return render_template('operationViolationNotice/list_operation_violation_notices.html', notices=notices, facility_names=facility_names, facility_name=facility_name)


@app.route('/api/regional-office-info/<office_name>', methods=['GET'])
def get_office_details(office_name):
    office_data = lookup_Regional_Office_Info(office_name)
    if office_data:
        return jsonify(office_data[0])  # Return the first item in the list
    else:
        flash("Office not found", "warning")  # Optional: Send a message back to the client
        return jsonify({"error": "Office not found"}), 404
    
@app.route('/viewOperationViolation/<int:operation_violation_law_id>')
def view_operation_violation_notice(operation_violation_law_id):
    notice = read_single_operation_violation(operation_violation_law_id)
    
    # Assuming Original_Regional_Office_Number is part of notice data
    original_regional_office_number = notice[4]
    
    #print(f"Original Regional Office Number: {original_regional_office_number}")
    # Call lookup function to get regional office info
    regional_office = lookup_Regional_Office_Info_By_Office_Number(original_regional_office_number)

    #print(f"Regional Office Info: {regional_office}")
    
    return render_template('operationViolationNotice/operationviolationnotice.html', notice=notice, regional_office=regional_office, mode='view')

@app.route('/updateOperationViolation/<int:operation_violation_law_id>', methods=['GET', 'POST'])
def update_operation_violation_notice(operation_violation_law_id):
    regional_offices = lookup_Regional_Office_Name()
    if request.method == 'POST':
        data = {
            'Facility_Name': request.form['Facility_Name'],
            'Facility_Address': request.form['Facility_Address'],
            'Facility_City': request.form['Facility_City'],
            'Location_Label': request.form['Location_Label'],
            'LPA_Manager_Signed_DateTime': request.form['LPA_Manager_Signed_DateTime'],
            'Regional_Office_Number': request.form['Regional_Office_Number']
        }
        edit_operation_violation_notice(operation_violation_law_id, data)
        return redirect(url_for('list_operation_violation', Facility_Name=request.form['Facility_Name']))
    notice=read_single_operation_violation(operation_violation_law_id)
    return render_template('operationViolationNotice/operationviolationnotice.html', notice=notice, regional_offices=regional_offices, mode='edit')

#--------------------------------------------------------------#

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
