SELECT 
    EntityName AS Entity,
    CIK,
    End,
    TO_VARCHAR(ROUND(SUM(CASE WHEN Metric = 'Assets' THEN Value ELSE NULL END) / 1000000, 2), '999,999,999,990.00') AS Assets_M,
    TO_VARCHAR(ROUND(SUM(CASE WHEN Metric = 'Liabilities' THEN Value ELSE NULL END) / 1000000, 2), '999,999,999,990.00') AS TotalLiabilities_Millions,
    TO_VARCHAR(ROUND(SUM(CASE WHEN Metric = 'StockholdersEquity' THEN Value ELSE NULL END) / 1000000, 2), '999,999,999,990.00') AS Equity_Millions,
    TO_VARCHAR(ROUND(CASE 
            WHEN SUM(CASE WHEN Metric = 'Liabilities' THEN Value ELSE NULL END) > 0 THEN 
                SUM(CASE WHEN Metric = 'Assets' THEN Value ELSE NULL END) / NULLIF(SUM(CASE WHEN Metric = 'Liabilities' THEN Value ELSE NULL END), 0)
            ELSE NULL 
          END, 2), '999,999,999,990.00') AS AssetToLiabilityRatio,
    TO_VARCHAR(ROUND(CASE 
            WHEN SUM(CASE WHEN Metric = 'StockholdersEquity' THEN Value ELSE NULL END) > 0 THEN 
                SUM(CASE WHEN Metric = 'Liabilities' THEN Value ELSE NULL END) / NULLIF(SUM(CASE WHEN Metric = 'StockholdersEquity' THEN Value ELSE NULL END), 0)
            ELSE NULL 
          END, 2), '999,999,999,990.00') AS DebtToEquityRatio,
    -- Calculating the quarter
    CASE 
        WHEN EXTRACT(MONTH FROM End) IN (1, 2, 3) THEN CONCAT('Q1-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (4, 5, 6) THEN CONCAT('Q2-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (7, 8, 9) THEN CONCAT('Q3-', EXTRACT(YEAR FROM End))
        ELSE CONCAT('Q4-', EXTRACT(YEAR FROM End))
    END AS Quarter
FROM 
    test_table
WHERE 
    Metric IN ('Assets', 'Liabilities', 'StockholdersEquity')
GROUP BY 
    EntityName, CIK, End
ORDER BY 
    EntityName, CIK, End;
