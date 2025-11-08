# Airflow DAG Exploration Guide
**Interactive guide to understanding your pipeline**

## 🎯 Step-by-Step Exploration

### Exercise 1: Trigger and Monitor the Pipeline

**Goal**: Run the pipeline and watch it execute

1. **Open Airflow**
   - URL: http://localhost:8080
   - Login: admin / admin123

2. **Find the DAG**
   - Look for `simple_document_pipeline`
   - If "paused" toggle is OFF (grey), click it to enable

3. **Trigger the Pipeline**
   - Click the **Play button** (▶) on the right
   - Click **"Trigger DAG"**
   - Click **"Trigger"** to confirm

4. **Watch it Run**
   - Click on the DAG name to enter detailed view
   - Select **"Grid"** view
   - Watch the boxes change colors:
     - Grey → Yellow (queued/running) → Green (success)

5. **Expected Timeline**:
   ```
   0s:    check_api_health starts (yellow)
   2s:    check_api_health completes (green)
   2s:    list_pending_documents starts (yellow)
   3s:    list_pending_documents completes (green)
   3s:    process_documents_batch starts (yellow)
   5s:    process_documents_batch completes (green)
   5s:    validate_results starts (yellow)
   6s:    validate_results completes (green)
   6s:    generate_pipeline_report starts (yellow)
   7s:    generate_pipeline_report completes (green)
   DONE!  All tasks green ✅
   ```

---

### Exercise 2: View Task Logs

**Goal**: See what each task actually does

1. **Click on** `check_api_health` (the first green box)
2. **Click "Log" tab**
3. **Read the output**:
   ```
   [2025-11-06 20:00:00] INFO - Checking API health
   [2025-11-06 20:00:01] INFO - ✅ API is healthy
   [2025-11-06 20:00:01] INFO - Marking task as SUCCESS
   ```

4. **Repeat for each task**:
   - `list_pending_documents` → See document list
   - `process_documents_batch` → See processing stats
   - `validate_results` → See validation metrics
   - `generate_pipeline_report` → See final report

5. **What to look for**:
   - ✅ Success messages
   - ❌ Error messages (if task failed)
   - 📊 Statistics (counts, percentages, times)
   - 🔍 Detailed processing info

---

### Exercise 3: Understand Data Flow (XCom)

**Goal**: See how tasks share data

1. **Click on** `list_pending_documents` task
2. **Go to "XCom" tab**
3. **You'll see**:
   ```json
   {
     "key": "document_list",
     "value": {
       "total_documents": 3,
       "documents": [
         "education-loan-agreement.pdf",
         "home-loan-agreement.pdf",
         "personal-loan-application.pdf"
       ]
     }
   }
   ```

4. **This data is used by**: `process_documents_batch` (next task)

5. **Check XCom for other tasks**:
   - `process_documents_batch` → Processing results
   - `validate_results` → Validation stats

---

### Exercise 4: View the Visual Graph

**Goal**: Understand the workflow structure

1. **Click "Graph" view** (top menu)
2. **You'll see the flow**:
   ```
   [check_api_health]
          ↓
   [list_pending_documents]
          ↓
   [process_documents_batch]
          ↓
   [validate_results]
          ↓
   [generate_pipeline_report]
   ```

3. **Click on each box** to see task details
4. **Arrows show dependencies**:
   - Task 2 waits for Task 1 to finish
   - Task 3 waits for Task 2 to finish
   - etc.

---

### Exercise 5: Check Task Duration

**Goal**: Identify bottlenecks

1. **Click "Task Duration" view**
2. **See bar chart**:
   ```
   check_api_health:        ██ 2s
   list_pending_documents:  █ 0.5s
   process_documents_batch: ████████ 15s  ← SLOWEST
   validate_results:        █ 0.3s
   generate_report:         ██ 1s
   ```

