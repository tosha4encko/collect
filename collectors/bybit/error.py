class BybitError(Exception):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.exchange_id = 1
