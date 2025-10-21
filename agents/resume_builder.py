from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class ResumeBuilder:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.llm = ChatGroq(
			api_key=groq_api_key,
			model_name=model_name
		)
		self.prompt = PromptTemplate(
			input_variables=["resume_text", "jd_analysis"],
			template=(
				"""
				You are an expert resume writer. Given the following resume:\n{resume_text}\n\n"
				"And the following job description analysis (JSON):\n{jd_analysis}\n\n"
				"Rewrite or tailor the resume to better match the key skills, tone, and keywords from the job description analysis."
				"Keep the resume professional, concise, and relevant to the job."
				"Return only the improved resume text."
				"""
			)
		)

	def build(self, resume_text: str, jd_analysis: dict) -> str:
		import json
		chain = self.prompt | self.llm
		response = chain.invoke({
			"resume_text": resume_text,
			"jd_analysis": json.dumps(jd_analysis)
		})
		response_text = getattr(response, "content", response) if hasattr(response, "content") else response
		return response_text.strip()
