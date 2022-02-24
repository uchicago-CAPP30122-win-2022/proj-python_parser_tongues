class Vaccines:

    def __init__(self, mmwr_week, date, location, administered, admin_per_100k, admin_per_100k_18plus, series_complete_18plus, series_complete_18pluspop):
        self.mmwr_week = mmwr_week
        self.date = date
        self.location = location
        self.administered = administered
        self.admin_per_100k = admin_per_100k
        self.admin_per_100k_18plus = admin_per_100k_18plus
        self.series_complete_18plus = series_complete_18plus
        self.series_complete_18pluspop = series_complete_18pluspop

    def __str__(self):
        s = "Date: " + self.date + "\n" + "Week: " + self.mmwr_week + "\n" + "State: " + self.location + "\n" + "Total Doses Administered: " + \
            self.administered + "\n" + "Doses Administered per 100k: " + self.admin_per_100k + "\n" + "Vaccines Administered per 100k 18 yrs+: " \
                + self.admin_per_100k_18plus + "\n" + "Total # of people 18+ who are fully vaccinated: " + self.series_complete_18plus + "\n" + \
                "Percent of people 18+ who are fully vaccinated: " + self.series_complete_18pluspop + "\n"
        return s 


