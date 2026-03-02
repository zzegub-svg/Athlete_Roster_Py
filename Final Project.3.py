# ================================================================
# UT AUSTIN ATHLETE DATABASE MANAGEMENT SYSTEM
# Merged Final Project -  Zachary
#
# This final script combines:
#   - Original function-based roster manager
#   - Object-oriented multi-team database system
# ================================================================

import csv
from statistics import mean

# ---------------------------------------------------------------
#                     ATHLETE CLASS
# ---------------------------------------------------------------
class Athlete:
    def __init__(self, name, position, year, number):
        self.name = name
        self.position = position
        self.year = year
        self.number = number
        self.tests = {}

    def add_test_result(self, test_name, value):
        self.tests[test_name] = value

    def __str__(self):
        return (f"{self.name} | #{self.number} | {self.position} | "
                f"{self.year} | Tests: {self.tests}")


# ---------------------------------------------------------------
#                     TEAM CLASS
# ---------------------------------------------------------------
class Team:
    def __init__(self, name):
        self.name = name
        self.athletes = []

    # -----------------------------------------------------------
    # Add Athlete
    # -----------------------------------------------------------
    def add_athlete(self, athlete):
        self.athletes.append(athlete)
        print(f"{athlete.name} added to {self.name}.\n")

    # -----------------------------------------------------------
    # Display Roster
    # -----------------------------------------------------------
    def show_roster(self):
        if not self.athletes:
            print(f"\nThe {self.name} roster is empty.\n")
            return


        print(f"\n--- {self.name} Roster ---")
        print("No  Name                Position     Year")
        print("--  ------------------  --------     ----")

        for a in self.athletes:
            print(f"{a.number:<3} {a.name:<18} {a.position:<12} {a.year}")

        print("\nDetailed athlete objects:")
        for a in self.athletes:
            print(a)
        print()

    # -----------------------------------------------------------
    # CSV LOADING
    # -----------------------------------------------------------
    def load_from_csv(self, filename):
        try:
            with open(filename, newline='') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    athlete = Athlete(
                        row["Name"],
                        row["Position"],
                        row["Year"],
                        row["Number"]
                    )
                    self.add_athlete(athlete)

            print(f"{self.name} roster loaded from {filename}.\n")
        except FileNotFoundError:
            print("Error: CSV file not found.\n")

    # -----------------------------------------------------------
    # CSV SAVING
    # -----------------------------------------------------------
    def save_to_csv(self, filename):
        with open(filename, "w", newline='') as f:
            fieldnames = ["Name", "Position", "Year", "Number", "Tests"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for a in self.athletes:
                writer.writerow({
                    "Name": a.name,
                    "Position": a.position,
                    "Year": a.year,
                    "Number": a.number,
                    "Tests": a.tests
                })

        print(f"{self.name} roster saved as {filename}.\n")

    # -----------------------------------------------------------
    # find_athlete FUNCTION
    # -----------------------------------------------------------
    def find_athlete(self, name):
        for a in self.athletes:
            if a.name.lower() == name.lower():
                return a
        return None

    # -----------------------------------------------------------
    # COMPARE Athletes
    # -----------------------------------------------------------
    def compare_athletes(self, name1, name2):
        a1 = self.find_athlete(name1)
        a2 = self.find_athlete(name2)

        if not a1 or not a2:
            print("Error: One or both athletes not found.\n")
            return

        print(f"\n--- Comparing {a1.name} vs {a2.name} ---")

        all_tests = set(a1.tests.keys()).union(a2.tests.keys())

        for test in all_tests:
            v1 = a1.tests.get(test, "N/A")
            v2 = a2.tests.get(test, "N/A")
            print(f"{test}: {a1.name}: {v1} | {a2.name}: {v2}")

        print()

    # -----------------------------------------------------------
    # TEAM AVERAGES
    # -----------------------------------------------------------
    def team_average(self, test_name):
        vals = [a.tests[test_name] for a in self.athletes if test_name in a.tests]

        if not vals:
            print(f"No athletes have results for '{test_name}'.\n")
            return

        print(f"Team average for {test_name}: {mean(vals):.2f}\n")


# ---------------------------------------------------------------
#                     LEAGUE CLASS
# ---------------------------------------------------------------
class League:
    def __init__(self, name):
        self.name = name
        self.teams = {}
        self.current_team = None

    def create_team(self, team_name):
        if team_name not in self.teams:
            self.teams[team_name] = Team(team_name)
            print(f"Team '{team_name}' created.\n")
        else:
            print("Team already exists.\n")

    def switch_team(self, team_name):
        if team_name in self.teams:
            self.current_team = self.teams[team_name]
            print(f"Switched to team: {team_name}\n")
        else:
            print("Team not found.\n")

    def list_teams(self):
        print("\n--- Teams in UT Austin ---")
        for t in self.teams:
            print(f"- {t}")
        print()


# ---------------------------------------------------------------
#                     MAIN MENU
# ---------------------------------------------------------------
def main():
    league = League("UT Austin")

    while True:
        print("========== UT AUSTIN ATHLETE DATABASE ==========")
        print("1. Create new team")
        print("2. Switch active team")
        print("3. List all teams")
        print("4. Load roster (CSV)")
        print("5. Add athlete")
        print("6. Add test result")
        print("7. Compare two athletes")
        print("8. Show team average for a test")
        print("9. Show team roster")
        print("10. Save team roster (CSV)")
        print("0. Exit")
        print("=================================================")

        choice = input("Choose an option: ").strip()

        # TEAM CREATION / SWITCHING
        if choice == "1":
            name = input("Enter new team name: ")
            league.create_team(name)

        elif choice == "2":
            name = input("Enter team to switch to: ")
            league.switch_team(name)

        elif choice == "3":
            league.list_teams()

        # ALL OPTIONS BELOW REQUIRE A CURRENT TEAM
        elif choice in ["4", "5", "6", "7", "8", "9", "10"]:
            if not league.current_team:
                print("\nError: No active team selected!\n")
                continue

            team = league.current_team

            if choice == "4":
                filename = input("CSV filename to load: ")
                team.load_from_csv(filename)

            elif choice == "5":
                name = input("Name: ")
                position = input("Position: ")
                year = input("Year: ")
                number = input("Number: ")
                team.add_athlete(Athlete(name, position, year, number))

            elif choice == "6":
                athlete_name = input("Athlete name: ")
                a = team.find_athlete(athlete_name)
                if a:
                    test = input("Test name: ")
                    value = float(input("Value: "))
                    a.add_test_result(test, value)
                    print("Test result added.\n")
                else:
                    print("Athlete not found.\n")

            elif choice == "7":
                a1 = input("First athlete: ")
                a2 = input("Second athlete: ")
                team.compare_athletes(a1, a2)

            elif choice == "8":
                test = input("Test name: ")
                team.team_average(test)

            elif choice == "9":
                team.show_roster()

            elif choice == "10":
                filename = input("CSV filename to save: ")
                team.save_to_csv(filename)

        elif choice == "0":
            print("Goodbye! Hook ’em Horns! 🤘")
            break

        else:
            print("Invalid choice. Try again.\n")


# ---------------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
