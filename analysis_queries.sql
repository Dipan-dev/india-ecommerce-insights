-- ============================================================
-- E-Commerce Sales Analysis — SQL Queries
-- Author  : Dipan Shil
-- Dataset : orders.csv + customers.csv (3,000 orders, 500 customers)
-- Tool    : SQLite / PostgreSQL compatible
-- ============================================================


-- ============================================================
-- 1. OVERALL BUSINESS SUMMARY
-- ============================================================

-- Total revenue, orders, avg order value
SELECT
    COUNT(order_id)                         AS total_orders,
    COUNT(DISTINCT customer_id)             AS unique_customers,
    ROUND(SUM(total_amount), 2)             AS total_revenue,
    ROUND(AVG(total_amount), 2)             AS avg_order_value,
    ROUND(SUM(total_amount) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM orders
WHERE order_status = 'Delivered';


-- ============================================================
-- 2. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    strftime('%Y-%m', order_date)           AS month,
    COUNT(order_id)                         AS total_orders,
    ROUND(SUM(total_amount), 2)             AS monthly_revenue,
    ROUND(AVG(total_amount), 2)             AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY month
ORDER BY month;


-- ============================================================
-- 3. TOP 5 BEST-SELLING CATEGORIES BY REVENUE
-- ============================================================

SELECT
    category,
    COUNT(order_id)             AS total_orders,
    SUM(quantity)               AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 5;


-- ============================================================
-- 4. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    product_name,
    category,
    SUM(quantity)               AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(discount_pct), 1) AS avg_discount_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 5. CITY-WISE SALES PERFORMANCE
-- ============================================================

SELECT
    city,
    COUNT(DISTINCT customer_id)             AS customers,
    COUNT(order_id)                         AS total_orders,
    ROUND(SUM(total_amount), 2)             AS total_revenue,
    ROUND(AVG(total_amount), 2)             AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY city
ORDER BY total_revenue DESC;


-- ============================================================
-- 6. ORDER STATUS BREAKDOWN (RETURNS & CANCELLATIONS)
-- ============================================================

SELECT
    order_status,
    COUNT(order_id)                                          AS total_orders,
    ROUND(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER(), 2) AS percentage,
    ROUND(SUM(total_amount), 2)                             AS revenue_impact
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- ============================================================
-- 7. PAYMENT METHOD PREFERENCE
-- ============================================================

SELECT
    payment_method,
    COUNT(order_id)                         AS total_orders,
    ROUND(SUM(total_amount), 2)             AS total_revenue,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders WHERE order_status = 'Delivered'), 2) AS usage_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY payment_method
ORDER BY total_orders DESC;


-- ============================================================
-- 8. CUSTOMER SEGMENTATION BY ORDER FREQUENCY (RFM LITE)
-- ============================================================

WITH customer_stats AS (
    SELECT
        customer_id,
        COUNT(order_id)             AS order_count,
        ROUND(SUM(total_amount), 2) AS total_spent,
        MAX(order_date)             AS last_order_date
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count >= 10 THEN 'Champion'
        WHEN order_count BETWEEN 5 AND 9 THEN 'Loyal'
        WHEN order_count BETWEEN 2 AND 4 THEN 'Potential'
        ELSE 'One-Time'
    END                             AS customer_segment,
    COUNT(customer_id)              AS customer_count,
    ROUND(AVG(total_spent), 2)      AS avg_lifetime_value,
    ROUND(AVG(order_count), 1)      AS avg_orders
FROM customer_stats
GROUP BY customer_segment
ORDER BY avg_lifetime_value DESC;


-- ============================================================
-- 9. DISCOUNT IMPACT ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN discount_pct = 0  THEN 'No Discount'
        WHEN discount_pct <= 10 THEN 'Low (1-10%)'
        WHEN discount_pct <= 20 THEN 'Medium (11-20%)'
        ELSE 'High (>20%)'
    END                             AS discount_tier,
    COUNT(order_id)                 AS total_orders,
    ROUND(AVG(total_amount), 2)     AS avg_order_value,
    ROUND(SUM(total_amount), 2)     AS total_revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY discount_tier
ORDER BY total_orders DESC;


-- ============================================================
-- 10. REPEAT CUSTOMERS vs ONE-TIME BUYERS
-- ============================================================

WITH order_counts AS (
    SELECT customer_id, COUNT(order_id) AS num_orders
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    CASE WHEN num_orders = 1 THEN 'One-Time Buyer' ELSE 'Repeat Buyer' END AS buyer_type,
    COUNT(customer_id)  AS customer_count,
    ROUND(AVG(num_orders), 2) AS avg_orders
FROM order_counts
GROUP BY buyer_type;
