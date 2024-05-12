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

# Web Pages
## Landing
![image](https://github.com/Jashwanth459/doctoral-search-flask-app/assets/34550047/c690fffd-b0d8-4404-aa8f-393010635407)

## Insert Student
![image](https://github.com/Jashwanth459/doctoral-search-flask-app/assets/34550047/5c8cf112-cfeb-46bb-b822-e6f53c110d75)

## Update Payment details
![image](https://github.com/Jashwanth459/doctoral-search-flask-app/assets/34550047/6c992cc0-5c01-43f1-9e1c-581798f52f06)

## Display GRA
![image](https://github.com/Jashwanth459/doctoral-search-flask-app/assets/34550047/c9ffc462-0047-403f-8a64-efcf39c84a04)

## Delete Record
![image](https://github.com/Jashwanth459/doctoral-search-flask-app/assets/34550047/ea6be295-cdd7-4ff5-86c5-251134e0b127)
