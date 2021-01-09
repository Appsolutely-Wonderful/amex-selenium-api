from datetime import datetime

class AmexTransaction:
    """
    Contains brief information about a specific transaction
    """
    def __init__(self, element):
        self._decode_html_element(element)

    def _decode_html_element(self, element):
        """
        Fills in class properties with information from the given element.

        Sets fields:
            - date
            - merchant
            - amount
        """
        this_year = datetime.now().year
        pieces = element.text.split('\n')
        # idx 0 - date
        self.date = datetime.strptime(pieces[0] + " " + str(this_year), "%b %d %Y")

        # idx 1 - Pending or Merchant
        # idx 2 - If pending: merchant, else amount
        # idx 3 - If pending: amount, else out of bounds
        pending = pieces[1] == 'Pending'
        if not pending:
            self.merchant = pieces[1]
            self._set_amount(pieces[2])
        else:
            self.merchant = pieces[2]
            self._set_amount(pieces[3])

    def _set_amount(self, amount_str):
        """
        Sets the amount field on the object as a float
        """
        # remove $ sign and cast to float
        self.amount = float(amount_str[1:])



    def __repr__(self):
        return f"{self.date} - {self.merchant} - {self.amount}"
