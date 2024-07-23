import time
from multiprocessing import Pool, cpu_count

def compute_square(number):
    """
    Function to compute the square of a number after a delay.
    :param number: The number to be squared
    :return: The square of the number
    """
    print(f"Processing number: {number}")
    time.sleep(2)  # Simulate a delay (e.g., a computationally expensive task)
    result = number ** 2
    return result

def main():
    numbers = [1, 2, 3, 4, 5]  # List of numbers to process

    # Create a Pool with the number of CPU cores available
    with Pool(cpu_count()) as pool:
        # Map the function 'compute_square' to the list of numbers
        results = pool.map(compute_square, numbers)
    
    # Print the results
    print("Results:", results)

if __name__ == "__main__":
    main()
