SELECT 
    EntityName AS Entity,
    CIK,
    End AS Date,
    ROUND(SUM(CASE WHEN Metric = 'NetIncomeLoss' THEN Value ELSE NULL END) / 1000000, 2) AS NetIncomeLoss,
    ROUND(SUM(CASE WHEN Metric = 'Revenues' THEN Value ELSE NULL END) / 1000000, 2) AS Revenues,
    ROUND(SUM(CASE WHEN Metric = 'OperatingIncomeLoss' THEN Value ELSE NULL END) / 1000000, 2) AS OperatingIncomeLoss,
    CASE 
        WHEN SUM(CASE WHEN Metric = 'Revenues' THEN Value ELSE NULL END) != 0 THEN 
            ROUND((SUM(CASE WHEN Metric = 'NetIncomeLoss' THEN Value ELSE NULL END) / NULLIF(SUM(CASE WHEN Metric = 'Revenues' THEN Value ELSE NULL END), 0)) * 100, 2)
        ELSE NULL 
    END AS ProfitMarginPercent,
    CASE 
        WHEN EXTRACT(MONTH FROM End) IN (1, 2, 3) THEN CONCAT('Q1-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (4, 5, 6) THEN CONCAT('Q2-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (7, 8, 9) THEN CONCAT('Q3-', EXTRACT(YEAR FROM End))
        ELSE CONCAT('Q4-', EXTRACT(YEAR FROM End))
    END AS Quarter
FROM 
    test_table
WHERE 
    Metric IN ('NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss')
GROUP BY 
    EntityName, CIK, End
ORDER BY 
    EntityName, CIK, End;
