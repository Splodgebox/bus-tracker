class BusTime:
    def __init__(self, number, name, scheduled_time, is_timetabled):
        self.number = number
        self.name = name
        self.scheduled_time = scheduled_time
        self.is_timetabled = is_timetabled

    def __repr__(self):
        return f"<BusTime {self.number} {self.name} {self.scheduled_time} Timetabled?: {self.is_timetabled}>"