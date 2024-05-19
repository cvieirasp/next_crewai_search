# Next Crew Search

This repository host a fullstack application built with Python, CrewAI and NextJS, used to manage Crews. CrewAI is a Cutting-edge framework that empowers collaborative groups of agents, called **crews**, to autonomously define and execute complex tasks. Each crew develops its own strategy for task execution, agent collaboration, and overall workflow.

_To learn more about CrewAI, click [here](https://docs.crewai.com/)._

## Description

The application is designed to:

- **Launch Crews:** The backend is responsible for launching Crews.
- **UI Interface:** The frontend handles the transfer of data to Crews, enabling user interaction and visualization of activity of each Crew.

## Technologies

#### Backend:

- Python
- CrewAI
- Flask

#### Frontend:

- NextJS
- TypeScript

## Running the Application

#### Requirements

- [Poetry](https://python-poetry.org/docs/): Python packaging and dependency management tool.

#### Steps

1. **Clone the Repository:** Clone the repository from GitHub.
2. **Install Dependencies:** Run the following command to install all necessary libraries listed in `pyproject.toml`:
   ```bash
   poetry install --no-root
   ```
3. **Activate Virtual Environment:** Run the following command to enter the project's virtual environment:
   ```bash
   poetry shell
   ```
4. **Start the Application:** Execute the following command to launch the application.
   ```bash
   python api.py
   ```

## API Documentation

**POST:** `/api/crew`

**Request Body**

```json
{
  "courses": ["Course Name"],
  "subjects": ["Subject"]
}
```

**Response**

```json
{
  "job_id": "job ID"
}
```

**GET:** `/api/crew/{job_id}`

**Response**

```json
{
  "job_id": "job ID",
  "status": "job status",
  "result": {},
  "events": [{ "timestamp": "YYYY-MM-DD", "data": "event data" }]
}
```

## References

- **Video:** Fullstack NextJS & CrewAI Crash Course For Beginners ([link to video](https://www.youtube.com/watch?v=d8juNbo3onk&t=480s))
