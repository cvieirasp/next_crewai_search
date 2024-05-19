from crewai import Crew

from agents import CourseReasearchAgents
from job_manager import append_event
from tasks import CourseResearchTasks

class CourseResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None

    def configure_crew(self, courses: list[str], subjects: list[str]):
        print(f'Configuring crew for {self.job_id} with courses {courses} and subjects {subjects}')

        # Configuração dos Agents
        agents = CourseReasearchAgents()
        research_manager = agents.research_manager(courses, subjects)
        course_research_agent = agents.course_research_agent()

        # Configuração das Tasks
        tasks = CourseResearchTasks(self.job_id)
        course_research_tasks = [
            tasks.course_research(course_research_agent, course, subject) for course in courses for subject in subjects
        ]

        manage_research = tasks.manage_research(research_manager, courses, subjects, course_research_tasks)

        # Criação do Crew
        self.crew = Crew(
            agents=[research_manager, course_research_agent],
            tasks=[*course_research_tasks, manage_research],
            verbose=2,
        )

    def start_crew(self):
        if not self.crew:
            print(f'No crew found for {self.job_id}')
            return
        
        append_event(self.job_id, 'CREW_STARTED')
        
        try:
            print(f'Starting crew for {self.job_id}')
            results = self.crew.start()
            append_event(self.job_id, 'CREW_COMPLETED')
            return results
        except Exception as e:
            append_event(self.job_id, 'CREW_ERROR')
            return f'Error starting crew for {self.job_id}: {e}'