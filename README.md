# Restaurant Booking Lab Backend

This is the backend component of the Restaurant Booking Lab project. It is built using Django and Django Rest Framework to provide the necessary API endpoints for managing restaurants and booking tickets.

## Prerequisites

- Python 3.11

## Installation

1. Clone this repository to your local machine:
   ```bash
    git clone https://github.com/sergiovl219/restaurantbookinglab-backend.git
   ```

2. Change to the project directory:
    ```bash
   cd restaurantbookinglab-backend
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv restaurant_booking_venv
    source restaurant_booking_venv/bin/activate # On Windows, use: venv\Scripts\activate
    ```

4. Install Poetry using pip:
    ```bash
    pip install poetry
    ```

5. Install project dependencies using Poetry:
    ```bash
    poetry install
    ```

6. Migrate the database:
    ```bash
    python manage.py migrate
    ```

7. Start the development server:
    ```bash
    python manage.py runserver
    ```
The backend should now be up and running. You can access the API endpoints at `http://localhost:8000/`.

## Usage

To use this backend component, you can integrate it with your front-end application. The API provides functionality for managing restaurants and booking tickets.

## Swagger Documentation
You can explore the API endpoints and their documentation interactively using Swagger. To access the Swagger UI, open your web browser and go to http://localhost:8000/swagger/.

## Configuration

You can customize the project settings in the `settings.py` file.

## Contributing

If you would like to contribute to this project, please follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact Sergio Vargas at svargas219@gmail.com.

