# data-business-product-management
Management of a business with physical products. Allows to view, and modify inventory, and track progress.

It includes two distinct versions of the code to showcase progression in programming and data processing skills—from an early university version to an improved version using more advanced techniques. Versions: "v1-original" (2020 version), and "v2-upgrade" (2025 version).

Python 3.11.9 64-bit was used. Previous versions might work.
---
## 🔹 Project Description

The goal of this project is to read, modify, and extract statistics from a local `.csv` database of an inventory of a business. The project allows:

- Reading the CSV file and displaying inventory
- Modifying the inventory: price, quantities, products avaiable
- Generating receipt.
- Log in via an user and password.
- Creation of new users.

---

## 🔸 Versions

### `v1-original/`
Developed during my first year of university. It uses basic file I/O and manual data parsing techniques.

### `v2-upgrade/`
An upgrade from the original code built from scratch.

- Instead of .csv, it uses SQLite for database management.
- For users, passwords pass through bcrypt. Given the nature of the project, the use of argon2id or scrypt isnt deemed necessary.
- A GUI is implemented, it changes according to the role of the user who logged in.
- Selling products generates a receipt in .txt.
- A graph of revenue per day is shown in statistics.

---

## 📝 Requirements

Python 3.11.9 is required. Previous versions might work for the "v1-original/" version.
libraries: tkinter, pathlib, pandas, and tkcalendar.

Copy .env.example to your .env
cp .env.example .env
