from langgraph.graph import StateGraph, END
from agents.jd_analyzer import JDAnalyzer
from agents.resume_builder import ResumeBuilder
from agents.supervisor import Supervisor

class ResumeFlow:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.jd_analyzer = JDAnalyzer(groq_api_key, model_name)
		self.resume_builder = ResumeBuilder(groq_api_key, model_name)
		self.supervisor = Supervisor(groq_api_key, model_name)

	def run(self, jd_text: str, resume_text: str, max_loops: int = 3):
		jd_analysis = self.jd_analyzer.analyze(jd_text)
		current_resume = resume_text
		for _ in range(max_loops):
			improved_resume = self.resume_builder.build(current_resume, jd_analysis)
			evaluation = self.supervisor.evaluate(improved_resume, jd_analysis)
			if not evaluation.get("request_rebuild", False):
				return {
					"resume": improved_resume,
					"evaluation": evaluation
				}
			current_resume = improved_resume
		# If still not effective after max_loops
		return {
			"resume": current_resume,
			"evaluation": evaluation,
			"note": "Max rebuild attempts reached."
		}
