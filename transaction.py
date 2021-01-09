class Transaction:
    def __init__(self, date, merchant, amount, pending=False):
        self.date = date
        self.merchant = merchant
        self.amount = amount
        self.pending = pending

    def __str__(self):
        return f"{self.date} - {self.merchant} - {self.amount}"