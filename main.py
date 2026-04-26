import time


def pomodoro(minutes):
    print(f"Focus session started for {minutes} minutes.")
    time.sleep(minutes * 60)
    print("Session complete. Take a break!")


pomodoro(25)
