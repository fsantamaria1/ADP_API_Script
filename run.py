import datetime
import time
from main import main
import schedule


def run_script():
    print("Running...")

    start = time.time()
    print("Start time:", datetime.datetime.fromtimestamp(start).strftime('%H:%M'))

    main()

    end = time.time()
    print("End time:", datetime.datetime.fromtimestamp(end).strftime('%H:%M'))

    elapsed_time = end - start
    time_difference = datetime.timedelta(seconds=elapsed_time)
    print("Elapsed time:", time_difference)

    print("Done")


if __name__ == '__main__':
    time_to_run = '22:00'

    # Schedule script to run daily at 10 PM
    schedule.every().day.at(time_to_run).do(run_script)

    while True:
        print(f"Waiting for scheduled time: {time_to_run}")
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"Current time: {current_time}\n")
        schedule.run_pending()
        time.sleep(30)
