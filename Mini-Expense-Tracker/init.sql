-- Mini Expense Tracker (MySQL 8+)
DROP DATABASE IF EXISTS mini_expense;
CREATE DATABASE mini_expense CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE mini_expense;

-- Single normalized-ish table with useful indexes
CREATE TABLE expenses (
  expense_id   BIGINT AUTO_INCREMENT PRIMARY KEY,
  occurred_on  DATE NOT NULL,
  amount       DECIMAL(10,2) NOT NULL,   -- negative = expense, positive = income
  category     VARCHAR(50) NOT NULL,
  note         VARCHAR(200) NULL,
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_date (occurred_on),
  KEY idx_category (category)
);

-- A simple monthly totals view
CREATE OR REPLACE VIEW v_monthly_totals AS
SELECT
  DATE_FORMAT(occurred_on, '%Y-%m-01') AS month_start,
  ROUND(SUM(amount), 2) AS net_amount
FROM expenses
GROUP BY DATE_FORMAT(occurred_on, '%Y-%m-01')
ORDER BY month_start;

-- Category breakdown per month view
CREATE OR REPLACE VIEW v_monthly_category AS
SELECT
  DATE_FORMAT(occurred_on, '%Y-%m-01') AS month_start,
  category,
  ROUND(SUM(amount), 2) AS total_amount,
  COUNT(*) AS txn_count
FROM expenses
GROUP BY DATE_FORMAT(occurred_on, '%Y-%m-01'), category
ORDER BY month_start, ABS(SUM(amount)) DESC;

-- Seed a few example rows
INSERT INTO expenses (occurred_on, amount, category, note) VALUES
('2025-08-01', -120.50, 'Groceries', 'WF run'),
('2025-08-02', -15.00,  'Dining',    'Burrito'),
('2025-08-15', 2000.00, 'Income',    'Paycheck'),
('2025-09-03', -35.75,  'Transportation', 'Metro card'),
('2025-09-05', -110.30, 'Utilities', 'Electric'),
('2025-09-15', 2000.00, 'Income',    'Paycheck');

-- Handy queries (uncomment in Workbench to try)
-- SELECT * FROM v_monthly_totals;
-- SELECT * FROM v_monthly_category WHERE month_start='2025-09-01';
