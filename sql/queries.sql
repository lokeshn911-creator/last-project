-- Part A: Data Infrastructure & Analytical Queries

-- Query 1: Top Customers by Support Ticket Volume
SELECT 
    customer_id, 
    COUNT(ticket_id) AS total_tickets
FROM support_tickets
GROUP BY customer_id
ORDER BY total_tickets DESC;

-- Query 2: Ticket Category Breakdown
SELECT 
    true_category, 
    COUNT(ticket_id) AS category_count
FROM support_tickets
GROUP BY true_category;