JOBS = (
    {"id": "job-1", "owner": "u1", "status": "ready"},
    {"id": "job-2", "owner": "u2", "status": "queued"},
)


def find_job(job_id):
    for job in JOBS:
        if job["id"] == job_id:
            return job.copy()
    return None
