import subprocess
import time
import webbrowser

# Change this to the absolute path of your Django project
manage_file = "Stock_Site/"

def main():
    while True:
        print("\n")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|                                         # Command Menu #                                              |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|                                         Server Commands                                               |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t| 1. Run Django Server  [ python3 manage.py runserver ]                                                 |")
        print("\t| 2. Collect Data Locally  [ python3 manage.py collect_data ]                                           |")
        print("\t| 3. Import Data into the Database  [ python3 manage.py import_data ]                                   |")
        print("\t| 4. Stocks to tickers (In Development!) [ python3 manage.py stos ]                                     |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|                                          Git Commands                                                 |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t| 5. Only Pull                                                                                          |")
        print("\t| 6. Git Commit and Pull                                                                                |")
        print("\t| 7. Only Push                                                                                          |")
        print("\t| 8. Git Commit and Push                                                                                |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|                                        Database Commands                                              |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t| 9. Open Postgres Database  [ psql -U user -d stock_analysis ]                                         |")
        print("\t| 10. Check User Data  [ SELECT * FROM auth_user ]                                                      |")
        print("\t| 11. Check Stock Data  [ SELECT * FROM accounts_stockdata WHERE stock_symbol = 'Ticker' ]              |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|                                         Other Commands                                                |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t| 12. Install Requirements                                                                              |")
        print("\t| 13. Update the requirements file                                                                      |")
        print("\t| (only for users with all packages installed).                                                         |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\t|  0. Exit                                                                                              |")
        print("\t|-------------------------------------------------------------------------------------------------------|")
        print("\n")

        choice = input("\tEnter your choice: ")

        if choice == "1":
            full_command = f"bash -c 'cd {manage_file} && python3 manage.py runserver; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
            # Wait a few seconds to ensure the server starts
            time.sleep(2)  # Adjust if needed

            # Open the Django development server in the browser
            webbrowser.open("http://127.0.0.1:8000/")

        elif choice == "2":
            full_command = f"bash -c 'cd {manage_file} && python3 manage.py collect_data; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "3":
            full_command = f"bash -c 'cd {manage_file} && python3 manage.py import_data; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "4":
            full_command = f"bash -c 'cd {manage_file} && python3 manage.py stos; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "5":
            full_command = f"bash -c 'git pull; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "6":
            print("Enter your commit message:")
            commit_message = input()
            full_command = f"bash -c 'git add . && git commit -m \"{commit_message}\" && git pull; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "7":
            full_command = f"bash -c 'git push; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "8":
            print("Enter your commit message:")
            commit_message = input()
            full_command = f"bash -c 'git add . && git commit -m \"{commit_message}\" && git push; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "9":
            print("Enter your username:")
            user = input().strip()
            full_command = f"bash -c 'psql -U {user} -d stock_analysis; echo \"Closing in 10 Sec...\"; sleep 10; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "10":
            print("Enter your username:")
            user = input().strip()
            sql_command = "SELECT * FROM auth_user;"
            full_command = f"gnome-terminal --maximize -- bash -c 'psql -U {user} -d stock_analysis -c \"{sql_command}\"; echo \"Closing in 10 Sec...\"; sleep 10; exit'"
            subprocess.Popen(full_command, shell=True, start_new_session=True)

        elif choice == "11":
            print("Enter your username:")
            user = input().strip()
            print("Enter the stock symbol (Ex. ITC.BO):")
            Ticker = input().strip()
            sql_command = f"SELECT * FROM accounts_stockdata WHERE stock_symbol = '{Ticker}';"
            full_command = f"gnome-terminal --maximize -- bash -c \"psql -U {user} -d stock_analysis -c \\\"{sql_command}\\\"; echo 'Closing in 10 Sec...'; sleep 10; exit\""
            subprocess.Popen(full_command, shell=True, start_new_session=True)

        elif choice == "12":
            full_command = f"bash -c 'pip install -r requirements.txt; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)

        elif choice == "13":
            full_command = f"bash -c 'pip freeze > requirements.txt; echo \"Closing in 1 minute...\"; sleep 60; exit'"
            subprocess.Popen(["x-terminal-emulator", "-e", full_command], start_new_session=True)
        
        elif choice == "0":
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
