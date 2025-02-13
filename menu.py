import subprocess

# Change this to the absolute path of your Django project
manage_file = "Stock_Site/"


def main():
    while True:
        print("\nCommand Menu:")
        print("1. Run Django Server")
        print("2. Collect Data")
        print("3. Import Data")
        print("4. Stocks to tickers (In Development!)")
        print("5. Git Commit and Pull")
        print("6. Only Push")
        print("7. Git Commit and Push")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            full_command = f"bash -c 'cd {manage_file} && python manage.py runserver; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "2":
            full_command = f"bash -c 'cd {manage_file} && python manage.py collect_data; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "3":
            full_command = f"bash -c 'cd {manage_file} && python manage.py import_data; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "4":
            full_command = f"bash -c 'cd {manage_file} && python manage.py stos; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "5":
            print("Enter your commit message:")
            commit_message = input()
            full_command = f"bash -c 'git add . && git commit -m \"{commit_message}\" && git pull; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "6":
            print("Enter your commit message:")
            commit_message = input()
            full_command = f"bash -c 'git push; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "7":
            print("Enter your commit message:")
            commit_message = input()
            full_command = f"bash -c 'git add . && git commit -m \"{commit_message}\" && git push; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        elif choice == "0":
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
