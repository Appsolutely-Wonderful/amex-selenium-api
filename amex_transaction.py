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
        self.id = element.get_attribute('id').split('_')[1]
        # idx 0 - date
        self.date = datetime.strptime(pieces[0] + " " + str(this_year), "%b %d %Y")

        # idx 1 - (Pending or Credit) or Merchant
        # TODO: This should probably be optimized to grab specific elements instead of
        #       trying to string parse the whole array
        # idx 2 - If pending: merchant, else amount
        # idx 3 - If pending: amount, else: or out of bounds
        #         If not pending: this could be amount or tag
        # idx 4 - If has tag: amount
        pending = pieces[1] == 'Pending'
        self.pending = pending
        self.credit = pieces[1] == 'Credit'
        if not pending and not self.credit:
            self.merchant = pieces[1]
            try:
                self._set_amount(pieces[2])
            # Value error occurs if value is not a # (it's a tag)
            except ValueError:
                self._set_amount(pieces[3])
        else:
            self.merchant = pieces[2]
            try:
                self._set_amount(pieces[3])
            # Value error occurs if value is not a # (it's a tag)
            except ValueError:
                self._set_amount(pieces[4])

    def _set_amount(self, amount_str):
        """
        Sets the amount field on the object as a float
        """
        # remove $ sign and cast to float
        clean_str = amount_str.strip().replace("$", '')
        # remove commas from string
        clean_str = clean_str.replace(",", "")

        # Linter thinks amount is defined outside of __init__ but it's wrong.
        # __init__ -> _decode_html_element -> _set_amount always.
        self.amount = float(clean_str)

    def __repr__(self):
        return f"{self.date} | {self.merchant} | ${self.amount}"
