import csv


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_to_csv(self, table):
        with open(self.file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for r in range(len(table)):
                row = []
                for c in range(len(table[r])):
                    item = table[r][c]
                    row.append(item)

                writer.writerow(row)

    def load_from_csv(self):
        with open(self.file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            table = []
            for r in reader:
                row = []
                for c in r:
                    row.append(c)
                table.append(row)
        return table
