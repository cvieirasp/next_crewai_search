from crewai import Task, Agent
from textwrap import dedent

from job_manager import append_event
from models import ResultInfo, ResultInfoList

class CourseResearchTasks():
    def __init__(self, job_id: str):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        print(f'Appending event for {self.job_id} with task output {task_output}')
        append_event(self.job_id, task_output.exported_output)

    def manage_research(self, agent: Agent, courses: list[str], subjects: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f'''
                Based on the list of {courses} and {subjects}, 
                use the results from the Course Reasearch Agent to research each course and subject 
                to put together a JSON object containing the URLs for 33 blog articles, 
                the URLs and title for 3 YouTube course or tutorial videos.
            '''),
            agent=agent,
            expected_output=dedent('''
                A JSON object containing the URLs for 3 blog articles and 
                the URLs and titles for 3 YouTube course or tutorial videos.
            '''),
            callback=self.append_event_callback,
            context=tasks,
            output_json=ResultInfoList,
        )
    
    def course_research(self, agent: Agent, course: str, subject: str):
        return Task(
            description=dedent(f'''
                Research the course {course} and subject {subject}.
                For each course, find the URLs and titles for 3 recent YouTube course or tutorial videos.
                For each subject, find the URLs for 3 recent blog articles.
                Return the collected information in a JSON object.

                Helpful Tips:
                - To find the blog articles names and URLs, perform searches on Google such like the following:
                    - "{subject} [POSITION HERE] blog articles"
                - To find the YouTube course or tutorial videos, perform searches on YouTube such as the following:
                    - "{course} [POSITION HERE] course or tutorial"

                Important:
                - Once you have found the information, immediately stop searching for additional information.
                - Only return the requested information. Nothing else.
                - Do not generate fake information. Only return the information you find. Nothing else.
                - Do not stop researching until you find the requested information for each course and subject.
            '''),
            agent=agent,
            expected_output=dedent('A JSON object containing the researched information for each position in the company.'),
            callback=self.append_event_callback,
            output_json=ResultInfo,
            async_execution=True,
        )