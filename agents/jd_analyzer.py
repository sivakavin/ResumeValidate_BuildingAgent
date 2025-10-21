from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class JDAnalyzer:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.llm = ChatGroq(
			api_key=groq_api_key,
			model_name=model_name
		)
		self.prompt = PromptTemplate(
			input_variables=["jd_text"],
			template=(
				"""
				Analyze the following job description (JD):\n{jd_text}\n\n"
				"Extract the following:\n"
				"1. Key skills required (list only the most relevant).\n"
				"2. The overall tone of the JD (e.g., formal, casual, urgent, etc.).\n"
				"3. Important keywords (list only the most important).\n"
				"Return your answer as a JSON object with keys: 'skills', 'tone', 'keywords'."
				"""
			)
		)

	def analyze(self, jd_text: str) -> dict:
		chain = self.prompt | self.llm
		response = chain.invoke({"jd_text": jd_text})
		# Extract text from AIMessage if needed
		response_text = getattr(response, "content", response) if hasattr(response, "content") else response
		import json
		try:
			result = json.loads(response_text)
		except Exception:
			import re
			match = re.search(r"{.*}", response_text, re.DOTALL)
			if match:
				try:
					result = json.loads(match.group(0))
				except Exception:
					result = {"skills": [], "tone": "", "keywords": []}
			else:
				result = {"skills": [], "tone": "", "keywords": []}
		return result
