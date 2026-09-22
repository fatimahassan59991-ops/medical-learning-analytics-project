-- ============================================================================
-- queries.sql
-- Example analysis queries against data/ab_test.db (SQLite)
-- Run with: sqlite3 data/ab_test.db < sql/queries.sql
--
-- Raw SQL is used here for the group-level descriptive numbers; the actual
-- significance tests (t-tests, z-test, effect sizes) are run in Python --
-- see scripts/analyze.py -- since SQLite doesn't have built-in statistical
-- test functions.
-- ============================================================================

-- 1. Group sizes (did randomization produce two similarly sized groups?)
SELECT "group", COUNT(*) AS n
FROM ab_test_results
GROUP BY "group";

-- 2. Balance check: average pre-test score by group
--    (should be close if randomization worked -- neither group should have
--    started out stronger, since this score is measured BEFORE training)
SELECT
  "group",
  COUNT(*) AS n,
  ROUND(AVG(pre_test_score), 2) AS avg_pre_test_score,
  ROUND(AVG(pre_test_score * pre_test_score) - AVG(pre_test_score) * AVG(pre_test_score), 2) AS variance
FROM ab_test_results
GROUP BY "group";

-- 3. Balance check: campus mix by group
SELECT campus, "group", COUNT(*) AS n
FROM ab_test_results
GROUP BY campus, "group"
ORDER BY campus, "group";

-- 4. Completion rate by group (the primary outcome)
SELECT
  "group",
  COUNT(*) AS n,
  SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) AS completions,
  ROUND(100.0 * SUM(CASE WHEN completion_status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct
FROM ab_test_results
GROUP BY "group";

-- 5. Average post-test score and learning gain by group (completers only)
SELECT
  "group",
  COUNT(*) AS completers,
  ROUND(AVG(post_test_score), 1) AS avg_post_test_score,
  ROUND(AVG(post_test_score - pre_test_score), 1) AS avg_learning_gain
FROM ab_test_results
WHERE completion_status = 'Completed'
GROUP BY "group";

-- 6. Average satisfaction score by group
SELECT
  "group",
  ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM ab_test_results
WHERE satisfaction_score IS NOT NULL AND satisfaction_score != ''
GROUP BY "group";

-- 7. Average assessment attempts by group
SELECT
  "group",
  ROUND(AVG(assessment_attempts), 2) AS avg_attempts
FROM ab_test_results
WHERE completion_status != 'Not Started'
GROUP BY "group";

-- 8. Average completion time (calendar days) by group
--    (Treatment is delivered over two weeks by design, so this metric is
--    expected to run longer for Treatment even though far more people finish)
SELECT
  "group",
  ROUND(AVG(completion_time_days), 1) AS avg_completion_time_days
FROM ab_test_results
WHERE completion_status = 'Completed'
GROUP BY "group";

-- 9. Full breakdown of completion status by group
SELECT
  "group",
  completion_status,
  COUNT(*) AS n
FROM ab_test_results
GROUP BY "group", completion_status
ORDER BY "group", completion_status;
