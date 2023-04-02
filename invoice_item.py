class InvoiceItem:
    def __init__(self) -> None:
        self.name = ""
        self.spec = ""
        self.unit = ""
        self.quantity = ""
        self.unit_price = ""
        self.amount_without_tax = ""
        self.tax_rate = ""

    @property
    def line_content(self) -> list[str]:
        return [self.name, self.spec, self.unit,
                self.quantity, self.unit_price,
                self.amount_without_tax, self.tax_rate]
