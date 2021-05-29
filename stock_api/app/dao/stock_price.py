# Class to return JSON objects
class StockPrice:
    time = ""
    open = 0
    high = 0
    low = 0
    close = 0
    volume = 0

    def default(self, o):
        return o.__dict__

    def __init__(self, time, open, high, low, close, volume):
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __str__(self):
        return (
            "DATE: "
            + str(self.time)
            + " OPEN: "
            + str(self.open)
            + " HIGH: "
            + str(self.high)
            + " LOW: "
            + str(self.low)
            + " CLOSE: "
            + str(self.close)
            + " VOLUME: "
            + str(self.volume)
        )
