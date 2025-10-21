from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class Supervisor:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.llm = ChatGroq(
			api_key=groq_api_key,
			model_name=model_name
		)
		self.prompt = PromptTemplate(
			input_variables=["resume_text", "jd_analysis"],
			template=(
				"""
				You are a resume evaluation expert. Given the following resume:\n{resume_text}\n\n"
				"And the following job description analysis (JSON):\n{jd_analysis}\n\n"
				"Evaluate how well the resume matches the job description analysis."
				"Rate effectiveness as 'effective' or 'not effective'."
				"If not effective, briefly explain why and request a rebuild."
				"Return a JSON object with keys: 'effectiveness', 'feedback', 'request_rebuild' (true/false)."
				"""
			)
		)

	def evaluate(self, resume_text: str, jd_analysis: dict) -> dict:
		import json
		chain = self.prompt | self.llm
		response = chain.invoke({
			"resume_text": resume_text,
			"jd_analysis": json.dumps(jd_analysis)
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
					result = {"effectiveness": "not effective", "feedback": "Could not parse response.", "request_rebuild": True}
			else:
				result = {"effectiveness": "not effective", "feedback": "No valid response.", "request_rebuild": True}
		return result
