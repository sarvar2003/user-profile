---

# User Profile Project

Welcome to the User Profile Project! This is fully dockerized user profiles django project that uses token authentication to authenticate users

## Features

- **Django Back-End**: A robust back-end built with Django to handle user profile management.
- **User Authentication**: Includes login, registration, and user profile functionalities.
- **CRUD Operations**: Create, read, update, and delete user profiles.

## Getting Started

### Prerequisites

To run this project locally, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Django 3.2+](https://www.djangoproject.com/)
- [Git](https://git-scm.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarvar2003/user-profile.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd user-profile
   ```
   
### Running the Application

1. **Start the Django development server:**
   ```bash
   make run
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:8000
   ```

   You will see the home page of the user profile application. You can access the Django admin interface at `http://localhost:8000/admin` using the superuser credentials created earlier.

## Project Structure

- `user_profile/`: Contains the main project settings and configurations.
- `profiles/`: The app that handles user profile logic.
  - `models.py`: Defines the database models.
  - `views.py`: Handles the logic for each URL route.
  - `forms.py`: Contains form definitions for user input.
  - `urls.py`: Maps URL routes to views.
  - `templates/`: HTML templates for rendering the UI.
  - `static/`: Static files (CSS, JavaScript, images).

## Usage

### Endpoints

- **/profiles/**: Lists all user profiles.
- **/profiles/<id>**: Displays details of a specific user profile.
- **/profiles/add/**: Form to add a new user profile.
- **/profiles/edit/<id>**: Form to edit an existing user profile.
- **/profiles/delete/<id>**: Deletes a specific user profile.

### Forms

- **Registration Form**: Allows new users to register.
- **Login Form**: Enables users to log in to their account.
- **Profile Form**: For updating user profile details.

## Contributing

We welcome contributions! Please fork the repository and create a pull request with your changes. Ensure you follow the coding standards and include tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to reach out to the project maintainers.

---

This README provides a detailed overview of the Django-based project, with instructions for setting it up and running it locally. For more details, you can visit the [GitHub repository](https://github.com/sarvar2003/user-profile).
