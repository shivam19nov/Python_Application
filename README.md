# Registration Application
Flask Application to buid user registration

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Execution](#execution)
* [Validation](#validation)

## General info
This project is to build a basic user Registration application in python.
	
## Technologies
Project is created with:
* Python: 3.7.4
* Flask: 1.1.1
* Sqlite3
* HTML
* Tailwind CSS
* HeroIcons

## Execution
**Live Application available here -> [Registration Application](https://registration-form-flask.herokuapp.com/)**
**Download Entire Code From here -> **

## Validation

### FrontEnd
**While Capturing the data in form, following validations are done:**
* User First Name length should be 3-12 character long
* User Name should contain only letters
* User Last Name length should be 3-12 character long
* Password Should we alpha-numeric with special characters
* Password should be greater than 8 characters
* Email should follow standard email rules.

**Other Validation:**
* While Logging into the form, if credentials not match, then login will fail with a failure message.
* While registration, if user is already registered then registration will fail.

### BackEnd
* Passwords are **encrypted** while storing it in database.
* User Name and email is stored in lower case into the database to keep data clean.
* Whitespaces are trimmed if any, in User Name or email.
