import random
import time

# Function to generate a random number using allowable digits
# def generate_random_number(allowable_digits):
#     length = random.randint(1, 9)  # Random length between 1 and 9
#     number = 0
#     for _ in range(length):
#         number = number * 10 + random.choice(allowable_digits)
#     return number

def generate_random_number(allowable_digits, max_digits):
    num_digits = random.randint(1, max_digits)
    return int(''.join(str(random.choice(allowable_digits)) for _ in range(num_digits)))

# Sizes of datasets （Dataset 1）
sizes = [100, 1000, 10000, 100000, 500000, 1000000]

# Generate and save datasets
for size in sizes:
    start_time = time.time()  
    dataset = []
    # Determine the maximum number of digits based on the size of the dataset
    max_digits = len(str(size))
    
    # Re-seed the random number generator with the current time for variability
    random.seed(time.time())
    
    # Allowable digits based on the group leader ID
    group_leader_id = 1211103705
    allowable_digits = list(set(int(digit) for digit in str(group_leader_id)))
    
    # Generate the dataset with random numbers based on allowable digits
    for _ in range(size):
        random_number = generate_random_number(allowable_digits, max_digits)
        dataset.append(random_number)
    
    # Create a filename based on the dataset size
    filename = f"dataset_{size}.txt"
    
    # Save the dataset to a text file
    with open(filename, 'w') as file:
        for number in dataset:
            file.write(f"{number}\n")

    end_time = time.time()  # End time
    generation_time = end_time - start_time

    print(f"Dataset of size {size} generated in {generation_time:.2f} seconds.")
    print(f"Dataset of size {size} saved to {filename}")
