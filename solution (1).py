"""
Python EDA + SQLite3 Assignment - Full Solution
Dataset: EDA_SQLite_Employee_200.csv
"""

import pandas as pd
import numpy as np
import sqlite3

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)


def section(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


# =========================================================================
# PART 1: LOAD AND INSPECT DATA
# =========================================================================
section("PART 1: LOAD AND INSPECT DATA")

# 1-2. Import libraries (pandas, numpy, sqlite3) already imported above; read CSV
df = pd.read_csv("EDA_SQLite_Employee_200.csv")

# 3. head(), tail(), sample(10)
print("\n--- head() ---")
print(df.head())
print("\n--- tail() ---")
print(df.tail())
print("\n--- sample(10) ---")
print(df.sample(10, random_state=1))

# 4. shape, columns, dtypes
print("\n--- shape ---")
print(df.shape)
print("\n--- columns ---")
print(list(df.columns))
print("\n--- dtypes ---")
print(df.dtypes)

# 5. info(), describe(include='all')
print("\n--- info() ---")
df.info()
print("\n--- describe(include='all') ---")
print(df.describe(include="all"))

# 6. Set EmployeeID as index
df = df.set_index("EmployeeID")
print("\n--- After set_index('EmployeeID') ---")
print(df.head())


# =========================================================================
# PART 2: DATA CLEANING
# =========================================================================
section("PART 2: DATA CLEANING")

# 7. Missing values per column
print("\n--- Missing values per column (before cleaning) ---")
print(df.isnull().sum())

# 8. Fill missing Age with median
df["Age"] = df["Age"].fillna(df["Age"].median())

# 9. Fill missing Salary with mean
df["Salary"] = df["Salary"].fillna(df["Salary"].mean())

# 10. Fill missing ExperienceYears with median
df["ExperienceYears"] = df["ExperienceYears"].fillna(df["ExperienceYears"].median())

# 11. Fill missing PerformanceScore with median
df["PerformanceScore"] = df["PerformanceScore"].fillna(df["PerformanceScore"].median())

# 12. Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"\nRemoved {before - len(df)} duplicate rows (from {before} to {len(df)})")

# 13. Rename PerformanceScore -> Rating
df = df.rename(columns={"PerformanceScore": "Rating"})

# 14. Convert JoinDate to datetime
df["JoinDate"] = pd.to_datetime(df["JoinDate"])

# 15. Verify no missing values remain
print("\n--- Missing values per column (after cleaning) ---")
print(df.isnull().sum())


# =========================================================================
# PART 3: DATA MANIPULATION
# =========================================================================
section("PART 3: DATA MANIPULATION")

# 16. Bonus = Salary * 0.10
df["Bonus"] = df["Salary"] * 0.10

# 17. TotalSalary = Salary + Bonus
df["TotalSalary"] = df["Salary"] + df["Bonus"]

# 18. SeniorEmployee Yes/No if ExperienceYears >= 5
df["SeniorEmployee"] = np.where(df["ExperienceYears"] >= 5, "Yes", "No")

print("\n--- New columns preview ---")
print(df[["Salary", "Bonus", "TotalSalary", "ExperienceYears", "SeniorEmployee"]].head())

# 19. Filter IT employees
it_employees = df[df["Department"] == "IT"]
print(f"\n--- IT employees: {len(it_employees)} rows ---")
print(it_employees.head())

# 20. Filter Salary > 10000
high_salary = df[df["Salary"] > 10000]
print(f"\n--- Salary > 10000: {len(high_salary)} rows ---")
print(high_salary.head())

# 21. Filter employees from Cairo with Rating >= 4
cairo_top = df[(df["City"] == "Cairo") & (df["Rating"] >= 4)]
print(f"\n--- Cairo & Rating>=4: {len(cairo_top)} rows ---")
print(cairo_top.head())

# 22. Sort by Salary descending
by_salary_desc = df.sort_values("Salary", ascending=False)
print("\n--- Sorted by Salary desc (top 5) ---")
print(by_salary_desc.head())

# 23. Sort by JoinDate ascending
by_join_asc = df.sort_values("JoinDate", ascending=True)
print("\n--- Sorted by JoinDate asc (top 5) ---")
print(by_join_asc.head())

# 24. Top 10 highest salaries
top10_salary = df.sort_values("Salary", ascending=False).head(10)
print("\n--- Top 10 highest salaries ---")
print(top10_salary[["Name", "Department", "Salary"]])


# =========================================================================
# PART 4: AGGREGATION
# =========================================================================
section("PART 4: AGGREGATION")

# 25. Department-wise average salary
print("\n--- Average salary by department ---")
print(df.groupby("Department")["Salary"].mean().round(2))

# 26. Department-wise max/min salary
print("\n--- Max/Min salary by department ---")
print(df.groupby("Department")["Salary"].agg(["max", "min"]))

# 27. Count employees in each city
print("\n--- Employee count by city ---")
print(df.groupby("City").size())

# 28. Average rating by department
print("\n--- Average rating by department ---")
print(df.groupby("Department")["Rating"].mean().round(2))

# 29. Number of males and females
print("\n--- Gender counts ---")
print(df["Gender"].value_counts())

# 30. Average experience by department
print("\n--- Average experience by department ---")
print(df.groupby("Department")["ExperienceYears"].mean().round(2))

# 31. Highest paid employee in each department
print("\n--- Highest paid employee per department ---")
idx = df.groupby("Department")["Salary"].idxmax()
print(df.loc[idx, ["Name", "Department", "Salary"]])


# =========================================================================
# PART 5: SQLITE3
# =========================================================================
section("PART 5: SQLITE3")

# 32. Create employee.db
conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# 33. Create employees table
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("""
CREATE TABLE employees (
    EmployeeID INTEGER PRIMARY KEY,
    Name TEXT,
    Age REAL,
    Department TEXT,
    City TEXT,
    Gender TEXT,
    Salary REAL,
    ExperienceYears REAL,
    Rating REAL,
    JoinDate TEXT,
    Bonus REAL,
    TotalSalary REAL,
    SeniorEmployee TEXT
)
""")
conn.commit()

# 34. Insert cleaned DataFrame using to_sql()
df_sql = df.reset_index()  # bring EmployeeID back as a column
df_sql["JoinDate"] = df_sql["JoinDate"].dt.strftime("%Y-%m-%d")
df_sql.to_sql("employees", conn, if_exists="replace", index=False)

# 35. Read all records
all_records = pd.read_sql("SELECT * FROM employees", conn)
print(f"\n--- All records read back from SQLite: {len(all_records)} rows ---")

# 36. Display first 10 rows from SQLite
print("\n--- First 10 rows from SQLite ---")
print(pd.read_sql("SELECT * FROM employees LIMIT 10", conn))

# 37. Count total employees
total_count = pd.read_sql("SELECT COUNT(*) AS TotalEmployees FROM employees", conn)
print("\n--- Total employees ---")
print(total_count)

# 38. Average salary
avg_salary = pd.read_sql("SELECT AVG(Salary) AS AvgSalary FROM employees", conn)
print("\n--- Average salary ---")
print(avg_salary)

# 39. Maximum salary
max_salary = pd.read_sql("SELECT MAX(Salary) AS MaxSalary FROM employees", conn)
print("\n--- Maximum salary ---")
print(max_salary)

# 40. Employees with Salary > 10000
print("\n--- Employees with Salary > 10000 (first 10) ---")
print(pd.read_sql("SELECT * FROM employees WHERE Salary > 10000 LIMIT 10", conn))

# 41. Employees in IT
print("\n--- Employees in IT (first 10) ---")
print(pd.read_sql("SELECT * FROM employees WHERE Department = 'IT' LIMIT 10", conn))

# 42. Group by Department, AVG(Salary)
print("\n--- AVG(Salary) grouped by Department ---")
print(pd.read_sql(
    "SELECT Department, AVG(Salary) AS AvgSalary FROM employees GROUP BY Department", conn
))

# 43. Update Salary = Salary*1.05 where Department='HR'
cursor.execute("UPDATE employees SET Salary = Salary * 1.05 WHERE Department = 'HR'")
conn.commit()
print(f"\nUpdated HR salaries (+5%): {cursor.rowcount} rows affected")

# 44. Delete employees where Rating < 3.0
cursor.execute("DELETE FROM employees WHERE Rating < 3.0")
conn.commit()
print(f"Deleted employees with Rating < 3.0: {cursor.rowcount} rows affected")

# 45. Add a new employee using SQL INSERT
cursor.execute("""
INSERT INTO employees (EmployeeID, Name, Age, Department, City, Gender, Salary,
                        ExperienceYears, Rating, JoinDate, Bonus, TotalSalary, SeniorEmployee)
VALUES (9999, 'New Employee', 30, 'IT', 'Cairo', 'Male', 12000, 3, 4.5,
        '2024-01-15', 1200, 13200, 'No')
""")
conn.commit()
print("\nInserted new employee with EmployeeID 9999")

# 46. Search employee by EmployeeID
print("\n--- Search EmployeeID = 9999 ---")
print(pd.read_sql("SELECT * FROM employees WHERE EmployeeID = 9999", conn))

# 47. Top 5 salaries
print("\n--- Top 5 salaries ---")
print(pd.read_sql("SELECT Name, Department, Salary FROM employees ORDER BY Salary DESC LIMIT 5", conn))

# 48. Order by JoinDate DESC
print("\n--- Ordered by JoinDate DESC (first 5) ---")
print(pd.read_sql("SELECT Name, JoinDate FROM employees ORDER BY JoinDate DESC LIMIT 5", conn))

# 49. Export final table back to CSV
final_table = pd.read_sql("SELECT * FROM employees", conn)
final_table.to_csv("employees_final.csv", index=False)
print(f"\nExported final table ({len(final_table)} rows) to employees_final.csv")

# 50. Close the database connection
conn.close()
print("\nDatabase connection closed.")


# =========================================================================
# BONUS CHALLENGES: reusable functions + exception handling
# =========================================================================
section("BONUS CHALLENGES")


def load_data(path):
    """Load a CSV file into a DataFrame, raising a friendly error if it fails."""
    try:
        data = pd.read_csv(path)
        print(f"[load_data] Loaded {len(data)} rows from '{path}'")
        return data
    except FileNotFoundError:
        print(f"[load_data] ERROR: File not found -> {path}")
        return None
    except Exception as e:
        print(f"[load_data] ERROR: Could not load '{path}': {e}")
        return None


def clean_data(data):
    """Clean a raw employee DataFrame: fill missing values, dedupe, rename, cast dates."""
    try:
        data = data.copy()
        data["Age"] = data["Age"].fillna(data["Age"].median())
        data["Salary"] = data["Salary"].fillna(data["Salary"].mean())
        data["ExperienceYears"] = data["ExperienceYears"].fillna(data["ExperienceYears"].median())
        data["PerformanceScore"] = data["PerformanceScore"].fillna(data["PerformanceScore"].median())
        data = data.drop_duplicates()
        data = data.rename(columns={"PerformanceScore": "Rating"})
        data["JoinDate"] = pd.to_datetime(data["JoinDate"])
        print(f"[clean_data] Cleaned dataset now has {len(data)} rows and "
              f"{data.isnull().sum().sum()} missing values")
        return data
    except Exception as e:
        print(f"[clean_data] ERROR while cleaning data: {e}")
        return data


def save_to_sqlite(data, db_path, table_name="employees"):
    """Save a DataFrame to a SQLite database, handling errors gracefully."""
    try:
        conn_local = sqlite3.connect(db_path)
        data_to_save = data.reset_index() if data.index.name == "EmployeeID" else data.copy()
        if "JoinDate" in data_to_save.columns and pd.api.types.is_datetime64_any_dtype(data_to_save["JoinDate"]):
            data_to_save["JoinDate"] = data_to_save["JoinDate"].dt.strftime("%Y-%m-%d")
        data_to_save.to_sql(table_name, conn_local, if_exists="replace", index=False)
        conn_local.close()
        print(f"[save_to_sqlite] Saved {len(data_to_save)} rows to '{db_path}' (table: {table_name})")
    except Exception as e:
        print(f"[save_to_sqlite] ERROR saving to SQLite: {e}")


# Demonstrate the reusable functions end-to-end
raw = load_data("EDA_SQLite_Employee_200.csv")
if raw is not None:
    cleaned = clean_data(raw)
    save_to_sqlite(cleaned, "employee_bonus.db")

# Demonstrate exception handling on a missing file
_ = load_data("this_file_does_not_exist.csv")

print("\nAll 50 tasks + bonus challenges completed successfully.")
