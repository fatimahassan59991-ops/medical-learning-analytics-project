-- ============================================================================
-- queries.sql
-- Example analysis queries against data/training.db (SQLite)
-- Run with: sqlite3 data/training.db < sql/queries.sql
-- or load training.db in any SQL client / Power BI.
--
-- These queries use the `training_data` VIEW, which already joins
-- students + courses + training_records into one flat table.
-- ============================================================================

-- 1. Overall completion rate across all training modules
SELECT
  COUNT(*) AS total_enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct
FROM training_data;

-- 2. Completion rate and average learning gain by course
--    (this is the query that surfaces the core finding of the project)
SELECT
  course_name,
  training_format,
  duration_hours,
  COUNT(*) AS enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct,
  ROUND(AVG(CASE WHEN completion_status = 'Completed' THEN post_test_score - pre_test_score END), 1) AS avg_learning_gain,
  ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM training_data
GROUP BY course_name
ORDER BY completion_rate_pct ASC;

-- 3. Completion rate by training format
SELECT
  training_format,
  COUNT(*) AS enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct,
  ROUND(AVG(CASE WHEN completion_status = 'Completed' THEN post_test_score - pre_test_score END), 1) AS avg_learning_gain
FROM training_data
GROUP BY training_format
ORDER BY completion_rate_pct DESC;

-- 4. Long modules vs. short modules, within Behavioral Science & Psychiatry only
--    (isolates duration as the driver, holding category constant)
SELECT
  CASE WHEN duration_hours >= 4 THEN 'Long (4+ hrs)' ELSE 'Short (<4 hrs)' END AS module_length,
  COUNT(*) AS enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct,
  ROUND(AVG(CASE WHEN completion_status = 'Completed' THEN post_test_score - pre_test_score END), 1) AS avg_learning_gain,
  ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM training_data
WHERE category = 'Behavioral Science & Psychiatry'
GROUP BY module_length;

-- 5. Completion rate by teaching campus (all courses combined)
SELECT
  campus,
  COUNT(*) AS enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct
FROM training_data
GROUP BY campus
ORDER BY completion_rate_pct DESC;

-- 6. Satisfaction score by completion status
SELECT
  completion_status,
  COUNT(*) AS enrollments,
  ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM training_data
WHERE satisfaction_score IS NOT NULL AND satisfaction_score != ''
GROUP BY completion_status
ORDER BY avg_satisfaction DESC;

-- 7. Assessment attempts vs. module duration
SELECT
  CASE WHEN duration_hours >= 4 THEN 'Long (4+ hrs)' ELSE 'Short (<4 hrs)' END AS module_length,
  ROUND(AVG(assessment_attempts), 2) AS avg_attempts
FROM training_data
WHERE completion_status != 'Not Started'
GROUP BY module_length;

-- 8. Average completion time (days from enrollment to finish) by course
SELECT
  course_name,
  duration_hours,
  COUNT(*) AS completions,
  ROUND(AVG(completion_time_days), 1) AS avg_completion_time_days
FROM training_data
WHERE completion_status = 'Completed'
GROUP BY course_name
ORDER BY avg_completion_time_days DESC;

-- 9. Pre-test score vs. number of assessment attempts
SELECT
  assessment_attempts,
  COUNT(*) AS enrollments,
  ROUND(AVG(pre_test_score), 1) AS avg_pre_test_score
FROM training_data
WHERE assessment_attempts > 0
GROUP BY assessment_attempts
ORDER BY assessment_attempts;

-- 10. The headline comparison: the three long Behavioral Science & Psychiatry
--     digital-workbook modules vs. the two short gamified microlearning
--     modules, side by side
SELECT
  CASE
    WHEN training_format = 'Gamified Microlearning' THEN 'Behavioral Science & Psychiatry - Gamified (short)'
    ELSE 'Behavioral Science & Psychiatry - Digital Workbook (long)'
  END AS module_group,
  COUNT(*) AS enrollments,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct,
  ROUND(AVG(CASE WHEN completion_status = 'Completed' THEN post_test_score - pre_test_score END), 1) AS avg_learning_gain,
  ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM training_data
WHERE category = 'Behavioral Science & Psychiatry'
GROUP BY module_group;
