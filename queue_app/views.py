import hashlib

from queue_app import app
from queue_app.tasks import scrape_url
from queue_app import q 
from queue_app.__init__ import r

from flask import redirect, render_template, request, url_for

from rq.job import Job

@app.route("/", methods=["GET", "POST"])
def add_task():
    if request.args:
        url = request.args.get("url")
        job_id = hashlib.md5(url.encode()).hexdigest()
        q.enqueue(scrape_url, url, job_id = job_id, result_ttl=5000)
        return redirect(url_for(f"get_results", job_key=job_id))
    return render_template("index.html")


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    q_len = len(q.jobs) + 1
    job = Job.fetch(job_key, connection=r)

    # Print errors to console
    try:
        if type(job.result) != "list":
            print(job.result)
        elif job.result[2]:
            print(job.result[2])
    except:
        pass

    if job.is_finished:
        return render_template("results_page.html", paragraphs=job.result[0], title = job.result[1]), 200
    else:
        return render_template("results_page.html", paragraphs=False, q_len=q_len), 202
