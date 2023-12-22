from chat.app import ApplicationManager


def run_application(cik_number="0000012927", query_type="Profitability", base_dir="data"):
    app_manager = ApplicationManager(cik_number, query_type, base_dir)
    app_manager.run()


if __name__ == "__main__":
    run_application()