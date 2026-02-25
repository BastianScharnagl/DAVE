import os

while True:
    message = input("Your message:")
    with open(os.path.join("signals", "cli", datetime.now() + ".txt"), "w") as f:
        f.write(message)