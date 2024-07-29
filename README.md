**REDBUS Data Scraping with Selenium & Dynamic Filtering using STREAMLIT**

**Introduction:**

redBus.com is an online portal for booking bus tickets for travel all over India. The company had its strange beginning some time in 2005. Its founders, all from BITS Pilani, one of India’s top engineering colleges, were working then with different IT MNCs like IBM, Texas Instruments and Honeywell in Bangalore.

redBus is an Indian online bus ticket booking company that provides bus ticket booking through its website and iOS and Android mobile apps. redBus is a consumer-facing travel brand enabling customers to buy tickets on the internet and mobile. The company partners with bus operators and enables travellers to book inter-city bus tickets and hire buses.

It is headquartered in Bangalore and works like a hub, acting as a medium for a network of more than 3500 bus operators, across the countries of India, Malaysia, Indonesia, Singapore, Peru, and Colombia. It claims to have registered over 180 million trips, with a customer base of over 20 million. In 2018, the company achieved a GMV of ₹50 billion (equivalent to ₹67 billion or US$800 million in 2023), with a 70% share in the Indian online bus ticketing segment.

**Business Use Cases:**

The solution can be applied to various business scenarios including:

- **Travel Aggregators:** Providing real-time bus schedules and seat availability for customers.
- **Market Analysis:** Analyzing travel patterns and preferences for market research.
- **Customer Service:** Enhancing user experience by offering customized travel options based on data insights.

**Competitor Analysis:** Comparing pricing and service levels with competitors.

**Problem Statement:**

The "redBus Data Scraping and Filtering with STREAMLIT Application" aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from redBus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.

**Packages Used:**

- **Selenium:**

Selenium Python bindings provides a simple API to write functional/acceptance tests using Selenium WebDriver. Through Selenium Python API you can access all functionalities of Selenium WebDriver in an intuitive way.

Selenium Python bindings provide a convenient API to access Selenium WebDrivers like Firefox, Ie, Chrome, Remote etc. To know more Click here <https://selenium-python.readthedocs.io/>

- **Streamlit:**

  ` `Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required.

  `  `As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab

  `   `in your default web browser. The app is your canvas, where you'll draw charts, text, widgets, tables, and more.

  `   `To know more about **Streamlit**. Click here <https://docs.streamlit.io/>

- **Pandas:**

  Pandas is a powerful and open-source Python library. The Pandas library is used for data manipulation and analysis.

  Pandas consist of data structures and functions to perform efficient operations on data. pandas is a [Python](https://www.python.org/) package                                   providing fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, **real-world** data analysis in Python. Additionally, it has the broader goal of becoming **the most powerful and flexible open source data analysis/manipulation tool available in any language**.

  To know more about **Pandas.** Click here [https://pandas.pydata.org/docs/                                ](https://pandas.pydata.org/docs/%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20)  

- **MySQL:**

  `              `MySQL, the most popular Open-Source SQL database management system, is developed, distributed, and supported by 

  `              `Oracle Corporation. 

  `               `To know more about **MySQL**. Click here <https://dev.mysql.com/doc/refman/9.0/en/>

- **Streamlit-Option-Menu:**
  **
  `                                         `Streamlit-option-menu is a simple Streamlit component that allows users to select a single item from a

  `                                         `list of options in a menu.

  `                                         `To know more about Streamlit-Option-Menu. Click here [https://discuss.streamlit.io/t/streamlit-option-                                             menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514](https://discuss.streamlit.io/t/streamlit-option-%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514)

**Install Packages:**

- **Selenium** – pip install selenium
- **Pandas** – pip install pandas
- **Streamlit** – pip install streamlit
- **MySQL** **Connector**– pip install mysql-connector-python
- **Streamlit-Option-Menu** – pip install streamlit-option-menu

**This project contains two files**

1) RedBus\_DataScrape.py
1) RedBus\_SQL\_DataBaseHandle.py
1) StreamLit\_UI.py

**1) RedBus\_DataScrape.py**

This Python script uses the Selenium library to automate web scraping from the Redbus website and process the data using pandas. The script follows these main steps:

1. **Import Libraries**: Necessary packages for web scraping, database operations, and data handling are imported.
1. **HomePage\_driver Function**: Opens the Redbus website, maximizes the browser window, and scrolls down the page to make elements visible.
1. **StatesPage\_Link Function**: Navigates to the provided state link, extracts the state names and their respective links, and stores them in lists.
1. **BusRoutes\_link Function**: For each state link, navigates to the state page, extracts bus route links from all available pages, and compiles a list of these routes along with state names.
1. **BUSDETAILS Function**: Iterates through the bus route links, navigates to each route page, extracts detailed bus information (such as bus names, types, departure times, travel durations, ratings, prices, and seat availability), and stores these details in a list.
1. **Closingdriver Function**: Closes the browser window to end the session.
1. **Main Script Execution**: Initializes the Chrome driver and calls the functions in sequence:
   1. Opens the Redbus home page.
   1. Extracts state page links and names, and saves them to a CSV file.
   1. Extracts bus route links and saves them to another CSV file.
   1. (Commented out) Extracts detailed bus information and saves it to a CSV file.
   1. Closes the browser.

