import numpy as np
import csv
import time

def load_star_data(filename='stars_data2.txt'):
    stars = []
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]  # Skip the first two lines
        for line in lines:
            parts = line.split()
            star = {
                'name': parts[0],
                'weight': int(parts[4]),
                'profit': int(parts[5])
            }
            stars.append(star)
    return stars

def knapsack(weights, profits, capacity):
    n = len(weights)  # Number of items
    dp = np.zeros((n + 1, capacity + 1), dtype=int)

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + profits[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    w = capacity  # Start with the full capacity
    items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # Check if the item was included
            items.append(i - 1)  # Add the item index to the list (adjust for 0-based index)
            w -= weights[i - 1] 

    return dp, items  # Return the DP table and the list of included items

def save_knapsack_result(stars, dp, items, capacity, execution_time, filename='knapsack_result.txt'):
    with open(filename, 'w') as f:
        f.write("0/1 Knapsack Result:\n")
        f.write("Maximum Profit: {}\n".format(dp[len(stars)][capacity]))
        f.write("Selected Stars:\n")
        f.write("Name Weight Profit\n")
        total_weight = 0
        total_profit = 0
        for i in items:
            star = stars[i]
            total_weight += star['weight']
            total_profit += star['profit']
            f.write(f"{star['name']} {star['weight']} {star['profit']}\n")
        f.write("\nTotal Weight: {}\n".format(total_weight))
        f.write("Total Profit: {}\n".format(total_profit))
        f.write("Execution Time: {:.6f} seconds\n".format(execution_time))

def save_knapsack_table_to_csv(dp, weights, profits, filename='knapsack_table.csv'):
    n, capacity = dp.shape
    n -= 1  # Adjust for zero indexing
    capacity -= 1  # Adjust for zero indexing

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header row
        header = ["Item/Capacity"] + [f"{w}" for w in range(capacity + 1)]
        csvwriter.writerow(header)

        # Write the DP table rows
        for i in range(n + 1):
            if i == 0:
                row = [f"{i}"] + [f"{dp[i][w]}" for w in range(capacity + 1)]
            else:
                row = [f"{i} ({weights[i-1]},{profits[i-1]})"] + [f"{dp[i][w]}" for w in range(capacity + 1)]
            csvwriter.writerow(row)

# Main code block
stars = load_star_data('stars_data.txt')  # Load star data
weights = [star['weight'] for star in stars]  # Extract weights of stars
profits = [star['profit'] for star in stars]  # Extract profits of stars
capacity = 800  # Define the maximum capacity of the knapsack

# Measure the execution time of the knapsack function
start_time = time.time()
dp, items = knapsack(weights, profits, capacity)  # Solve the knapsack problem
end_time = time.time()
execution_time = end_time - start_time

save_knapsack_result(stars, dp, items, capacity, execution_time, 'knapsack_result.txt')  # Save the results to a text file
save_knapsack_table_to_csv(dp, weights, profits, 'knapsack_table.csv')  # Save the DP table to a CSV file
