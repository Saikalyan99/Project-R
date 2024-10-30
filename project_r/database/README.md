# Database Setup Instructions

## Introduction
This guide is to help new users setup a database for 'ProjectR.' Following this guide should allow you to easily get setup and use the database.

## MySQL Installation
To install MySQL, open server_setup.sh in your favorite text editor and use the commands listed there to setup and install. I am not sure if you can 'just run' the file since there are SQL instructions in there and I don't know how Bash will handle it. Consider that untested.

## Python Environment Setup
Next you'll want to prepare your Python environment. It is advised to setup a virtual python environment. The package is called "venv" without the quotes. In your environment, you'll need to install NumPy, SQLAlchemy, and the MySQL Connector for Python.

`pip install numpy`
`pip install sqlalchemy`
`pip install mysql-connector-python`

## Users Setup
We're gonna log into MySQL with the root to setup users. Once you've logged in, open the database_setup.sql file in a text editor then copy and paste the "Create Users" section of the document. Pay attention to the comment below the section to make sure you're able to use your new user once you login with it.

## Database Creation & Imports
We're on the last leg of our journey. Before we can put any data into the database, we have to have a database to put information into! This is separate from setting up MySQL. MySQL is the server that hosts databases. We must create a database, put tables in, then insert information into those tables.

Use Python to run the database_setup.py file. It should create our database and tables. Now, don't get rid of this file since it's a dependency for the import script.

To import data, using Python run the database_import.py file and pass the JSON file you want to import as an argument. Your command might look something like this if you're using the testing file on hand:
`python database_import.py restaurants.json`

## Checking Your Work
After you've run that script, feel free to login to MySQL and check the database to see if everything went in. Here's the commands I used to see some of the information.
`USE ProjectR;`
`SELECT id,name,rating,zip from stores;`
`SELECT * from tags;`
`SELECT * from store_tags;`

I also like this next command. It lets you see every tag association with a store:
```
SELECT S.name AS Store, T.name AS Tag
FROM stores S
JOIN store_tags ST ON S.id = ST.storeid
JOIN tags T ON T.id = ST.tagid
ORDER BY S.id;
```

## Conclusion
Everything should now be setup and ready for integration into whatever. If you followed the guide to completion, you should even have test data to work with. If you have any question or issues, please reach out to Exypnos64.