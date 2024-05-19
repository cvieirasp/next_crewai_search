import datetime
import json
from threading import Thread
from flask import Flask, request, jsonify
from uuid import uuid4

from crew import CourseResearchCrew
from job_manager import append_event, Event, jobs, jobs_lock

app = Flask(__name__)

def start_crew(job_id: str, courses: list[str], subjects: list[str]):
    print(f'Starting crew job for {job_id} with courses {courses} and subjects {subjects}')

    results = None
    try:
        course_research_crew = CourseResearchCrew(job_id)
        course_research_crew.configure_crew(courses, subjects)
        results = course_research_crew.start_crew()
    except Exception as e:
        print(f'CREW FAILED: {str(e)}')
        append_event(job_id, f'CREW FAILED: {str(e)}')
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(
            data='CREW COMPLETED',
            timestamp=datetime.now()
        ))

@app.route('/api/crew/<job_id>', methods=['GET'])
def get_job_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return jsonify({'error': 'job not found'}), 404
        
    try:
        result_json = json.loads(job.result)
    except:
        result_json = job.result

    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'result': result_json,
        'events': [{ 'timestamp':event.timestamp.isoformat(), 'data':event.data } for event in job.events]
    }), 200

@app.route('/api/crew', methods=['POST'])
def execute_crew():
    data = request.json
    if not data or 'courses' not in data or 'subjects' not in data:
        return jsonify({'error': 'invalid request with missing data'}), 400
    
    job_id = str(uuid4())
    courses = data['courses']
    subjects = data['subjects']

    # Executa crew
    thread = Thread(target=start_crew, args=(job_id, courses, subjects))
    thread.start()

    return jsonify({'job_id': job_id}), 200

if __name__ == '__main__':
    app.run(debug=True, port=3001)
