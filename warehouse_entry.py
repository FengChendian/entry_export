import time
from invoice_item import InvoiceItem

class WarehouseEntry:
    __items: list[InvoiceItem]
    def __init__(self) -> None:
        self.__supplier_name = ""
        self.__invoice_code = ""
        self.__invoice_number = ""
        self.__purchase_date = ""
        self.__entry_date = time.strftime("%Y-%m-%d", time.localtime())
        self.__amount_with_tax_zh = ""
        self.__amound_with_tax = ""
        self.__items = []
    
    @property
    def supplier_name(self):
        return self.__supplier_name
    @property
    def invoice_code(self):
        return self.__invoice_code
    @property
    def invoice_number(self):
        return self.__invoice_number
    @property
    def purchase_date(self):
        return self.__purchase_date
    @property
    def entry_date(self):
        return self.__entry_date
    @property
    def amount_with_tax_zh(self):
        return self.__amount_with_tax_zh
    @property
    def amount_with_tax(self):
        return self.__amound_with_tax
    @property
    def items(self):
        return self.__items

    @staticmethod
    def _get_invoice_info_name(info:dict):
       return info['Name']
    @staticmethod
    def _get_invoice_info_value(info:dict):
       return info['Value']


    def get_invoice_infos(self, invoice_infos):
        for info in invoice_infos:
            if type(info) is dict:
                info_name = self._get_invoice_info_name(info)
                info_value = self._get_invoice_info_value(info)
                if info_name == '销售方名称':
                    self.__supplier_name = info_value
                elif info_name == '发票代码':
                    self.__invoice_code = info_value
                elif info_name == '发票号码':
                    self.__invoice_number = info_value
                elif info_name == '开票日期':
                    self.__purchase_date = info_value
                elif info_name == '价税合计(大写)':
                    self.__amount_with_tax_zh = info_value
                elif info_name == '小写金额':
                    self.__amound_with_tax = info_value

    def get_invoice_items(self, invoice_items):
        for item in invoice_items:
            invoice_item = InvoiceItem()
            invoice_item.name = item['Name']
            invoice_item.spec = item['Spec']
            invoice_item.unit = item['Unit']
            invoice_item.quantity = item['Quantity']
            invoice_item.unit_price = item['UnitPrice']
            invoice_item.amount_without_tax = item['AmountWithoutTax']
            invoice_item.tax_rate = item['TaxRate']
            self.items.append(invoice_item)
                
