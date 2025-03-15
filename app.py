import datetime
import calendar

class MeetingScheduler:
    def _init_(self, working_hours=(9, 17), public_holidays=None):
        self.working_hours = working_hours 
        self.public_holidays = public_holidays if public_holidays else []
        self.schedule = {} 
    
    def is_working_day(self, date):
       
        if date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return False
        if date in self.public_holidays:
            return False
        return True

    def add_user(self, user):
       
        if user not in self.schedule:
            self.schedule[user] = []

    def schedule_meeting(self, user, date, start_hour, end_hour):
        
        self.add_user(user)
        
       
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        
        if not self.is_working_day(date):
            return "Error: Cannot schedule on weekends or public holidays."

        if start_hour < self.working_hours[0] or end_hour > self.working_hours[1]:
            return "Error: Meeting time must be within working hours."

        for meeting in self.schedule[user]:
            if not (end_hour <= meeting[0] or start_hour >= meeting[1]):
                return "Error: Overlapping meeting detected."

        self.schedule[user].append((start_hour, end_hour, date))
        self.schedule[user].sort()
        return "Meeting scheduled successfully."

    def view_meetings(self, user):
     
        if user not in self.schedule or not self.schedule[user]:
            return "No meetings scheduled."
        return self.schedule[user]

    def available_slots(self, user, date):
       
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "Error: Non-working day."

        booked_slots = [meeting[:2] for meeting in self.schedule.get(user, []) if meeting[2] == date]
        available_slots = []

        start = self.working_hours[0]
        for slot in booked_slots:
            if start < slot[0]:
                available_slots.append((start, slot[0]))
            start = slot[1]

        if start < self.working_hours[1]:
            available_slots.append((start, self.working_hours[1]))

        return available_slots if available_slots else "No available slots."


scheduler = MeetingScheduler(public_holidays=[datetime.date(2025, 1, 1)]) 

print(scheduler.schedule_meeting("Asha", "2025-03-17", 10, 11)) 
print(scheduler.schedule_meeting("Asha", "2025-03-17", 10, 12)) 
print(scheduler.view_meetings("Asha")) 
print(scheduler.available_slots("Asha", "2025-03-17")) 