**2) RedBus\_SQL\_DataBaseHandling.py**

- This Python script facilitates the extraction, transformation, and loading (ETL) of bus route and bus details data into a MySQL database. It begins by importing the necessary modules, including mysql.connector for database operations and pandas for data manipulation. The script defines several functions for different stages of the ETL process:
- **SQL\_Connection**: Establishes a connection to a MySQL database using provided configuration details and returns the connection and cursor objects.
- **ReadData\_From\_Excel**: Reads data from a CSV file and returns it as a pandas DataFrame. It includes error handling to catch issues that might occur during file reading.
- **Create\_Table**: Executes a SQL query to create a table in the MySQL database. It includes error handling to manage exceptions during table creation.
- **Insert\_Table**: Inserts data into a specified MySQL table using a provided query and data. It commits the changes to the database and handles any insertion errors.
- **Close\_Connection**: Closes the database connection and cursor, with error handling to ensure proper closure even if issues arise.
- The script's main execution sequence involves:
- Establishing a connection to the MySQL database.
- Reading bus route links and bus details from CSV files (route\_data.csv and bus\_data.csv, respectively) into pandas DataFrames.
- Filling missing star ratings in the bus details DataFrame with 0.
- Creating the BusRoutesAndLinks and BusDetails tables in the MySQL database if they do not already exist. The BusDetails table includes a foreign key reference to BusRoutesAndLinks.
- Inserting the bus route links and bus details data into their respective tables using the INSERT statements with ON DUPLICATE KEY UPDATE to handle duplicates.
- Closing the database connection and cursor to clean up resources.
- This script ensures that data is accurately transferred from CSV files to a MySQL database, with robust error handling at each step to manage potential issues..

**3) RedBus\_SQL\_DataBaseHandling.py**

This Streamlit application enables users to search and book bus tickets using the Redbus platform. It integrates with a MySQL database to fetch and display bus information based on user-selected filters.

The script begins by importing necessary modules, including Streamlit for the web interface, MySQL connector for database interaction, pandas for data manipulation, and time for delays.

A configuration function sets up database connection parameters, while the connection function establishes a connection to the MySQL database using these parameters. If the connection fails, appropriate error messages are displayed.

Two helper functions are defined for database interaction:

- fetch\_distinct\_value executes queries to retrieve distinct values from the database (e.g., bus types, states).
- fetch\_filtered\_value executes queries to retrieve filtered bus data based on user criteria, returning the data as a pandas DataFrame. It also converts 0.0 star ratings to "NA".

The Streamlit page is configured with a title, icon, and layout. Custom CSS is loaded to enhance the styling of the application.

The sidebar contains an image and filter options for seat type, price range, star rating, and departure time. These options are populated dynamically with data fetched from the database.

The main page layout includes two columns for selecting the state and route. The state dropdown is populated with distinct states, and based on the selected state, the route dropdown is populated with corresponding routes.

When the "Search" button is clicked, a SQL query is constructed based on the selected filters. This query is executed, and the results are displayed in a table. If no buses match the criteria, an appropriate message is shown.

Overall, this application provides a user-friendly interface for searching and booking bus tickets, offering various filters to refine search results and display relevant bus information.

**How to use the application:**

- State and Route Selection: Start by selecting the state you are traveling from. Then choose the specific route you are interested in.
- Seat Type: Use the dropdown to select your preferred type of seat. Whether it's a sleeper, semi-sleeper, or any other type, we have options for you.
- Price Range: Adjust the slider to set your budget. You can filter buses based on your preferred price range.
- Star Rating: Looking for a top-rated bus? Adjust the star rating filter to find buses with the highest ratings.
- Starting Time: Use the slider to choose the departure time that suits you best. Whether you prefer early morning departures or late-night buses.
- After selecting your preferences, simply click on the 'Search' button to view the available options. The results will display here, and you can further refine your choices as needed. 

**How to run the code:**

1) Step 1: Run command “python RedBus\_DataScrape.py” in terminal
1) Step 2: Run command “python RedBus\_SQL\_DataBaseHandle.py” in terminal
1) Step 3: Run command “streamlit run StreamLit\_UI.py” in terminal









