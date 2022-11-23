from hangoutcore import util

def setup():
    util.terminal.log.INFO(f"Test complete.")


def beginSetup():
    try:
        setup()
    except KeyboardInterrupt:
        print("Exiting HangoutCore")
    else:
        print("Exiting HangoutCore.")

if __name__ == "__main__":
    beginSetup()