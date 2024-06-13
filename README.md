# PcHelper

Welcome to PcHelper, your one-stop solution for building your perfect PC. This application allows users to register, set their budget and preferred computer type, and choose compatible components for their PC build.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login
- Set budget and preferred computer type (Gaming PC, Office PC, Workstation PC, or None)
- Choose compatible components in sequence: CPU, Motherboard, RAM, SSD, HDD, GPU, PSU, Chassis
- Compatibility checks for component selections
- Finalize selection and see total price
- Get recommendations for better components within the remaining budget

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/opbru/DBMS_project.git
    cd DBMS_project
    ```

2. **Set up the backend**:
    - Ensure you have Python installed.
    - Create a virtual environment and activate it:
      ```sh
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install the required packages:
      ```sh
      pip install -r requirements.txt
      ```
    - Initialize the database (if not already initialized):
      ```sh
      python manage.py db init
      python manage.py db migrate
      python manage.py db upgrade
      ```

3. **Set up the frontend**:
    - Navigate to the `my-project` directory:
      ```sh
      cd my-project
      ```
    - Ensure you have Node.js and npm installed.
    - Install the required packages:
      ```sh
      npm install
      ```
    - Start the Vue.js development server:
      ```sh
      npm run serve
      ```

4. **Run the backend server**:
    - From the project root directory:
      ```sh
      python app.py
      ```

## Usage

1. **Open the application**:
   - Go to `http://localhost:8080` in your web browser.

2. **Register a new user**:
   - Navigate to the Register page and create a new account.

3. **Login**:
   - Login with your registered email and password.

4. **Set Budget and Computer Type**:
   - After logging in, set your budget and preferred computer type.

5. **Choose Components**:
   - Start by selecting a CPU, then proceed to select other components ensuring compatibility.

6. **Finalize Selection**:
   - Review the selected components and see the total price.
   - Get recommendations for better components within your remaining budget.

## API Endpoints

- `POST /register`: Register a new user
- `POST /login`: User login
- `POST /set_budget_and_type`: Set user's budget and computer type
- `GET /get_cpu_options`: Get suitable CPU options
- `POST /select_cpu/<cpu_id>`: Select a CPU
- `GET /get_mb_options/<cpu_id>`: Get suitable motherboard options
- `POST /select_mb/<mb_id>`: Select a motherboard
- `GET /get_ram_options/<mb_id>`: Get suitable RAM options
- `POST /select_ram/<ram_id>`: Select RAM
- `GET /get_ssd_options`: Get suitable SSD options
- `POST /select_ssd/<ssd_id>`: Select SSD
- `GET /get_hdd_options`: Get suitable HDD options
- `POST /select_hdd/<hdd_id>`: Select HDD
- `GET /get_gpu_options`: Get suitable GPU options
- `POST /select_gpu/<gpu_id>`: Select GPU
- `GET /get_psu_options`: Get suitable PSU options
- `POST /select_psu/<psu_id>`: Select PSU
- `GET /get_chassis_options/<mb_id>/<gpu_id>`: Get suitable chassis options
- `POST /select_chassis/<chassis_id>`: Select chassis
- `POST /finalize_selection`: Finalize component selection
- `GET /recommend_gpu`: Get recommendations for a better GPU

## Technologies Used

- **Backend**: Flask, SQLAlchemy, SQLite, Flask-JWT-Extended, Flask-CORS
- **Frontend**: Vue.js, Vue Router, Axios
- **Other Tools**: Python, Node.js, npm

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.
