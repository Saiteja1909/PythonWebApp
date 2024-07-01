from flask import Flask, request, render_template, redirect, url_for, flash
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
            print(f"Error: {ex}")
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
        print(f"Error inserting site visit notice: {e}")
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
        print(f"Error reading site visit notice: {e}")
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
        print(f"Error reading single site visit notice: {e}")
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
        print(f"Error updating site visit notice: {e}")
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
        print(f"Error deleting site visit notice: {e}")
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
                Comments,
                LPA_Signed_Ind,
                LPA_Name,
                Signed_DateTime,
                Inserted_DateTime,
                Created_By,
                Create_DateTime,
                Updated_By,
                Update_DateTime,
                LPA_Sign
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data['Facility_Number'], data['Facility_Name'], data['Public_Or_Confidential'], data['Collateral_Visit'], 
           data['Visit_Date'], data['Visit_Reason_Description'], data['Comments'], data['LPA_Signed_Ind'], 
           data['LPA_Name'], data['Signed_DateTime'], datetime.now(), 'Admin', datetime.now(), 'Admin', 
           datetime.now(), data['LPA_Sign'])
        conn.commit()
    except Exception as e:
        print(f"Error inserting supportive detail: {e}")
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
        print(f"Error reading supportive details: {e}")
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
        print(f"Error reading single supportive detail: {e}")
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
                Comments = ?,
                LPA_Signed_Ind = ?,
                LPA_Name = ?,
                Signed_DateTime = ?,
                Updated_By = 'Admin',
                Update_DateTime = ?,
                LPA_Sign = ?
            WHERE Supportive_Details_Information_Id = ?
        """, data['Facility_Number'], data['Facility_Name'], data['Public_Or_Confidential'], data['Collateral_Visit'], 
           data['Visit_Date'], data['Visit_Reason_Description'], data['Comments'], data['LPA_Signed_Ind'], 
           data['LPA_Name'], data['Signed_DateTime'], datetime.now(), data['LPA_Sign'], record_id)
        conn.commit()
    except Exception as e:
        print(f"Error updating supportive detail: {e}")
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
        print(f"Error deleting supportive detail: {e}")
        flash("An error occurred while deleting the record. Please try again.", "danger")
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
                'Comments': request.form.get('comments'),
                'LPA_Signed_Ind': 1 if request.form.get('evaluator_signature') else 0,
                'LPA_Name': request.form.get('evaluator_name'),
                'Signed_DateTime': request.form.get('evaluator_date'),
                'LPA_Sign': request.form.get('evaluator_signature')
            }
            insert_supportive_detail(data)
            flash("Form submitted successfully!", "success")
        except Exception as e:
            print(f"Error inserting supportive details information: {e}")
            flash("An error occurred while submitting the form. Please try again.", "danger")
        return redirect(url_for('home'))
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
                'Comments': request.form.get('comments'),
                'LPA_Signed_Ind': 1 if request.form.get('evaluator_signature') else 0,
                'LPA_Name': request.form.get('evaluator_name'),
                'Signed_DateTime': request.form.get('evaluator_date'),
                'LPA_Sign': request.form.get('evaluator_signature')
            }
            update_supportive_detail(record_id, data)
            flash("Record updated successfully!", "success")
        except Exception as e:
            print(f"Error updating supportive detail: {e}")
            flash("An error occurred while updating the record. Please try again.", "danger")
        return redirect(url_for('list_supportive_details', Facility_Number=request.form.get('facility_number')))
    detail = read_single_supportive_detail(record_id)
    return render_template('supportiveDetailInfo/supportivedetailInfo.html', detail=detail, mode='edit')

@app.route('/deletedetail/<int:record_id>', methods=['POST'])
def delete_detail(record_id):
    facility_number = request.form.get('Facility_Number')
    delete_supportive_detail(record_id)
    return redirect(url_for('list_supportive_details', Facility_Number=facility_number))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
