from agents.resume_builder import ResumeBuilder
from agents.supervisor import Supervisor

class ResumeFlow:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.resume_builder = ResumeBuilder(groq_api_key, model_name)
		self.supervisor = Supervisor(groq_api_key, model_name)

	def run(self, jd_text: str, resume_text: str, max_loops: int = 3):
		current_resume = resume_text
		last_eval = None
		last_builder = None
		for _ in range(max_loops):
			# Builder compares JD and resume and returns sections + revised_resume
			builder_result = self.resume_builder.build(current_resume, jd_text)
			revised = builder_result.get("revised_resume", current_resume)
			# Supervisor evaluates the revised resume against the JD
			evaluation = self.supervisor.evaluate(revised, jd_text)
			last_eval = evaluation
			last_builder = builder_result
			# stop when neither asks for rebuild
			if not builder_result.get("request_rebuild", False) and not evaluation.get("request_rebuild", False):
				return {
					"resume": revised,
					"builder": builder_result,
					"evaluation": evaluation
				}
			current_resume = revised
		# If still not effective after max_loops
		return {
			"resume": current_resume,
			"builder": last_builder,
			"evaluation": last_eval,
			"note": "Max rebuild attempts reached."
		}
