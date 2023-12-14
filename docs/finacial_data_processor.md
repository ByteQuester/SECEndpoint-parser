# Financial Data Processor

The Financial Data Processor is a software component that allows you to process financial data using two different methods: annually and quarterly. It provides a convenient way to filter, clean, and sort financial data based on a specific metric.

To use the Financial Data Processor, you need to import the `FinancialDataProcessor` class from the `financial_data_processor` module. Here's an example of how to use it:

```python
from financial_data_processor import FinancialDataProcessor, AnnualDataProcessor, QuarterlyDataProcessor

# Create an instance of the FinancialDataProcessor
data_processor = FinancialDataProcessor()

# Load your financial data into a DataFrame
df = ...

# Process the data annually
annual_processor = AnnualDataProcessor(df)
annual_data = annual_processor.process_data()

# Process the data quarterly
quarterly_processor = QuarterlyDataProcessor(df)
quarterly_data = quarterly_processor.process_data()
```

In the example above, we first create an instance of the `FinancialDataProcessor` class. Then, we create two concrete subclasses, `AnnualDataProcessor` and `QuarterlyDataProcessor`, passing the financial data DataFrame as an argument to their `__init__` methods. Finally, we call the `process_data` method on each processor to obtain the processed data.

## Customization

You can customize the processing logic by modifying the `process_data` method in the `AnnualDataProcessor` and `QuarterlyDataProcessor` classes. These methods currently implement the logic from the original functions `prepare_and_sort_data_annually` and `prepare_and_sort_data_quarterly`, respectively. Feel free to modify these methods to suit your specific needs.

## Conclusion

The Financial Data Processor provides a convenient way to process financial data based on a specific metric. By using the provided concrete subclasses, you can process the data annually or quarterly. Feel free to customize the processing logic to suit your specific requirements.