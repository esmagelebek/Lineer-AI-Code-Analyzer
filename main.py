from analyzer import TechnicalDebtAnalyst
from reporter import DebtReporter

def main():
    target_project = input("Analiz edilecek projenin yolunu girin: ")
    
    # 1. Analizi Başlat
    analyst = TechnicalDebtAnalyst(target_project)
    debt_data = analyst.run_analysis()
    
    # 2. Raporla
    DebtReporter.to_console(debt_data)
    DebtReporter.to_csv(debt_data)

if __name__ == "__main__":
    main()