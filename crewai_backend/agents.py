from crewai import Agent
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAi

from tools.youtube_search_tools import YoutubeVideoSearchTool

class CourseReasearchAgents():
    def __init__(self):
        self.youtubeSearchTool = YoutubeVideoSearchTool
        self.searchInternetTool = SerperDevTool()
        self.llm = ChatOpenAi(model='gpt-4-turbo-preview')
        
    def research_manager(self, courses: list[str], subjects: list[str]) -> Agent:
        return Agent(
            role='Course Reasearch Manager',
            goal=f'''
                Generate a list of JSON objects containing the urls for 3 recent blog articles for each subject and 
                the url and title for 3 recent YouTube course or tutorial videos for each course.

                Courses: {courses}
                Subjects: {subjects}

                Important:
                - The final list of JSON objects must include all courses and subjects. Do not leave any out.
                - If you can't find information for a specific course or subject, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else.
                - Do not stop researching until you find the requested information for each course and subject.
                - All the courses and subjects exist and are real so keep researching until you find the information for each one.
                - Make sure you each researched course contains 3 YouTube course or tutorial.
                - Make sure you each researched subject contains 3 blog articles.
            ''',
            backstory='As a Course Reasearch Manager, you are responsible for aggregating all the researched information into a list.',
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
            allow_delegation=True,
        )
    
    def course_research_agent(self) -> Agent:
        return Agent(
            role='Course Research Agent',
            goal='''
                Look up the specific courses and find url and title for 3 recent YouTube course or tutorial videos for each course. 
                Look up the specific subjects and find url for 3 recent blog articles for each subject. 
                It is your job to return this collected information in a JSON object.
            ''',
            backstory='''
                As a Course Research Agent, you are responsible for looking up specific courses and subjects 
                and gathering relevant information.

                Important:
                - Once you have found the information, immediately stop searching for additional information.
                - Only return the requested information. Nothin Else.
                - Do not generate fake information. Only return the information you find. Nothin Else.
            ''',
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
        )
        