import random
from datetime import datetime, timedelta, date
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import json

# changing to milileter pretty much idk where to use
conversions = {
    "cups": 240,
    "ounces": 29.57,
    "liters": 1000,
    "gallons": 3785,
    "milliliters": 1
}



now = datetime.now()
current_month = now.month 

goal_file = "water_goal.json"


def save_goal(daily, weekly, monthly, unit):
    goals = {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "unit": unit
    }

    with open(goal_file, "w") as f:
        json.dump(goals, f)


def load_goals():
    try:
        with open(goal_file, "r") as f:
            goals =  json.load(f)
        return goals["daily"], goals["weekly"], goals["monthly"], goals["unit"]
    except FileNotFoundError:
        return None, None, None, None




def log_water_intake(amount, unit, log_file="water_log.txt"):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}: {amount} {unit}\n")

def show_log(log_file="water_log.txt"):
    try:
        with open(log_file, "r") as f:
            print("\n--- Water Intake Log ---")
            print(f.read())
    except FileNotFoundError:
        print("No log file found. Start by logging your water intake!")

def main():
    print("Water Intake Tracker")
    valid_units = ["gallons", "liters", "cups", "milliliters", "ounces"]
    goal_amount_daily, goal_amount_weekly, goal_amount_monthly, goal_unit = load_goals()



    while True:
        print("\nOptions:")
        print("1. Log water intake")
        print("2. Show log")
        print("3. Goal")
        print("4. Clear Log")
        print("5. Fun Facts About Water")
        print("6. Exit")
        choice = input("Select an option (1/2/3/4): ").strip()

        if choice == "1":
            unit = input("Enter the unit to use (gallons, liters, cups, milliliters, or ounces): ").lower().strip()
            if unit not in valid_units:
                print("Invalid unit selected. Please choose a valid unit.")
                continue
            try:
                amount = float(input(f"How many {unit} of water did you drink? "))
                log_water_intake(amount, unit)
                print("Water intake logged successfully!")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "2":
            show_log()

        elif choice == "3":
            checkormake = input("Would you like to change or set a goal or check if your current goal has been met? (Set or Check) ").lower().strip()

            if checkormake == "set":
                goal_unit = input("Pick a unit for your goal to be in (gallons, liters, cups, milliliters, or ounces): ").lower().strip()
                if goal_unit not in valid_units:
                    print("Invalid unit selected. Please choose a valid unit.")
                else:
                    dwm = input("Would you like to set a daily, weekly or monthly goal ").lower().strip()
                    if dwm == "daily":
                        try:
                            goal_amount_daily = float(input(f"How many {goal_unit} of water do you want to drink per day? "))
                            print(f"Your daily goal is set to {goal_amount_daily} {goal_unit}.")
                            save_goal(goal_amount_daily, goal_amount_weekly, goal_amount_monthly, goal_unit)
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    elif dwm == "weekly":
                        try:
                            goal_amount_weekly = float(input(f"How many {goal_unit} of water do you want to drink per week? "))
                            print(f"Your weekly goal is set to {goal_amount_weekly} {goal_unit}")
                            save_goal(goal_amount_daily, goal_amount_weekly, goal_amount_monthly, goal_unit)
                            perweek = goal_amount_weekly/7
                            print(f"You need to drink {perweek} {goal_unit} to meet ur weekly goal")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    elif dwm == "monthly":
                        try:
                            goal_amount_monthly = float(input(f"How many {goal_unit} of water do you want to drink per month? "))
                            print(f"Your monthly goal is set to {goal_amount_monthly} {goal_unit}")
                            save_goal(goal_amount_daily, goal_amount_weekly, goal_amount_monthly, goal_unit)
                            permonthAJSN = goal_amount_monthly/30
                            permonthJMMJAOD = goal_amount_monthly/31
                            permonthF = goal_amount_monthly/28
                            if current_month in [4, 6, 9, 11]:
                                print(f"You need to drink {permonthAJSN} {goal_unit} everyday to meet your goal")

                            elif current_month in [1, 3, 5, 7, 8, 10, 12]:
                                print(f"You need to drink {permonthJMMJAOD} {goal_unit} everyday to meet your goal")

                            elif current_month == "2":
                                print(f"You need to drink {permonthF} {goal_unit} everyday to meet your goal")
                            
                            
                        except ValueError:
                            print("Invalid input. Please enter a valid number")

            if checkormake == "check":
                checkwhat = input("Which of your goals would you like to check (Daily, Weekly or Monthly) ").lower().strip()

                if checkwhat == "daily":
                    if goal_unit is None or goal_amount_daily is None:
                        print("No daily goal set. Please set a goal first.")
                    else:
                        try:
                            with open("water_log.txt", "r") as f:
                                today = date.today()
                                total = 0
                                for line in f:
                                    timestamp, entry = line.split(": ", 1)
                                    entry_date = datetime.fromisoformat(timestamp.strip()).date()
                                    if entry_date == today:
                                        amount, unit = entry.strip().split()[:2]
                                        amount = float(amount)
                                        unit = unit.lower()
                                        total += amount * conversions[unit] / conversions[goal_unit]

                                print(f"Today's water intake is {total:.2f} {goal_unit}")
                                if total >= goal_amount_daily:
                                    print("You reached your water intake goal YAY!!!")
                                else:
                                    print(f"Keep drinking! You need {goal_amount_daily - total:.2f} more {goal_unit}.")
                                    percent_doned = (total / goal_amount_daily)
                                    if percent_doned > 100:
                                        percent_doned = 100
                                    bar_size = 20
                                    fill_amountd  = int(bar_size * total / goal_amount_daily)
                                    bar = '█' * fill_amountd + '-' * (bar_size - fill_amountd)
                                    print(f"[{bar}] {percent_doned:1f}% of daily goal completed")

                                    
                        except FileNotFoundError:
                            print("No water log found. Start logging water intake first")

                if checkwhat == "weekly":
                    if goal_unit is None or goal_amount_weekly is None:
                        print("No weekly goal set. Please set a goal first")
                    else:
                        try:
                            today = date.today()
                            last_week = today - timedelta(weeks=1)
                            total = 0
                            with open("water_log.txt", "r") as f:
                                for line in f:
                                    timestamp, entry = line.split(": ", 1)
                                    entry_date = datetime.fromisoformat(timestamp.strip()).date()
                                    if last_week <= entry_date <= today:
                                        amount, unit = entry.strip().split()[:2]
                                        amount = float(amount)
                                        unit = unit.lower()
                                        total += amount * conversions[unit] / conversions[goal_unit]

                            print(f"This weeks water intake is {total: .2f} {goal_unit}")
                            if total >= goal_amount_weekly:
                                print("You reached your water intake goal YAY!!!!")
                            else:
                                print(f"Keep drinking! You need {goal_amount_weekly - total:.2f} more {goal_unit} of water.")
                                percent_donew = (total / goal_amount_weekly)
                                if percent_donew > 100:
                                    percent_donem = 100
                                bar_size = 20 
                                fill_amountw = int(bar_size * total / goal_amount_weekly)
                                bar = '█' * fill_amountw + '-' * (bar_size - fill_amountw)
                                print(f"[{bar}] {percent_donew:1f}% of daily goal completed")
                        except FileNotFoundError:
                            print("No water log found. Start logging water intake first")

                if checkwhat == "monthly":
                    if goal_unit is None or goal_amount_monthly is None:
                        print("No monthly goal set. Please set a goal first")
                    else:
                        try:
                            today = date.today()
                            last_month = today - relativedelta(months=1)
                            total = 0
                            with open("water_log.txt", "r") as f:
                                for line in f:
                                    timestamp, entry = line.split(": ", 1)
                                    entry_date = datetime.fromisoformat(timestamp.strip()).date()
                                    if last_month <= entry_date <= today:
                                        amount, unit = entry.strip().split()[:2]
                                        amount = float(amount)
                                        unit = unit.lower()
                                        total += amount * conversions[unit] / conversions[goal_unit]

                            print(f"This months water intake is {total} {goal_unit}")
                            if total >= goal_amount_monthly:
                                    print("You reached your water intake goal YAY!!!!!")
                            else: 
                                print(f"Keep drinking! You need {goal_amount_monthly - total:.2f} more {goal_unit} of water.")
                                percent_donem = (total / goal_amount_monthly)
                                if percent_donem > 100:
                                    percent_donem = 100
                                bar_size = 20 
                                fill_amountm = int(bar_size * total / goal_amount_monthly)
                                bar = '█' * fill_amountm + '-' * (bar_size - fill_amountm)
                                print(f"[{bar}] {percent_donem:1f}% of daily goal completed")

                        except FileNotFoundError:
                            print("No water log found. Start logging water intake first")
                
                


                            


                

        elif choice == "4":
            cleardata = input("Are you sure you want to clear your water log (Yes or No)? ").lower().strip()
            if cleardata == "yes":
                open("water_log.txt", "w").close()
                print("Water log cleared.")
            elif cleardata == "no":
                print("Water log not cleared.")
            else:
                print("Invalid input. Water log not cleared.")

        elif choice == "5":
            waterfacts = [
                "Water covers about 71% of the Earth", 
                "97% of Earth's water is salty",
                "The human body is 55-60% water",
                "Water can dissolve more substances than any other liquid",
                "A newborn baby is about 78% water",
                "Hot water can freeze faster than cold water",
                "The human body can only survive about a week without water",
                "The average American uses about 100 gallons of water every day",
                "Thirst is a delayed signal — by the time you feel thirsty, you’re already 1-2% dehydrated",
                "Most freshwater on Earth is ice",
                "Sound travels faster in water",
                "Earth’s largest waterfall is underwater",
                "Koalas don't need water",
                "There are more than 16 types of ice",
                "Your bones contain about 31 percent water",
                "Your brain is about 75 percent water",
                "Your lungs are about 90 percent water"
            ]
            random_fact = random.choice(waterfacts)
            print(random_fact)

        elif choice == "6":
            print("Exiting tracker. Stay hydrated!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, 5.")
            show_log()

if __name__ == "__main__":
    main()
