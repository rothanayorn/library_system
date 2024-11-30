. Library system management 
The Library Management System is a software solution designed to simplify and streamline library operations, providing an efficient way to manage book inventories, track borrowing activities, and ensure easy access for users like librarians
.Project Overview
It is a Python-based desktop application designed to facilitate and automate library operations. It helps users organize books, store book data, and note down available books.
.Problem Addressed
-Inefficient Manual Processes
-Difficulty in Tracking Book Inventory
-Lack of Insights for Decision-Making
.Solutions
- The system automates these operations, ensuring accurate, fast, and efficient record-keeping.
- The system maintains a real-time inventory with updated book statuses, making it easy to track availability.
- The system can be extended to generate usage reports and analytics, aiding better resource planning and decision-making.
.Current Progress
1. Problem Analysis
   By addressing these issues, the Library Management System not only improves operational efficiency but also enhances the overall experience for librarians and students alike.
2. Design
   Using Tkinter GUI, the platform feature
   - A clean, user-friendly interface
   - Simple navigation for customization.
3. Implementation
   Key Features include:
   - user interface
   - book inventory
4. Testing
   - Through testing for a smooth transition
   - Database integration for accurate data
5. Development
   This application is still in development phase:
   -both the user and librarian can access
   -improve UI
.Feature:
-Book Inventory System
.Add, delete, and update book details.
.Maintain book availability status (Available/Issued).
-Borrow/Return Tracking
.Logs the lending and returning of books, reducing the risk of misplaced item
-Database Storage
.All records are stored in an SQLite database, providing reliability and easy data retrieval.
-User-Friendly Interface
.A clean, responsive GUI built with tkinter makes the system accessible to users with minimal training.

. Expected page 
One page is divided into 2 sections for adding or clearing book and book inventory.
.Database 
This system uses SQLite with SQLite viewer extension in vs code.
.Tool
-Language: Python 
-Framework: Tkinter
_Database: SQLite
. Development Status
The application is functional but needs more improvement
-User log-in
-Enhanced UI design
-Localization for the Khmer language
. How to run the code
Install library
pip install Tkinter
pip install sqlite
Download and copy code to vs code 
.How it works
after running the code, the librarian can add books to the book inventory. For adding a book include the book name, Book ID, Author name, and Status of the book. In book inventory, librarians can delete records, Delete full inventory, update book details, and change book availability.
