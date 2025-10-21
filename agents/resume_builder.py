from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class ResumeBuilder:
	def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
		self.llm = ChatGroq(
			api_key=groq_api_key,
			model_name=model_name
		)
		# Prompt asks the model to compare the JD and the resume, provide per-section feedback,
		# make minimal edits preserving the resume's original format and ordering, and return JSON.
		self.prompt = PromptTemplate(
			input_variables=["resume_text", "jd_text"],
			template=(
				"""
				You are a resume editor. Do NOT create a new resume format or change the resume layout.
				You will be given the applicant's current resume text (which may be plain text extracted from a PDF/DOCX)
				and the full job description text. Your tasks:
				1) Compare the JD to the resume and for each resume section (Summary, Skills, Experience, Education, Other)
				   provide concise feedback on how well that section matches the JD. For each section include:
				   - match_score (0-5),
				   - comments (short suggestions),
				   - important_keywords_to_add (list)
				2) Produce a minimally edited version of the resume that keeps the original format and ordering,
				   only modifying or adding lines/phrases to better match the JD. Do not reformat, do not reorder sections,
				   and do not invent sections.
				3) Indicate whether another refinement is recommended with a boolean 'request_rebuild'.

				Return a JSON object with keys: 'sections' (object by section name), 'revised_resume' (string),
				and 'request_rebuild' (true/false). Example:
				{
				  "sections": {"Summary": {"match_score":4, "comments":"...", "important_keywords_to_add":[...]}, ...},
				  "revised_resume": "...full resume text...",
				  "request_rebuild": false
				}
				Only return the JSON (no extra commentary). Here are the inputs:\n\nResume:\n{resume_text}\n\nJob Description:\n{jd_text}\n"""
			)
		)

	def build(self, resume_text: str, jd_text: str) -> dict:
		import json
		chain = self.prompt | self.llm
		response = chain.invoke({
			"resume_text": resume_text,
			"jd_text": jd_text
		})
		response_text = getattr(response, "content", response) if hasattr(response, "content") else response
		# Try to parse JSON; allow for JSON embedded in text
		try:
			result = json.loads(response_text)
		except Exception:
			import re
			match = re.search(r"{.*}\n?", response_text, re.DOTALL)
			if match:
				try:
					result = json.loads(match.group(0))
				except Exception:
					result = {"sections": {}, "revised_resume": resume_text, "request_rebuild": False}
			else:
				result = {"sections": {}, "revised_resume": resume_text, "request_rebuild": False}
		return result
