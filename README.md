DEEL AI Transaction System
A complete web-based transaction management system with AI-powered name matching and transaction analysis.

Overview
The DEEL AI Transaction System is a Streamlit web application that helps manage financial transactions and user data. It includes intelligent features like:

AI-powered name extraction from transaction descriptions

Fuzzy matching to find similar users

Transaction similarity search

Full CRUD operations for transactions and users

Features
🎯 Core Functions
Find Matching Users - Extract names from transaction descriptions and match with existing users

Find Similar Transactions - Search for transactions similar to a query

Add/Delete Transactions - Full transaction management

Add/Delete Users - User data management

View Data - Browse all transactions and users

Statistics - System analytics and insights

🔧 Technical Features: 
Real-time data processing

JSON export for all operations

CSV data persistence

Responsive web interface

Visual match scoring

Embedding-based similarity search


How to Use
1. Dashboard
View system overview

See recent transactions

Check total amounts and statistics

2. Find Matching Users (Task 1)
Option A: Search by Transaction ID

Enter a transaction ID

System extracts name from description

Shows matching users with similarity scores

Option B: Search by Description

Paste transaction description

Get matching users instantly

3. Find Similar Transactions (Task 2)
Enter search text (e.g., "From Liam Johnson")

Adjust similarity threshold

View similar transactions with embeddings

4. Add New Transaction
Enter amount and description

System automatically extracts names

Shows matching users for verification

5. Add New User
Enter full name

System generates unique ID

User added to database

6. Delete Operations
Search transactions/users by ID or description

Delete with confirmation

View deletion results in JSON

7. View Data
Browse all transactions with search

View all users

Export data as JSON

8. Statistics
Transaction analytics

User statistics

Type distribution

9. Demo Mode
Test key features

See example outputs

Understand system capabilities

Name Matching Logic
The system uses intelligent name extraction:

Pattern Matching - Extracts names using regex patterns

Similarity Scoring - Compares extracted names with user database

Fuzzy Matching - Handles variations and misspellings

Score Calculation - Combines word and character similarity

JSON Output
Every operation provides JSON output:

Downloadable JSON files

Structured response data

Complete operation details

Match scores and metadata
