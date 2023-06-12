import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Column,
    Text,
    icons,
)
from openpyxl import load_workbook, Workbook
from config_read import get_pdf_base64
import pdf_ocr
import json
from warehouse_entry import WarehouseEntry
from excel_export import export_entry_workbook
import os
import sys

def main(page: Page):
    page.title = "入库单生成器"
    page.window_height = 200
    page.window_width = 200
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    # page.horizontal_alignment = flet.MainAxisAlignment.CENTER
    # Pick files dialog
    # selected_files = Text()
    if getattr(sys, 'frozen', None):
        os.chdir(sys._MEIPASS)
    def pick_files_result(e: FilePickerResultEvent):
        # selected_files.value = (
        #     ", ".join(map(lambda f: f.name, e.files)
        #               ) if e.files else "Cancelled!"
        # )
        # print(e.files[0].name)
        # print(e.files[0].path)
        
        pdf_base64 = get_pdf_base64(e.files[0].path)
        pdf_info = pdf_ocr.ocr(pdf_base64=pdf_base64)
        # with open("test.json", "w") as f:
        #     f.write(pdf_info)
        # with open("test.json", "r") as f:
        #     pdf_info_dict = json.load(f)
        pdf_info_dict = json.loads(pdf_info)
        # pdf_info_dict = json.loads(json.dumps(pdf_info_dict))
        invoice_infos = pdf_info_dict["VatInvoiceInfos"]
        invoice_items = pdf_info_dict["Items"]
        # print(invoice_infos)
        warehouse_entry = WarehouseEntry()
        warehouse_entry.get_invoice_infos(invoice_infos)
        warehouse_entry.get_invoice_items(invoice_items)
        # print(warehouse_entry.purchase_date)
        # for item in warehouse_entry.items:
        #     print(item.line_content)

        global wb 
        wb = export_entry_workbook(warehouse_entry)

        
        save_file_button.disabled = False
        save_file_button.update()
        # selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)

    # Save file dialog
    def save_file_result(e: FilePickerResultEvent):
        print(e.path)
        
        if e.path:
            path = e.path
            if '.xlsx' not in path or '.xls' not in path:
                path = path + '.xlsx'
            wb.save(path)

    save_file_dialog = FilePicker(on_result=save_file_result)

    save_file_button = ElevatedButton(
        "导出入库单",
        icon=icons.SAVE,
        on_click=lambda _: save_file_dialog.save_file(),
        disabled=True,
    )

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, save_file_dialog])
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.add(
        
        Column(
            [
                ElevatedButton(
                    "打开文件",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),

                save_file_button,
            ],
            horizontal_alignment=flet.CrossAxisAlignment.START
        ),
    )


flet.app(target=main)
