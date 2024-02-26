import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Initialize Faker to generate fake data
faker = Faker()

# Function to generate a random date between two dates


def generate_random_date(start_date, end_date):
    time_between = end_date - start_date
    random_days = random.randint(0, time_between.days)
    return start_date + timedelta(days=random_days)

# Function to assign a random age within a given age range with specified weight


def assign_random_age():
    age_weights = [(20, 10), (25, 75), (30, 10), (35, 2), (40, 2), (50, 1)]
    age = random.choices(*zip(*age_weights))[0]
    return random.randint(age - 4, age)

# Function to assign an age range based on age


def assign_age_range(age):
    if 20 <= age <= 24:
        return "20-24"
    elif 25 <= age <= 29:
        return "25-29"
    elif 30 <= age <= 35:
        return "30-35"
    elif 36 <= age <= 40:
        return "36-40"
    elif 41 <= age <= 50:
        return "41-50"
    else:
        return "51+"

# Function to assign gender based on name with specified weight


def assign_gender(name):
    female_weight = 0.62
    if random.random() < female_weight:
        return "Female"
    else:
        return "Male"


def generate_and_save_transaction_data(filename, num_rows=10000, min_transactions=1, max_transactions=5):
    try:
        # Define start and end dates for transactions
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2024, 12, 31)

        # Initialize dictionaries to track existing Customer_IDs and their associated Customer_Names
        existing_customers = {}
        existing_transaction_ids = set()

        # Generate data for the transaction table
        data = {
            "Transaction_ID": [],
            "Customer_ID": [],
            "Customer_Name": [],
            "Gender": [],
            "Transaction_Date": [],
            "Transaction_Status": [],
            "Quantity": [],
            "Transaction_Amount": [],
            "Product_ID": [],
            "Category_ID": [],
            "Brand_ID": [],
            "Country": [],
        }

        # Calculate the number of customers needed
        num_customers = num_rows // max_transactions + 1

        for _ in range(num_customers):
            customer_name = faker.name()
            birthdate = datetime.today() - timedelta(days=365 * assign_random_age())

            # Check if the customer name already exists in the dictionary
            if customer_name in existing_customers:
                customer_id = existing_customers[customer_name]
                # 25% chance for additional transactions
                if random.random() < 0.25:
                    num_transactions = random.randint(2, 3)
                else:
                    num_transactions = 1
            else:
                # Generate a new unique customer_id if the customer name is new
                customer_id = len(existing_customers) + 90000
                existing_customers[customer_name] = customer_id
                # Most common occurrence: 75% chance for a single transaction
                if random.random() < 0.75:
                    num_transactions = 1
                else:
                    num_transactions = random.randint(2, 3)

            for _ in range(num_transactions):
                transaction_id = len(existing_transaction_ids) + 90000
                transaction_date = generate_random_date(
                    start_date, end_date).strftime('%Y-%m-%d')
                transaction_status = random.choice(
                    ["Paid", "Cancelled", "Refunded"])
                quantity = random.randint(1, 5)
                transaction_amount = round(
                    random.uniform(90, 110) * quantity, 2)
                product_id = random.randint(101, 500)
                category_id = random.randint(1, 28)
                brand_id = random.randint(1, 50)
                country = random.choice(
                    ["France", "Canada", "Germany", "Brazil", "Italy"])

                data["Transaction_ID"].append(transaction_id)
                data["Customer_ID"].append(customer_id)
                data["Customer_Name"].append(customer_name)
                data["Gender"].append(assign_gender(customer_name))
                data["Transaction_Date"].append(transaction_date)
                data["Transaction_Status"].append(transaction_status)
                data["Quantity"].append(quantity)
                data["Transaction_Amount"].append(transaction_amount)
                data["Product_ID"].append(product_id)
                data["Category_ID"].append(category_id)
                data["Brand_ID"].append(brand_id)
                data["Country"].append(country)

                existing_transaction_ids.add(transaction_id)

                num_rows -= 1
                if num_rows == 0:
                    break

            if num_rows == 0:
                break

        # Create a DataFrame
        transaction_df = pd.DataFrame(data)

        # Calculate age based on birthdate
        transaction_df["Age"] = transaction_df["Customer_Name"].apply(
            lambda x: assign_random_age())

        # Assign age range based on age
        transaction_df["Age_Range"] = transaction_df["Age"].apply(
            assign_age_range)

        # Add a "Cost" field that is less than the "Transaction_Amount" field
        transaction_df["Cost"] = [round(random.uniform(
            50, amount), 2) for amount in transaction_df["Transaction_Amount"]]

        # Save the DataFrame to a CSV file
        transaction_df.to_csv(filename, index=False)

        print(f"Transaction data generated and saved to '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Define the filename for the CSV
filename = "CommerceTable.csv"

# Call the function to generate and save the transaction data
generate_and_save_transaction_data(filename)
