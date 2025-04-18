# Travel Log

## Project Summary

Travel Log is a Flask-based web application that allows users to create entries of their trips. Users can submit their information about where they visited and the rating they give it. All logs will be printed out under the travel log when submitted. User data is stored in DynamoDB, while world data is queried from a MySQL RDS instance.

## Technologies Used

- **Flask** (Python web framework)  
- **HTML** (Frontend)  
- **AWS EC2** (App hosting)  
- **AWS DynamoDB** (User data storage)  
- **AWS RDS (MySQL)** (World data storage)  

## Set Up and Run Instructions
The app can be accessed through a web brower using the URL http://192.168.0.99:8080

Alternatively, you can run the app on your local machine with your own RDS instance
1. In a terminal type `git clone https://github.com/alex-carr/CS178-Project1`
2. Change directory into the cloned folder using `cd CS178-Project1`
3. Create a creds.py file in the folder with credentials for an RDS server with the world data base installed
4. Run the flaskapp.py file using `nohup python3 flaskapp.py &`
5. Connect in a web browser using http://127.0.0.1:8080/
