class Receipt:
    count_id = 0  # Class-level counter

    def __init__(self, creditcard, items):
        Receipt.count_id += 1
        self._receipt_id = Receipt.count_id  
        self._creditcard = creditcard  
        self._items = items  

    def get_receipt_id(self):
        return getattr(self, "_receipt_id", 0)  

    def get_creditcard(self):
        return getattr(self, "_creditcard", "Unknown") 

    def get_items(self):
        return getattr(self, "_items", [])  

    def set_receipt_id(self, receipt_id):
        self._receipt_id = receipt_id  

    def set_creditcard(self, creditcard):
        self._creditcard = creditcard  

    def set_items(self, items):
        self._items = items  
