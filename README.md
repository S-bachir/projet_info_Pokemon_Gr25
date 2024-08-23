# Pokemon Game

## Prerequisites

Before launching the application, it is essential to set up the database and install the required packages.

### Package Installation

The application relies on several Python packages listed in the `requirements.txt` file. The application is compatible with Python version 3.6. To install the necessary packages, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Database Setup

The database setup involves executing a series of SQL and Python scripts located in the `bdd` directory. Follow these steps to set up the database:

1. **Step 1:** Execute the `1script_bdd.sql` file.
   - This script sets up the initial database schema, including tables and relationships required by the application.
   - To run it, copy its contents into your SQL query editor and execute it.

2. **Step 2:** Run the `2script_insert_pokemon_ball.py` file.
   - This Python script inserts initial data into the database, specifically the data related to Pokémon and Poké Balls.
   - Run this script in your IDE to populate the database with this essential data.

3. **Step 3:** Execute the `3script_bdd_insert.sql` file.
   - This SQL script inserts additional data into the database, such as more Pokémon entries, item details, and other relevant data.
   - Copy its contents into your SQL query editor and execute it.

   **Important:** Ensure you execute these files in the specified order (1, 2, 3) to properly set up the database.

The class responsible for managing the connection between the application and the database is found in `dao/pool_connection.py`. This file contains all the necessary configuration details for the database connection.

## Running the Application

After setting up the database and installing the required packages, you can launch the application. This can be done either by running the `main.py` file in your IDE or by executing the following command in the terminal, depending on your operating system:

```bash
python3 main.py
```

or

```bash
python.exe main.py
```

## Testing and Documentation

The class used for documentation and unit testing is `PokemonDao`, located in `dao/pokemon_dao.py`. The corresponding test class is found in `test/test_pokemon_dao.py`.

## Acknowledgements

Thank you for your attention and for using this application!
