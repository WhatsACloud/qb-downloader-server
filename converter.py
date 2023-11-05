import pandas as pd
import io
import csv
import json

filename = "test.json"
output_filename = "test.csv"

def get_arr(obj):
    return [x["value"] for x in obj]

class Converter:
    def __init__(self):
        self.lelist = []
    
    def search_for_rows(self, data):
        if len(data["Rows"]) == 0:
            return self.lelist
        for row in data["Rows"]["Row"]:
            if "Header" in row:
                header = get_arr(row["Header"]["ColData"])
                header.append("")
                self.lelist.append(header)
            if "Rows" in row:
                self.search_for_rows(row)
            if "ColData" in row:
                colData = get_arr(row["ColData"])
                colData.insert(0, "")
                self.lelist.append(colData)
            if "Summary" in row:
                colData = get_arr(row["Summary"]["ColData"])
                colData.insert(1, "")
                self.lelist.append(colData)
        return self.lelist
    def convert(self, json_obj):
        columnNames = ["Profit/Expense"]
        for col in json_obj["Columns"]["Column"]:
            columnNames.append(col["ColTitle"])
        row_data = self.search_for_rows(json_obj)
        df = pd.DataFrame(row_data, columns=columnNames)
        csv_byte_str = io.BytesIO()
        df.to_csv(csv_byte_str, sep="\t", index=False)
        csv_byte_str = csv_byte_str.getvalue()
        return csv_byte_str

            
if __name__ == "__main__":
    converter = Converter()
    with open(filename) as f:
        data = json.load(f)
        csv_byte_str = converter.convert(data)
        with open(output_filename, "wb") as output_f:
            output_f.write(csv_byte_str)
            output_f.close()
        f.close()
