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

> Note: The project is currently configured to use SQLite as the database for testing and development purposes only. SQLite is not recommended for production environments, and it is advisable to configure a more robust database system for production use. Ensure that you do not upload sensitive information to a SQLite database on a public repository like GitHub.

## Usage

To use this backend component, you can integrate it with your front-end application. The API provides functionality for managing restaurants and booking tickets.

## Swagger Documentation
You can explore the API endpoints and their documentation interactively using Swagger. To access the Swagger UI, open your web browser and go to http://localhost:8000/swagger/.

## Configuration

You can customize the project settings in the `settings.py` file.

## Asynchronous Task Processing with Celery, Redis, and Flower
This project now utilizes Celery, Redis, and Flower to handle asynchronous task processing and monitoring. These tools enhance the performance and scalability of the application by offloading time-consuming operations from the main application thread.

### Celery
Celery is a distributed task queue system that allows tasks to be executed asynchronously. It is used to manage and execute background tasks without blocking the main application.

### Redis
Redis serves as the message broker for Celery, enabling it to distribute tasks across multiple workers. Redis is a high-performance, in-memory data store that efficiently handles task queueing and management.

### Flower
Flower is a real-time web-based monitoring tool for Celery. It provides a web interface for inspecting the status of workers, viewing task progress, and monitoring the execution of asynchronous tasks.

To start using these tools, please follow the instructions provided in the previous section to install and configure them in your project. You can monitor Celery tasks and worker status by accessing the Flower web interface at http://localhost:5555 after starting Flower.


## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact Sergio Vargas at svargas219@gmail.com.
