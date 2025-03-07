# CTI Blog Post AI Feedback Tool

## 1. Project Overview

- **Objective:**  
  Build an AI-powered tool that automatically evaluates student blog posts based on the CTI rubric and provides actionable feedback.

- **Audience:**  
  CTI staff and students using Canvas, with the goal of improving blog quality and supporting underrepresented students.

## 2. Functional Requirements

- **Input:**  
  - Accept blog post text (from Canvas or a user-submitted form).

- **Processing:**  
  - Evaluate text against defined rubric criteria.
  - Use rule-based methods initially to check for the presence/absence of required elements.
  - (Future enhancement: Integrate a lightweight ML model for more nuanced evaluation.)

- **Output:**  
  - Return a structured JSON response containing:
    - Scores or pass/fail flags for each rubric criterion.
    - Specific feedback messages for improvement.
  
## 3. Non-functional Requirements

- **Performance:**  
  - Provide feedback within a few seconds per submission.
  
- **Scalability:**  
  - Designed to serve a small number of CTI users without incurring hosting costs.
  
- **Security:**  
  - Limit access to authorized CTI users (potentially using a simple API key or token for MVP).

## 4. Scope (MVP)

- **Implemented Criteria:**  
  - Section 1: About the Project
  - Section 2: The Issue
  - Section 3: Codebase Overview
  - Section 4: Challenges
  - Section 5: Solution
  
- **Exclusions (For now):**  
  - Grammar and style checks.
  - Advanced ML-based feedback (will start with rule-based checks).
  - Chrome extension front-end (focus first on building a robust API).

## 5. Future Enhancements

- **Enhance Evaluation:**  
  - Integrate fine-tuned ML models for better feedback.
  - Incorporate grammar and style checking.

- **User Interface:**  
  - Develop a Chrome extension for seamless integration with Canvas.
  - Create a dedicated web app for CTI users if needed.

- **Deployment:**  
  - Explore free hosting options (local hosting, Hugging Face Spaces, etc.) to ensure minimal cost.

## 6. Next Steps

1. **Data Preparation:**  
   - Organize sample blog posts and rubric labels into a JSON file for initial testing.

2. **Back-end Development:**  
   - Set up a FastAPI project to serve as the back-end API.
   - Implement rule-based logic to evaluate blog posts based on the requirements.

3. **Testing:**  
   - Use tools like Postman or curl to validate the API responses.
   - Iterate based on feedback from initial tests.

4. **Front-end Planning:**  
   - Outline how the Chrome extension will interact with the API (to be implemented after the back-end is stable).

