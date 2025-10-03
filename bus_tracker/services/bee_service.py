from bus_tracker.services.scraper import get_bee_times

class BeeService:
    def get_times(self, url: str):
        return get_bee_times(url)