import requests
import time
import concurrent.futures

# Configuration
API_URL = "http://localhost:8000"
USER_FILE = "backend/test_users.txt"
NUM_USERS = 40

def verify_user(username):
    start_time = time.time()
    try:
        response = requests.post(f"{API_URL}/verify-user", json={"username": username}, timeout=5)
        duration = time.time() - start_time
        if response.status_code == 200 and response.json().get("allowed"):
            return True, duration
        else:
            return False, duration
    except Exception as e:
        return False, time.time() - start_time

def run_simulation():
    print(f"🚀 Starting simulation for {NUM_USERS} users...")
    
    # Read users
    with open(USER_FILE, "r") as f:
        usernames = [line.strip() for line in f if line.strip()][:NUM_USERS]

    start_sim = time.time()
    results = []

    # Use ThreadPoolExecutor to simulate concurrent logins
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = {executor.submit(verify_user, user): user for user in usernames}
        for future in concurrent.futures.as_completed(future_to_user):
            results.append(future.result())

    total_sim_time = time.time() - start_sim
    successes = [r for r in results if r[0]]
    durations = [r[1] for r in results]

    print("\n--- Simulation Results ---")
    print(f"Total Users: {NUM_USERS}")
    print(f"Successful Logins: {len(successes)}")
    print(f"Failed Logins: {NUM_USERS - len(successes)}")
    print(f"Total Time Taken: {total_sim_time:.2f} seconds")
    print(f"Average Response Time: {sum(durations)/len(durations):.4f} seconds")
    print(f"Fastest Response: {min(durations):.4f} seconds")
    print(f"Slowest Response: {max(durations):.4f} seconds")
    print("--------------------------")

if __name__ == "__main__":
    run_simulation()
