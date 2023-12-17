from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' # this should be given
app.config['MYSQL_DB'] = 'cse_5330_project'

mysql = MySQL(app)

# Preparing Column names to display tabular results
def get_column_names(table_description):
    column_names = []
    for col in table_description:
        column_names.append(col[0])
    return column_names

# Landing route to handle all the get and post requests in the application
@app.route('/', methods=['post', 'get'])
def index():
    cursor = mysql.connection.cursor()
    result_count = 0
    result = ()
    column_names = ()
    task = ''
    result_message = ''
    if request.method == 'POST':
        filter_criterion = request.form.to_dict(flat=False)

        # Selecting available operations to perform
        if filter_criterion.get('query_opt'):
            task = filter_criterion['query_opt'][0]

        # Insert a new student in the database. Your query should insert values for all attributes in the PhdStudent table.
        # Link the new student with an existing scholarship and also add committee members for the student in the PhDCommittee table.
        if filter_criterion.get('add_student'):
            try:
                student_id = filter_criterion['student_id'][0]
                fname = filter_criterion['fname'][0]
                lname = filter_criterion['lname'][0]
                st_sem = filter_criterion['st_semester'][0]
                st_year = int(filter_criterion['st_year'][0])
                supervisor_id = filter_criterion['supervisor_id'][0]
                scholarship_type = filter_criterion['scholarship_type'][0]
                scholarship_source = filter_criterion['scholarship_source'][0]
                phd_committee_members = filter_criterion['phd_committee'][0].split(',')
                phd_student_insert_query = f"insert into _PHDSTUDENT values ('{student_id}', '{fname}', '{lname}', '{st_sem}', {st_year}, '{supervisor_id}');"
                scholarship_support_insert_query = f"insert into _SCHOLARSHIPSUPPORT values ('{student_id}', '{scholarship_type}', '{scholarship_source}');"
                phdcommittee_insert_query = 'insert into _PHDCOMMITTEE values'
                for mem in phd_committee_members:
                    phdcommittee_insert_query += f"('{student_id}', '{mem}'),"
                phdcommittee_insert_query = phdcommittee_insert_query[:len(phdcommittee_insert_query)-1]+';'
                cursor.execute(phd_student_insert_query)
                cursor.execute(scholarship_support_insert_query)
                cursor.execute(phdcommittee_insert_query)
                select_student_query = f"select * from _PHDSTUDENT where StudentId = '{student_id}'"
                result_count = cursor.execute(select_student_query)
                if result_count > 0:
                    result_message = 'Student added successfully...!!!'
                else:
                    result_message = 'Oops, failed adding Student.'
                result = cursor.fetchall()
                column_names = get_column_names(cursor.description)
            except Exception as e:
                result_message = 'Oops, failed adding Student. '+str(e)
        
        # Update the payment amount of the TAs for a course given the course id and updated payment amount.
        if filter_criterion.get('update_payment'):
            try:
                course_id = filter_criterion['course_id'][0]
                new_monthly_pay = int(filter_criterion['new_monthly_pay'][0])
                query_statement = f"update _GTA set MontlyPay = {new_monthly_pay} where SectionId like '{course_id}-%';"
                result_count = cursor.execute(query_statement)
                updated_records_query = f"select * from _GTA where SectionId like '{course_id}-%';"
                result_count = cursor.execute(updated_records_query)
                if result_count > 0:
                    result_message = 'Update successful. Fetched updated records successfully...!! '
                else:
                    result_message = 'Oops!! TAs Payment Update failed....'
                result = cursor.fetchall()
                column_names = get_column_names(cursor.description)
            except Exception as e:
                result_message = 'Oops, TAs Payment Update failed. '+str(e)
        
        # Display Grant Title, Type, and Account No. for a GRA student.
        if filter_criterion.get('find'):
            try:
                gra_keyword = filter_criterion['find_gra'][0]
                gra_keyword_regex = gra_keyword
                query_statement = f"select _GRANTS.GrantTitle, _GRANTS._Type, _GRANTS.AccountNo, _PHDSTUDENT.FName, _PHDSTUDENT.LName from _GRA, _GRANTS, _PHDSTUDENT where _GRA.StudentId = _PHDSTUDENT.StudentId and _GRA.Funding = _GRANTS.AccountNo and (_PHDSTUDENT.FName like '{gra_keyword_regex}%' or _PHDSTUDENT.LName like '{gra_keyword_regex}%');"
                result_count = cursor.execute(query_statement)
                if result_count > 0:
                    result_message = 'Data fetched successfully...!! '
                else:
                    result_message = 'Oops!! There are no records for this criterion.'
                result = cursor.fetchall()
                column_names = get_column_names(cursor.description)
            except Exception as e:
                result_message = 'Oops, finding GRA student failed. '+str(e)

        # Delete a Self-Support student type who has not passed any milestone yet (to avoid integrity constraints).
        # Your query should also reflect changes in the PhDStudent table.
        if filter_criterion.get('confirm_delete'):
            try:
                result_count = cursor.execute('''
                    DELETE FROM _PHDSTUDENT as phd_st
                    WHERE phd_st.StudentId is NOT NULL and EXISTS
                    (
                        SELECT *
                        FROM (
                            select * from _SELFSUPPORT as ssi where ssi.StudentId not in (
                                select distinct ss.*
                                from _SELFSUPPORT as ss, _MILESTONESPASSED as mp
                                where ss.StudentId = mp.StudentId
                            )) as MILESTONES_NOT_PASSED
                        WHERE MILESTONES_NOT_PASSED.StudentId = phd_st.StudentId
                    );  
                ''')
                result_count = cursor.execute('''
                    DELETE FROM _SELFSUPPORT as sso
                    WHERE sso.StudentId is NOT NULL and EXISTS
                    (
                        SELECT *
                        FROM (
                            select * from _SELFSUPPORT as ssi where ssi.StudentId not in (
                                select distinct ss.*
                                from _SELFSUPPORT as ss, _MILESTONESPASSED as mp
                                where ss.StudentId = mp.StudentId
                            )) as MILESTONES_NOT_PASSED
                        WHERE MILESTONES_NOT_PASSED.StudentId = sso.StudentId
                    );
                    ''')
                result_message = 'Self Support students who have not passed any milestone are deleted and PHDSTUDENT table is also updated!!!'
            except Exception as e:
                result_message = 'Oops, deleting Self Support student without Milestones failed. '+str(e)
    mysql.connection.commit()
    cursor.close()
    return render_template('index.html', data=result, column_names=column_names, task=task, result_message=result_message, result_count=result_count, groupby_data={}, filtered_data={})
 
if __name__ == "__main__":
    app.run(debug=True)