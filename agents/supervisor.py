from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class Supervisor:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.llm = ChatGroq(
			api_key=groq_api_key,
			model_name=model_name
		)
		self.prompt = PromptTemplate(
			input_variables=["resume_text", "jd_text"],
			template=(
				"""
				You are an expert resume evaluator. You will be given a candidate's resume text and a full job description.
				Compare the resume against the JD and provide a concise evaluation. Return JSON with keys:
				- effectiveness: 'effective' or 'not effective'
				- feedback: short actionable feedback
				- request_rebuild: true/false
				- section_scores: an object mapping resume sections to scores (0-5) and short comments.
				Only return valid JSON.
				Resume:\n{resume_text}\n\nJob Description:\n{jd_text}\n"""
			)
		)

	def evaluate(self, resume_text: str, jd_text: str) -> dict:
		import json
		chain = self.prompt | self.llm
		response = chain.invoke({
			"resume_text": resume_text,
			"jd_text": jd_text
		})
		response_text = getattr(response, "content", response) if hasattr(response, "content") else response
		try:
			result = json.loads(response_text)
		except Exception:
			import re
			match = re.search(r"{.*}", response_text, re.DOTALL)
			if match:
				try:
					result = json.loads(match.group(0))
				except Exception:
					result = {"effectiveness": "not effective", "feedback": "Could not parse response.", "request_rebuild": True, "section_scores": {}}
			else:
				result = {"effectiveness": "not effective", "feedback": "No valid response.", "request_rebuild": True, "section_scores": {}}
		return result
