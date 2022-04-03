
## 3. Move spark_dag.py to ~/airflow/dags

### 3.2 - Move spark_dag.py to ~/PySpark/workspace/dags

```bash
mv spark_dag.py ~/airflow/dags
```

## 4, Open port 8080 to see Airflow UI and check if `example_spark_operator` exists. 
If it does not exist yet, give it a few seconds to refresh.

## 5. Spark Configuration

### 5.1 - Update spark_default 
Under the `Admin` section of the menu, select `spark_default` and update the host to the Spark master URL. Save once done

### 5.2 - Turn on DAG
Select the `DAG` menu item and return to the dashboard. Unpause the `example_spark_operator`, and then click on the `example_spark_operator`link. 

## 6. Trigger the DAG 
Trigger from the tree view and click on the graph view afterwards

## 7. Review Logs
Once the jobs have run, you can click on each task in the graph view and see their logs. In their logs, we should see value of Pi that each job calculated, and the two numbers differing between Python and Scala

## 8. Trigger DAG from command line

### 8.1 - Open a new terminal and run `airflow dags`

```bash
airflow dags trigger example_spark_operator
```

### 8.2 - If we want to trigger only one task

```bash
airflow tasks run example_spark_operator python_submit_job now
```

And that wraps up our basic walkthrough on using Airflow to schedule Spark jobs.
