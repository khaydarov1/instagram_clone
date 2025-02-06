# Instagram Clone

This is a simple Instagram clone built with Django and Django REST framework.

## Features

- User authentication
- Post creation and management
- Commenting on posts
- Liking posts and comments
- Pagination for posts

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/instagram_clone.git
    ```

2. Navigate to the project directory:
    ```sh
    cd instagram_clone
    ```

3. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

5. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Apply migrations:
    ```sh
    python manage.py migrate
    ```

7. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

8. Run the application:
    ```sh
    python manage.py runserver
    ```

## Contributing

Feel free to fork this repository and submit pull requests.

## License

This project is open source and available under the MIT License.