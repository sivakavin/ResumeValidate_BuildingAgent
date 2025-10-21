import os
from dotenv import load_dotenv
from graph.resume_flow import ResumeFlow

def main():
	load_dotenv()
	groq_api_key = os.getenv("GROQ_API_KEY")
	if not groq_api_key:
		raise ValueError("GROQ_API_KEY not found in .env file.")

	# Sample inputs
	jd_text = """
	We are seeking a Python developer with experience in data analysis, machine learning, and cloud deployment. The ideal candidate is proactive, detail-oriented, and comfortable working in a fast-paced environment. Key skills: Python, Pandas, Scikit-learn, AWS, communication.
	"""
	resume_text = """
	John Doe
	Experienced software engineer skilled in Python and web development. Worked on several web apps and internal tools. Familiar with cloud platforms. Looking for new opportunities to grow.
	"""

	flow = ResumeFlow(groq_api_key)
	result = flow.run(jd_text, resume_text)
	print("Final Approved Resume:\n")
	print(result["resume"])
	print("\nEvaluation:\n", result["evaluation"])
	if "note" in result:
		print("\nNote:", result["note"])

if __name__ == "__main__":
	main()
