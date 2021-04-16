# Instructions for Running the Application

The CLI is designed to access a MySQL database running inside a Docker container. The two main stages of project setup are creating the DB and connecting it to the CLI.

- Run `docker compose up --detach` in the directory which contains the included `docker-compose.yml` file.
	> This sets up both MySQL and the virtual network that the CLI will use to communicate with the DB. The most important part of this is the port mapping; the CLI is set up to query port 3307; if you have an existing container you're building the DB inside of, simply edit line 158 of the CLI to reflect the port mapping on your system.
- Open a bash session once the container is up. Navigate to `/var/lib/mysql-files/Database`, create a database called `Cars` using `create database Cars; use Cars;` and run `source createDb.sql;` in the MySQL CLI.
	> If your privileged directory is in another path, navigate there instead. The path is only important for running `source createDb.sql;` without getting complaints from MySQL.
- Once the database is built, run the following two commands:
		- `CREATE USER 'admin'@'%' IDENTIFIED BY 'password';`
		- `GRANT ALL PRIVILEGES ON Cars.* TO 'admin'@'%';`
- Outside of the container, install the Python packages needed by the CLI (described at the top of the `Cli.py` file).
- At this point, the CLI should be able to be run using `python Cli.py` on a Windows machine or `python3 Cli.py` in a Unix environment. 


