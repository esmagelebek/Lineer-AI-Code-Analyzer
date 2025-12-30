import pandas as pd

class DebtReporter:
    @staticmethod
    def to_console(data):
        df = pd.DataFrame(data)
        if df.empty:
            print("Tebrikler! Hiç teknik borç bulunamadı.")
        else:
            print("\n--- TEKNİK BORÇ RAPORU ---\n")
            print(df.to_string(index=False))

    @staticmethod
    def to_csv(data, filename="technical_debt.csv"):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"\nRapor şuraya kaydedildi: {filename}")