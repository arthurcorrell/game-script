import multiprocessing
import aim
import trigger

def run_aim():
    aim.send_coordinates()

def run_trigger():
    trigger.send_bool()

if __name__ == "__main__":
    aim_process = multiprocessing.Process(target=run_aim)
    trigger_process = multiprocessing.Process(target=run_trigger)

    aim_process.start()
    trigger_process.start()

    aim_process.join()
    trigger_process.join()