3. **Interpretation**:
   - Longest bar = Bottleneck (slowest task)
   - In this case: `process_documents_batch` takes most time
   - This is expected (it's doing the actual processing)

---

### Exercise 6: View DAG Code

**Goal**: Understand the implementation

1. **Click "Code" view**
2. **Scroll through the Python code**
3. **Key sections to find**:

   **DAG Definition**:
   ```python
   dag = DAG(
       dag_id='simple_document_pipeline',
       schedule_interval='@daily',
       start_date=datetime(2025, 11, 1),
   )
   ```

   **Task Functions**:
   ```python
   def check_api_health(**context):
       """Task 1: Check if API is healthy"""
       response = requests.get(f"{API_BASE_URL}/health")
       if response.status_code == 200:
           logger.info("✅ API is healthy")
   ```

   **Task Dependencies**:
   ```python
   task1 >> task2 >> task3 >> task4 >> task5
   ```
   *(This means: task1 runs first, then task2, then task3, etc.)*

---

### Exercise 7: Run Multiple Times

**Goal**: See execution history

1. **Trigger the DAG again** (Play button)
2. **Wait for completion**
3. **Go to Grid view**
4. **You'll now see**:
   ```
   Run 2: ✅✅✅✅✅  (latest)
   Run 1: ✅✅✅✅✅  (previous)
   ```

5. **Click on different runs** to compare:
   - Duration differences
   - Any failures in history
   - Performance trends

---

### Exercise 8: Force a Failure

**Goal**: Learn how to debug failures

1. **Stop the API service**:
   ```bash
   docker stop loan-extractor-api
   ```

2. **Trigger the DAG**

3. **Watch Task 1 fail** (turns red):
   ```
   ❌ check_api_health - FAILED
   ⚪ list_pending_documents - NOT RUN (upstream failed)
   ⚪ process_documents_batch - NOT RUN
   ⚪ validate_results - NOT RUN
   ⚪ generate_pipeline_report - NOT RUN
   ```

4. **Click the red box → View logs**:
   ```
   ERROR - API health check failed
   Connection refused to http://api:8000/health
   ```

5. **Fix it**:
   ```bash
   docker start loan-extractor-api
   ```

6. **Click "Clear" on failed task** to retry

---

## 🎓 Understanding DAG Components

### 1. DAG Parameters

| Parameter | What it means | Example |
|-----------|---------------|---------|
| `dag_id` | Unique name | `simple_document_pipeline` |
| `schedule_interval` | How often to run | `@daily`, `@hourly`, `*/5 * * * *` |
| `start_date` | When scheduling begins | `datetime(2025, 11, 1)` |
| `catchup` | Run for past dates | `False` = No |
| `max_active_runs` | Concurrent runs allowed | `1` = Only one at a time |
| `tags` | Labels for filtering | `['mlops', 'api-based']` |

### 2. Task Parameters

| Parameter | What it means | Example |
|-----------|---------------|---------|
| `task_id` | Unique task name | `check_api_health` |
| `python_callable` | Function to run | `task_check_api_health` |
| `retries` | How many retry attempts | `2` |
| `retry_delay` | Wait between retries | `timedelta(minutes=2)` |
| `execution_timeout` | Max time allowed | `timedelta(minutes=5)` |

### 3. Task States

| Color/State | Meaning | What to do |
|-------------|---------|------------|
| ⚪ Grey (None) | Not yet run | Wait for upstream tasks |
| 🟡 Yellow (Running) | Currently executing | Monitor logs |
| 🟢 Green (Success) | Completed successfully | Nothing - all good! |
| 🔴 Red (Failed) | Task failed | Check logs, fix, retry |
| 🟠 Orange (Queued) | Waiting for resources | Be patient |
| 🟣 Purple (Up for retry) | Failed, will retry | Wait for retry |
| ⬛ Black (Skipped) | Intentionally skipped | Normal in some workflows |

---

## 🔍 Common Questions

### Q1: Why did my task fail?
**A**: Click the red box → Log tab → Scroll to bottom for error message

### Q2: How do I re-run a failed task?
**A**: Click failed task → "Clear" button → Confirm

### Q3: How do I see what data was passed between tasks?
**A**: Click any task → XCom tab → See all data

### Q4: Can I run tasks manually in order?
**A**: Yes! Click task → "Run" button (for testing)

### Q5: How do I change the schedule?
**A**: Edit the DAG file → Change `schedule_interval` → Airflow auto-updates

### Q6: How do I pause the DAG?
**A**: Click the toggle switch on the DAG list page (turns grey when paused)

### Q7: Where are the logs stored?
**A**: In `/opt/airflow/logs/` inside the Airflow container

### Q8: Can I see historical runs?
**A**: Yes! Grid view shows all past runs in rows

---

## 📊 Real-World Monitoring Checklist

Use this checklist when monitoring your pipeline:

### Daily Checks
- [ ] Check last run status (Grid view)
- [ ] Verify all tasks are green
- [ ] Check total run duration (should be consistent)
- [ ] Review any error logs

### Weekly Checks
- [ ] Check success rate over time (Calendar view)
- [ ] Identify any slow tasks (Task Duration view)
- [ ] Review XCom data sizes (growing too large?)
- [ ] Check for retries (might indicate intermittent issues)

### Monthly Checks
- [ ] Analyze performance trends
- [ ] Review and optimize slow tasks
- [ ] Check disk space in logs directory
- [ ] Update dependencies if needed

---

## 🎯 Advanced Topics

### Parallel Tasks

Currently, all tasks run sequentially (one after another). You can make some run in parallel:

```python
# Sequential (current):
task1 >> task2 >> task3

# Parallel (example):
task1 >> [task2, task3] >> task4
```

This means task2 and task3 run at the same time, then task4 waits for both.

### Dynamic Tasks

You can create tasks dynamically based on data:

```python
# For each document, create a processing task
for doc in documents:
    task = PythonOperator(
        task_id=f'process_{doc}',
        python_callable=process_document,
        op_kwargs={'doc': doc}
    )
```

### Task Groups

Group related tasks together:

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup("processing_group") as group:
    task2 = PythonOperator(...)
    task3 = PythonOperator(...)
    task4 = PythonOperator(...)
```

---

## 🚀 Next Steps

1. ✅ **Complete all exercises above**
2. ✅ **Trigger the pipeline 3-5 times** to see consistency
3. ✅ **Check logs for each task** to understand output
4. ✅ **View XCom data** to see data flow
5. ✅ **Try the "force failure" exercise** to learn debugging

---

## 📚 Quick Reference

### Access URLs
- **Airflow UI**: http://localhost:8080
- **API**: http://localhost:8000
- **Dashboard**: http://localhost:8501

### Login
- **Username**: admin
- **Password**: admin123

### Useful Commands
```bash
# View DAG list
docker exec loan-extractor-airflow-webserver airflow dags list

# Trigger DAG
docker exec loan-extractor-airflow-webserver airflow dags trigger simple_document_pipeline

# View logs
docker logs loan-extractor-airflow-scheduler

# Check DAG status
docker exec loan-extractor-airflow-webserver airflow dags list-runs -d simple_document_pipeline
```

---

**Last Updated**: November 6, 2025  
**DAG Version**: simple_document_pipeline v1.0
