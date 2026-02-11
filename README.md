# JobTrackr

JobTrackr is a simple web application built with Flask that allows users to track their job applications. This project is a great starting point for those who want to learn how to build a backend with Flask, integrate JWT for authentication, and work with databases.

## Features

- User registration and login
- Create and track job applications
- View applications by status (Applied, Interview, Offer, Rejected)
- JWT-based authentication

## Getting Started

To get this project running on your local machine, follow these steps:

### Prerequisites

You need Python 3.6 or higher installed on your machine. You'll also need to install the required dependencies from the `requirements.txt` file.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BrindirCoder/Job_Trackr.git

   cd JobTrackr

Create a virtual environment and activate it:

python3 -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt


Set up the database:
The project uses SQLite for local development. To create the database, run:

flask db init
flask db migrate
flask db upgrade


Set up your environment variables:
You need to set the following environment variables for the app to work:

SECRET_KEY: A secret key for session management.

JWT_SECRET_KEY: A secret key for JWT authentication.

Create a .env file in the project root and add these values:

SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key


Run the application:

flask run


The app will be running at http://127.0.0.1:5000/.

Testing the API

You can use Postman or curl to interact with the API:

Register a new user:
POST /register with JSON data:

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "yourpassword"
}


Login:
POST /login with JSON data:

{
  "email": "testuser@example.com",
  "password": "yourpassword"
}


Create a job application:
POST /applications with JSON data:

{
  "company_name": "OpenAI",
  "position_title": "Backend Engineer",
  "status": "Applied"
}

Contributing

Feel free to fork this repository and submit pull requests. If you have any suggestions or improvements, feel free to open an issue!

License

This project is licensed under the MIT License - see the LICENSE
 file for details.



