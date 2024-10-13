import os
from dotenv import load_dotenv
import openai
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import re

class TextGenerator:
  def __init__(self):
      load_dotenv()
      openai.api_key = os.getenv('OPENAI_API_KEY')
      if not openai.api_key:
          raise ValueError("No se encontró la clave de API de OpenAI en el archivo .env")

      self.models = {
          "es": "PlanTL-GOB-ES/gpt2-base-bne",
          "en": "gpt2"
      }
      self.generators = {}
      for lang, model_name in self.models.items():
          tokenizer = AutoTokenizer.from_pretrained(model_name)
          model = AutoModelForCausalLM.from_pretrained(model_name)
          self.generators[lang] = pipeline('text-generation', model=model, tokenizer=tokenizer)

      self.processed_resume = ""
      self.keywords = []
      self.skills = []

  def process_resume(self, resume_text):
      self.processed_resume = resume_text
      self.extract_keywords_and_skills(resume_text)

  def extract_keywords_and_skills(self, resume_text):
      skills_pattern = r'Habilidades?:\s*([A-Za-z\s,]+)'
      skills_match = re.search(skills_pattern, resume_text, re.IGNORECASE)
      if skills_match:
          self.skills = [skill.strip() for skill in skills_match.group(1).split(',')]
      self.keywords = list(set(re.findall(r'\b\w+\b', resume_text)))

  def generate_response(self, prompt, context, resume, job_description, language='es', model='gpt-3.5-turbo', max_tokens=150, n=1, temperature=0.7):
      if not self.processed_resume:
          self.process_resume(resume)

      system_message = "Eres un asistente de entrevistas útil y profesional." if language == 'es' else "You are a helpful and professional interview assistant."
      user_message = f"Contexto: {context}\nCurriculum: {self.processed_resume}\nDescripción del trabajo: {job_description}\nPregunta: {prompt}\n\nGenera una respuesta apropiada en {'español' if language == 'es' else 'English'}:"

      try:
          response = openai.ChatCompletion.create(
              model=model,
              messages=[
                  {"role": "system", "content": system_message},
                  {"role": "user", "content": user_message}
              ],
              max_tokens=max_tokens,
              n=n,
              stop=None,
              temperature=temperature,
          )
          return response.choices[0].message['content'].strip()
      except Exception as e:
          print(f"Error al usar {model}: {e}")
          generator = self.generators.get(language[:2], self.generators['es'])
          response = generator(user_message, max_length=max_tokens, num_return_sequences=n)
          return response[0]['generated_text'].strip()