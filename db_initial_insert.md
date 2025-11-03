-- ======================================
-- NutriGuard Test Data
-- PostgreSQL Insert Statements
-- ======================================

SET search_path TO nutriguard;

-- ======================================
-- STAFF DATA
-- ======================================
INSERT INTO staff (name, email, password_hash, role, certification, is_active) VALUES
('Dr. Sarah Mitchell', 'sarah.mitchell@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'Admin', 'Hospital Administration Certificate', TRUE),
('Emily Chen', 'emily.chen@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'Dietitian', 'Registered Dietitian Nutritionist (RDN)', TRUE),
('Michael Rodriguez', 'michael.rodriguez@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'Dietitian', 'Clinical Nutrition Specialist', TRUE),
('Nurse Jennifer Parker', 'jennifer.parker@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'Nurse', 'RN License, Nutrition Care Certified', TRUE),
('Nurse David Kim', 'david.kim@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'Nurse', 'RN License', TRUE),
('Chef Marco Rossi', 'marco.rossi@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'KitchenStaff', 'Culinary Arts Degree, Food Safety Certified', TRUE),
('Chef Aisha Patel', 'aisha.patel@nutriguard.com', '$2a$10$abcdefghijklmnopqrstuvwxyz', 'KitchenStaff', 'Food Safety Manager Certification', TRUE);

-- ======================================
-- PATIENTS DATA
-- ======================================
INSERT INTO patients (name, age, gender, medical_conditions, dietary_restrictions, admission_date, photo_url) VALUES
('Robert Johnson', 68, 'Male', 'Type 2 Diabetes, Hypertension', 'Low sodium, Diabetic diet', '2025-10-15', 'https://example.com/photos/patient1.jpg'),
('Maria Garcia', 45, 'Female', 'Celiac Disease, Anemia', 'Gluten-free, Iron-rich foods', '2025-10-20', 'https://example.com/photos/patient2.jpg'),
('James Williams', 72, 'Male', 'Chronic Kidney Disease Stage 3, Heart Disease', 'Low potassium, Low phosphorus, Low sodium', '2025-10-18', 'https://example.com/photos/patient3.jpg'),
('Linda Thompson', 55, 'Female', 'Obesity, Pre-diabetes', 'Calorie-restricted, Low carbohydrate', '2025-10-25', 'https://example.com/photos/patient4.jpg'),
('Ahmed Hassan', 61, 'Male', 'Post-surgical recovery (Gastric bypass)', 'Soft foods, High protein, Small portions', '2025-10-28', 'https://example.com/photos/patient5.jpg'),
('Patricia Lee', 78, 'Female', 'Dysphagia, Dementia', 'Pureed foods, Thickened liquids', '2025-10-22', 'https://example.com/photos/patient6.jpg'),
('Carlos Martinez', 50, 'Male', 'Lactose Intolerance, IBS', 'Lactose-free, Low FODMAP', '2025-10-30', 'https://example.com/photos/patient7.jpg'),
('Susan Anderson', 42, 'Female', 'Food Allergies (Nuts, Shellfish)', 'Nut-free, Shellfish-free', '2025-11-01', 'https://example.com/photos/patient8.jpg');

-- ======================================
-- INGREDIENTS DATA
-- ======================================
INSERT INTO ingredients (name, nutritional_info, supplier, quantity, unit, expiry_date, last_inspection_date, storage_temp) VALUES
('Brown Rice', '{"calories": 216, "protein": 5, "carbs": 45, "fiber": 3.5, "fat": 1.8}'::jsonb, 'Whole Grains Co.', 50.00, 'kg', '2026-03-15', '2025-10-30', 20.0),
('Chicken Breast', '{"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6}'::jsonb, 'Fresh Poultry Farm', 30.00, 'kg', '2025-11-10', '2025-11-01', 2.0),
('Salmon Fillet', '{"calories": 206, "protein": 22, "carbs": 0, "fat": 13, "omega3": 2.3}'::jsonb, 'Ocean Harvest', 15.00, 'kg', '2025-11-08', '2025-11-01', 1.0),
('Sweet Potato', '{"calories": 86, "protein": 1.6, "carbs": 20, "fiber": 3, "vitaminA": 14187}'::jsonb, 'Local Farms', 40.00, 'kg', '2025-11-20', '2025-10-29', 15.0),
('Spinach', '{"calories": 23, "protein": 2.9, "carbs": 3.6, "fiber": 2.2, "iron": 2.7}'::jsonb, 'Green Leaf Suppliers', 10.00, 'kg', '2025-11-06', '2025-11-01', 4.0),
('Low-Fat Milk', '{"calories": 83, "protein": 8, "carbs": 12, "fat": 2, "calcium": 300}'::jsonb, 'Dairy Fresh', 25.00, 'liters', '2025-11-12', '2025-11-02', 3.0),
('Oatmeal', '{"calories": 389, "protein": 17, "carbs": 66, "fiber": 10.6, "fat": 6.9}'::jsonb, 'Whole Grains Co.', 30.00, 'kg', '2026-06-01', '2025-10-28', 18.0),
('Olive Oil', '{"calories": 884, "fat": 100, "saturatedFat": 14, "omega9": 73}'::jsonb, 'Mediterranean Oils', 20.00, 'liters', '2026-08-15', '2025-10-25', 20.0),
('Carrots', '{"calories": 41, "protein": 0.9, "carbs": 10, "fiber": 2.8, "vitaminA": 16706}'::jsonb, 'Local Farms', 35.00, 'kg', '2025-11-18', '2025-10-30', 5.0),
('Quinoa', '{"calories": 368, "protein": 14, "carbs": 64, "fiber": 7, "fat": 6}'::jsonb, 'Healthy Grains Inc.', 25.00, 'kg', '2026-04-20', '2025-10-27', 20.0),
('Greek Yogurt', '{"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4, "calcium": 110}'::jsonb, 'Dairy Fresh', 15.00, 'kg', '2025-11-15', '2025-11-02', 3.0),
('Broccoli', '{"calories": 34, "protein": 2.8, "carbs": 7, "fiber": 2.6, "vitaminC": 89}'::jsonb, 'Green Leaf Suppliers', 20.00, 'kg', '2025-11-09', '2025-11-01', 4.0),
('Lentils', '{"calories": 116, "protein": 9, "carbs": 20, "fiber": 8, "iron": 3.3}'::jsonb, 'Legume Suppliers', 40.00, 'kg', '2026-12-31', '2025-10-20', 22.0),
('Turkey Breast', '{"calories": 135, "protein": 30, "carbs": 0, "fat": 1.5}'::jsonb, 'Fresh Poultry Farm', 20.00, 'kg', '2025-11-09', '2025-11-01', 2.0),
('Blueberries', '{"calories": 57, "protein": 0.7, "carbs": 14, "fiber": 2.4, "antioxidants": "high"}'::jsonb, 'Berry Farms', 8.00, 'kg', '2025-11-07', '2025-11-02', 2.0),
('Almonds', '{"calories": 579, "protein": 21, "carbs": 22, "fiber": 12.5, "fat": 50}'::jsonb, 'Nut Suppliers', 15.00, 'kg', '2026-09-30', '2025-10-15', 20.0),
('Tofu', '{"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "calcium": 350}'::jsonb, 'Soy Products Co.', 12.00, 'kg', '2025-11-14', '2025-11-01', 4.0),
('Tomatoes', '{"calories": 18, "protein": 0.9, "carbs": 3.9, "fiber": 1.2, "vitaminC": 14}'::jsonb, 'Local Farms', 25.00, 'kg', '2025-11-10', '2025-10-31', 12.0);

-- ======================================
-- RECIPES DATA
-- ======================================
INSERT INTO recipes (name, description, image_url, total_calories, created_by) VALUES
('Grilled Chicken with Steamed Vegetables', 'Lean grilled chicken breast served with steamed broccoli and carrots', 'https://example.com/recipes/grilled-chicken.jpg', 320.50, 2),
('Diabetic-Friendly Salmon Bowl', 'Baked salmon with quinoa and spinach, low glycemic index', 'https://example.com/recipes/salmon-bowl.jpg', 425.00, 2),
('Gluten-Free Oatmeal Breakfast', 'Steel-cut oats with blueberries and low-fat milk', 'https://example.com/recipes/oatmeal.jpg', 280.00, 3),
('Low-Sodium Turkey Stir-Fry', 'Turkey breast with mixed vegetables in olive oil', 'https://example.com/recipes/turkey-stirfry.jpg', 310.00, 2),
('Kidney-Friendly Lentil Soup', 'Low potassium lentil soup with carrots and herbs', 'https://example.com/recipes/lentil-soup.jpg', 245.00, 3),
('Pureed Sweet Potato Blend', 'Smooth pureed sweet potato for dysphagia patients', 'https://example.com/recipes/pureed-potato.jpg', 180.00, 3),
('High-Protein Greek Yogurt Parfait', 'Greek yogurt layered with blueberries (nut-free)', 'https://example.com/recipes/yogurt-parfait.jpg', 210.00, 2),
('Mediterranean Quinoa Salad', 'Quinoa with tomatoes, spinach, and olive oil dressing', 'https://example.com/recipes/quinoa-salad.jpg', 295.00, 3),
('Soft Diet Chicken Puree', 'Finely pureed chicken with gravy for post-surgical patients', 'https://example.com/recipes/chicken-puree.jpg', 190.00, 2),
('Low-Carb Tofu Scramble', 'Scrambled tofu with spinach and tomatoes', 'https://example.com/recipes/tofu-scramble.jpg', 165.00, 3);

-- ======================================
-- RECIPE_INGREDIENTS DATA
-- ======================================
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
-- Grilled Chicken with Steamed Vegetables
(1, 2, 150, 'grams'),
(1, 12, 100, 'grams'),
(1, 9, 80, 'grams'),
(1, 8, 10, 'ml'),
-- Diabetic-Friendly Salmon Bowl
(2, 3, 120, 'grams'),
(2, 10, 100, 'grams'),
(2, 5, 80, 'grams'),
(2, 8, 15, 'ml'),
-- Gluten-Free Oatmeal Breakfast
(3, 7, 80, 'grams'),
(3, 15, 50, 'grams'),
(3, 6, 150, 'ml'),
-- Low-Sodium Turkey Stir-Fry
(4, 14, 130, 'grams'),
(4, 12, 100, 'grams'),
(4, 9, 80, 'grams'),
(4, 8, 12, 'ml'),
-- Kidney-Friendly Lentil Soup
(5, 13, 100, 'grams'),
(5, 9, 80, 'grams'),
(5, 8, 10, 'ml'),
-- Pureed Sweet Potato Blend
(6, 4, 200, 'grams'),
(6, 6, 50, 'ml'),
-- High-Protein Greek Yogurt Parfait
(7, 11, 150, 'grams'),
(7, 15, 80, 'grams'),
-- Mediterranean Quinoa Salad
(8, 10, 100, 'grams'),
(8, 18, 80, 'grams'),
(8, 5, 50, 'grams'),
(8, 8, 15, 'ml'),
-- Soft Diet Chicken Puree
(9, 2, 120, 'grams'),
(9, 6, 80, 'ml'),
-- Low-Carb Tofu Scramble
(10, 17, 150, 'grams'),
(10, 5, 60, 'grams'),
(10, 18, 50, 'grams');

-- ======================================
-- MEAL_PLANS DATA
-- ======================================
INSERT INTO meal_plans (patient_id, created_by, start_date, end_date, ai_generated, notes) VALUES
(1, 2, '2025-11-01', '2025-11-07', FALSE, 'Diabetic diet plan - Monitor blood sugar levels closely'),
(2, 3, '2025-11-01', '2025-11-07', FALSE, 'Strict gluten-free diet, iron supplementation needed'),
(3, 2, '2025-11-01', '2025-11-07', FALSE, 'Renal diet - Low potassium, phosphorus, and sodium'),
(4, 3, '2025-11-01', '2025-11-07', TRUE, 'AI-generated weight management plan - 1500 cal/day'),
(5, 2, '2025-11-01', '2025-11-07', FALSE, 'Post-surgical soft diet, small frequent meals'),
(6, 3, '2025-11-01', '2025-11-07', FALSE, 'Pureed diet for dysphagia, all liquids thickened'),
(7, 2, '2025-11-01', '2025-11-07', FALSE, 'Low FODMAP, lactose-free diet'),
(8, 3, '2025-11-01', '2025-11-07', FALSE, 'Allergen-free diet - No nuts or shellfish');

-- ======================================
-- MEAL_PLAN_RECIPES DATA
-- ======================================
INSERT INTO meal_plan_recipes (meal_plan_id, recipe_id, meal_type, portion_size) VALUES
-- Patient 1 (Robert - Diabetic)
(1, 3, 'Breakfast', '1 serving'),
(1, 2, 'Lunch', '1 serving'),
(1, 1, 'Dinner', '1 serving'),
(1, 7, 'Snack', '0.5 serving'),
-- Patient 2 (Maria - Celiac)
(2, 3, 'Breakfast', '1 serving'),
(2, 8, 'Lunch', '1 serving'),
(2, 4, 'Dinner', '1 serving'),
-- Patient 3 (James - Kidney Disease)
(3, 3, 'Breakfast', '0.75 serving'),
(3, 5, 'Lunch', '1 serving'),
(3, 1, 'Dinner', '0.75 serving'),
-- Patient 4 (Linda - Weight Management)
(4, 10, 'Breakfast', '1 serving'),
(4, 8, 'Lunch', '1 serving'),
(4, 1, 'Dinner', '1 serving'),
-- Patient 5 (Ahmed - Post-surgical)
(5, 9, 'Breakfast', '0.5 serving'),
(5, 6, 'Lunch', '1 serving'),
(5, 9, 'Dinner', '0.5 serving'),
-- Patient 6 (Patricia - Dysphagia)
(6, 6, 'Breakfast', '1 serving'),
(6, 6, 'Lunch', '1 serving'),
(6, 9, 'Dinner', '1 serving'),
-- Patient 7 (Carlos - IBS)
(7, 3, 'Breakfast', '1 serving'),
(7, 10, 'Lunch', '1 serving'),
(7, 4, 'Dinner', '1 serving'),
-- Patient 8 (Susan - Allergies)
(8, 3, 'Breakfast', '1 serving'),
(8, 8, 'Lunch', '1 serving'),
(8, 4, 'Dinner', '1 serving');

-- ======================================
-- NUTRITION_ENTRIES DATA
-- ======================================
INSERT INTO nutrition_entries (patient_id, recipe_id, recorded_by, date, intake_percentage, blood_sugar, notes) VALUES
(1, 3, 4, '2025-11-01', 95.00, 128.5, 'Patient ate well, blood sugar within target range'),
(1, 2, 4, '2025-11-01', 100.00, 142.0, 'Completed lunch, slight elevation in blood sugar'),
(1, 1, 5, '2025-11-01', 85.00, 135.0, 'Left some vegetables, blood sugar acceptable'),
(2, 3, 4, '2025-11-01', 100.00, NULL, 'No adverse reactions to gluten-free meal'),
(2, 8, 4, '2025-11-01', 90.00, NULL, 'Good appetite, tolerated well'),
(3, 3, 5, '2025-11-01', 75.00, NULL, 'Limited appetite, encouraged fluid intake'),
(3, 5, 5, '2025-11-01', 80.00, NULL, 'Ate most of soup, compliant with renal restrictions'),
(4, 10, 4, '2025-11-02', 100.00, 108.0, 'Enjoyed breakfast, motivated for weight loss'),
(5, 9, 5, '2025-11-02', 60.00, NULL, 'Post-surgical day 5, tolerating soft foods slowly'),
(6, 6, 4, '2025-11-02', 70.00, NULL, 'Required assistance, swallowing safely with puree'),
(7, 3, 5, '2025-11-02', 95.00, NULL, 'No GI symptoms, tolerating low FODMAP well'),
(8, 3, 4, '2025-11-02', 100.00, NULL, 'No allergic reactions, satisfied with meal');

-- ======================================
-- SAFETY_LOGS DATA
-- ======================================
INSERT INTO safety_logs (ingredient_id, facility_area, temperature, inspector_id, inspection_date, compliance_status, remarks, document_url) VALUES
(2, 'Cold Storage Unit A', 2.0, 6, '2025-11-01', 'Pass', 'Chicken stored at proper temperature, no contamination detected', 'https://example.com/safety/inspection-001.pdf'),
(3, 'Cold Storage Unit A', 1.0, 6, '2025-11-01', 'Pass', 'Salmon fresh, proper storage conditions maintained', 'https://example.com/safety/inspection-002.pdf'),
(5, 'Refrigerator B', 4.5, 7, '2025-11-01', 'Pass', 'Spinach fresh, within expiry date', 'https://example.com/safety/inspection-003.pdf'),
(6, 'Dairy Refrigerator', 3.0, 6, '2025-11-02', 'Pass', 'Milk temperature acceptable, sealed containers', 'https://example.com/safety/inspection-004.pdf'),
(15, 'Cold Storage Unit B', 2.5, 7, '2025-11-02', 'Pass', 'Blueberries fresh, no mold detected', 'https://example.com/safety/inspection-005.pdf'),
(1, 'Dry Storage Room', 21.0, 6, '2025-10-30', 'Warning', 'Temperature slightly elevated, AC needs adjustment', 'https://example.com/safety/inspection-006.pdf'),
(7, 'Dry Storage Room', 20.0, 7, '2025-10-28', 'Pass', 'Oatmeal properly sealed, pest control effective', 'https://example.com/safety/inspection-007.pdf'),
(18, 'Produce Storage', 13.0, 6, '2025-10-31', 'Pass', 'Tomatoes inspected, quality good', 'https://example.com/safety/inspection-008.pdf');

-- ======================================
-- ALERTS DATA
-- ======================================
INSERT INTO alerts (type, message, triggered_by, status) VALUES
('Safety Violation', 'Temperature in Dry Storage Room exceeded safe range (21°C)', 6, 'Resolved'),
('Expiry Warning', 'Spinach (Ingredient ID: 5) expires in 5 days - use soon', 6, 'Active'),
('Expiry Warning', 'Blueberries (Ingredient ID: 15) expires in 5 days', 7, 'Active'),
('Low Stock', 'Greek Yogurt stock below reorder threshold (15kg remaining)', 7, 'Active'),
('Patient Alert', 'Patient Robert Johnson blood sugar elevated after lunch (142 mg/dL)', 4, 'Resolved'),
('Safety Violation', 'Salmon shipment delayed, delivery temperature log missing', 6, 'Resolved');

-- ======================================
-- Verification Queries
-- ======================================


SELECT COUNT(*) as staff_count FROM staff;
SELECT COUNT(*) as patients_count FROM patients;
SELECT COUNT(*) as ingredients_count FROM ingredients;
SELECT COUNT(*) as recipes_count FROM recipes;
SELECT COUNT(*) as meal_plans_count FROM meal_plans;
SELECT COUNT(*) as nutrition_entries_count FROM nutrition_entries;
SELECT COUNT(*) as safety_logs_count FROM safety_logs;
SELECT COUNT(*) as alerts_count FROM alerts;

-- Sample Test Queries
-- ======================================
-- ======================================

-- Get all meal plans for diabetic patients
SELECT mp.*, p.name, p.medical_conditions 
FROM meal_plans mp
JOIN patients p ON mp.patient_id = p.id
WHERE p.medical_conditions LIKE '%Diabetes%';

-- Get ingredients expiring soon (within 7 days)
-- SELECT name, expiry_date, quantity, unit
-- FROM ingredients
-- WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
-- ORDER BY expiry_date;

-- Get all recipes with their ingredients
-- SELECT r.name as recipe_name, i.name as ingredient_name, ri.quantity, ri.unit
-- FROM recipes r
-- JOIN recipe_ingredients ri ON r.id = ri.recipe_id
-- JOIN ingredients i ON ri.ingredient_id = i.id
-- ORDER BY r.name;

-- Get patient nutrition tracking with blood sugar
-- SELECT p.name, r.name as recipe, ne.date, ne.intake_percentage, ne.blood_sugar, ne.notes
-- FROM nutrition_entries ne
-- JOIN patients p ON ne.patient_id = p.id
-- JOIN recipes r ON ne.recipe_id = r.id
-- ORDER BY ne.date DESC, p.name;

-- ======================================
-- Done ✅
-- ======================================