# NEScafeBot Project Documentation

## Overview

NEScafeBot is a Telegram bot designed to facilitate random coffee meetups for students of the New Economic School (NES).  

The bot matches users for coffee meetups while respecting their blacklists and availability. Users can manage their profiles, activate or deactivate their participation in random coffee, and maintain a blacklist of people they don't want to meet.  

The bot is built using **Python, MongoDB, Redis, Docker**, with **asynchronous** message handling powered by the aiogram framework.

## Project Structure

The project follows a structured organization to separate different functionalities like configurations, database interactions, and message handling. Below is an outline of the project’s main directories and files.

### Root Directory

* **compose.yaml**: This file defines the Docker Compose setup for the project. It configures the services needed to run the bot, including the bot service itself, MongoDB for database storage, and Redis for caching. It also sets up the necessary network connections and environment variables;  

* **Dockerfile.py**: This is the Dockerfile that builds the container for running the bot. It sets up the Python environment, installs necessary dependencies, and copies the required files into the container. It ensures that the bot runs in a clean, reproducible environment;  

* **instructions.md**: This file contains instructions on how to launch the bot, including how to set up the environment variables, build the Docker image, and start the bot using Docker Compose. It also includes troubleshooting steps and instructions for using tmux to manage the bot process inside the container;  

* **README.md**: This is a brief introductory file that points users to the instructions.md for detailed setup and usage information;  

* **requirements.txt**: This file lists all the Python dependencies required to run the bot, including libraries like aiogram, pydantic, pandas, motor, and aiosmtplib. These dependencies are installed in the Docker container during the build process;  

### bot

This is the main directory for the bot's source code. It contains several subdirectories for configurations, database operations, and handlers, as well as the entry point for running the bot.

* **start_bot.py**: This is the entry point for running the bot. It initializes the bot, sets up the database connection, registers handlers for user and admin interactions, and starts polling for messages. It also handles bot startup and shutdown events, ensuring that resources are properly initialized and cleaned up.

* **create_bot.py**: This file initializes the bot with the token stored in the environment

#### bot/configs

This directory handles all configurations related to environment variables, logging, and administrative settings.

* **env_reader.py**: Responsible for reading environment variables from a .env file, which contains sensitive information such as the Telegram bot token and MongoDB credentials. It uses the pydantic library to securely manage these variables.

* **logs.py**: Sets up the logging system for the bot, ensuring that both console and file logs are managed efficiently. It creates log files, filters certain log levels, and uses colored logs for easier readability in the console.

* **selected_ids.py**: Contains a list of user IDs that are designated as administrators of the bot. These admins have special privileges and can use admin-only commands.

#### bot/db

This directory handles database connections and operations. The bot uses MongoDB to store user profiles, messages, and matching results.

* **connect.py**: Establishes the MongoDB connection using motor, an asynchronous MongoDB driver. It sets up collections for users, messages, and match results and provides functions to retrieve and manage these collections.

* **users.py, messages.py, user_profile.py**: These files contain functions for interacting with specific MongoDB collections. They handle operations such as finding users, updating profiles, retrieving messages, and managing user data.

* **conversion.py**: Contains utility functions for converting data between different formats, making it easier to handle and store in the database.

### bot/handlers

The handlers directory is the core of the bot's interaction logic. It contains subdirectories and files for handling different types of user interactions, including admin commands, client (user) commands, and common utilities shared by both.

#### bot/handlers/admin

This subdirectory contains handlers that are accessible only by the bot's administrators. Admins can manage users, trigger matchings, and review logs.

* **admin.py**: Registers all the admin handlers. This file imports various commands related to admin functionality and sets up routers for admin-only actions like triggering the matching process.

* **admin_filter.py**: Defines a filter to restrict certain commands to admin users only, based on their user IDs.

* **send_on.py**: Handles notifications to admins when the bot starts or shuts down, including sending logs to admins during shutdown.

* **interactive.py**, non_interactive.py: These files define interactive and non-interactive admin commands. Interactive commands require user input, while non-interactive ones run independently, such as fetching logs or sending messages.

* **block_matching.py**: Allows admins to block or unblock users from participating in the matching process. This file handles the logic for adding or removing users from the blocked list.

* **assignment.py, emojis.py, save.py, sending.py**: These files handle the matching algorithm, emoji assignment, saving match results to the database, and sending notifications to users about their matches.

#### bot/handlers/client

The client subdirectory contains handlers for regular users. These handlers manage user interactions such as registration, profile updates, and controlling whether the user participates in matchings.

* **client.py**: Registers all the client-related handlers. It imports commands related to user functionality like starting the bot, managing the blacklist, checking active status, and accessing help.

* **email.py**: Manages email-related functionality, including sending verification emails during registration and checking the status of email accounts used by the bot. It uses the aiosmtplib library for asynchronous email sending.

* **menu.py**: Defines the menu commands that users can access when interacting with the bot, such as /start, /blacklist, /active, /help, and /cancel.

* **contains.py, keyboard.py**: Utility files for handling user input validation and creating reply keyboards that guide users through various options in the bot.

#### bot/handlers/common

This subdirectory contains shared utilities and handlers that are used across both admin and client functionalities.

* **addressing_errors.py**: Provides error-handling utilities that log exceptions and notify admins and users when an error occurs. It ensures that unexpected issues are managed gracefully.

* **checks.py**: Contains decorators that validate user input, such as checking if the user has completed their profile or if a message is in the correct format.

* **common_handlers.py**: Registers common handlers that are used across the bot, such as handling cancellation commands or responding to unrecognized messages.

* **pending.py**: Handles pending updates by notifying users if the bot was inactive and asking them to resend their messages.

* **cancel.py, zero_message.py**: These files define handlers for commands that allow users to cancel ongoing processes or handle unrecognized messages when no specific state is active.
