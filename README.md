# Depencies

- html
- css
- python
- flask
- flask_mysqldb

# How to Run the Application

- After cloning the repository, install the above dependencies with ```pip install```
- Use ```flask run``` or ```python -m flask run```


# Briefly about the Project

- This is a Doctoral Search/Update Web application where backend connects to MySQL DB which has Doctoral data of PhD students

- This application has got the following 4 operations 
1. Insert a new student in the database. Your query should insert values for all attributes in the PhdStudent table. Link the new student with an existing scholarship and also add committee members for the student in the PhDCommittee table.
2. Update the payment amount of the TAs for a course given the course id and updated payment amount.
3. Display Grant Title, Type, and Account No. for a GRA student.
4. Delete a Self-Support student type who has not passed any milestone yet (to avoid integrity constraints). Your query should 
also reflect changes in the PhDStudent table.

- This application also provides additional functionality of catching excpetions and displaying the error logs as the info message in the Results section.